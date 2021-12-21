import sys
from antlr4 import *
from project.parser.dist.grammarGQLLexer import grammarGQLLexer
from project.parser.dist.grammarGQLParser import grammarGQLParser


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


if __name__ == "__main__":
    main(sys.argv)
