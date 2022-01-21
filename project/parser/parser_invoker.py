import sys
from antlr4 import *
from project.parser.dist.grammarGQLLexer import grammarGQLLexer
from project.parser.dist.grammarGQLParser import grammarGQLParser
from project.parser.dist.grammarGQLListener import grammarGQLListener

from pydot import Dot, Node, Edge
from antlr4.tree.Tree import TerminalNodeImpl

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, ParserRuleContext


def main(argv):
    input_ = FileStream(argv[1])
    lexer = grammarGQLLexer(input_)

    # lexer = grammarGQLLexer(InputStream(argv[1]))
    stream = CommonTokenStream(lexer)
    parser = grammarGQLParser(stream)
    tree = parser.prog()
    print(tree.toStringTree(recog=parser))


def parse_to_string(line):
    lexer = grammarGQLLexer(InputStream(line))
    stream = CommonTokenStream(lexer)
    parser = grammarGQLParser(stream)
    tree = parser.prog()
    return tree.toStringTree(recog=parser)


def is_in_grammar(line):
    lexer = grammarGQLLexer(InputStream(line))
    stream = CommonTokenStream(lexer)
    parser = grammarGQLParser(stream)
    tree = parser.prog()
    if parser.getNumberOfSyntaxErrors() > 0:
        return False
    else:
        return True


def write_to_dot(line: str, path: str):
    if not is_in_grammar(line):
        print("Can not parse input line!")
        return False
    lexer = grammarGQLLexer(InputStream(line))
    stream = CommonTokenStream(lexer)
    parser = grammarGQLParser(stream)
    ast = parser.prog()
    tree = Dot("tree", graph_type="digraph")
    ParseTreeWalker().walk(DotTreeListener(tree, grammarGQLParser.ruleNames), ast)
    tree.write(path)
    return True


class DotTreeListener(grammarGQLListener):
    def __init__(self, tree: Dot, rules):
        self.tree = tree
        self.num_nodes = 0
        self.nodes = {}
        self.rules = rules
        super(DotTreeListener, self).__init__()

    def enterEveryRule(self, ctx: ParserRuleContext):
        if ctx not in self.nodes:
            self.num_nodes += 1
            self.nodes[ctx] = self.num_nodes
        if ctx.parentCtx:
            self.tree.add_edge(Edge(self.nodes[ctx.parentCtx], self.nodes[ctx]))
        label = self.rules[ctx.getRuleIndex()]
        self.tree.add_node(Node(self.nodes[ctx], label=label))

    def visitTerminal(self, node: TerminalNodeImpl):
        self.num_nodes += 1
        self.tree.add_edge(Edge(self.nodes[node.parentCtx], self.num_nodes))
        self.tree.add_node(Node(self.num_nodes, label=f"TERM: {node.getText()}"))


if __name__ == "__main__":
    main(sys.argv)
