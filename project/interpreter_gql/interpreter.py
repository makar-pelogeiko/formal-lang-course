import sys
from antlr4 import *
from project.parser.dist.grammarGQLLexer import grammarGQLLexer
from project.parser.dist.grammarGQLParser import grammarGQLParser
from project.parser.dist.grammarGQLListener import grammarGQLListener
from project.parser.dist.grammarGQLVisitor import grammarGQLVisitor
from project.interpreter_gql.GQLVisitor import GQLTreeVisitor
from project.interpreter_gql.interpreter_utils.interpreter_except import InterpError

from project.parser.parser_invoker import is_in_grammar, parse_to_string


class GQLInterpreter:
    def __init__(self, flag_info=False):
        self.flag_info = flag_info
        self.visitor = GQLTreeVisitor()

    def run_query(self, query):
        lexer = grammarGQLLexer(InputStream(query))
        stream = CommonTokenStream(lexer)
        parser = grammarGQLParser(stream)
        tree = parser.prog()

        try:
            self.visitor.visit(tree)

        except InterpError as exc:
            print("----Exception----")
            print(exc.message)
            print("-----------------")
            for item in exc.stack_lst:
                print(item)
            print("-----------------")

    def online_run(self):
        raw_input = ""
        while raw_input != "exit()":
            raw_input = input(">>")

            if raw_input == "exit()":
                break
            raw_input += "\n"
            if self.flag_info:
                print("\n<<" + parse_to_string(raw_input) + ">>\n")

            if not is_in_grammar(raw_input):
                print("Error input: can not parse")
                continue

            self.run_query(raw_input)

        print("end executing")

    def file_run(self, path):
        file = open(path, "r")
        raw_input = file.read()

        if self.flag_info:
            print("\n<<" + parse_to_string(raw_input) + ">>\n")

        if not is_in_grammar(raw_input):
            print("Error input: can not parse")
            return

        self.run_query(raw_input)

        print("end executing")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "online":
            interp = GQLInterpreter()
            interp.online_run()
        else:
            interp = GQLInterpreter()
            interp.file_run(sys.argv[1])
