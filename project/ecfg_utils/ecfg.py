"""Class that implements an Extended Context Free Grammar"""
from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex
from project.ecfg_utils.ecfg_production import ECFGProduction


class ECFG:
    """Extended CFG
    productions = dictionary {head: ECFGProduction} head - is instance of Variable()"""

    def __init__(
        self,
        variables=None,
        start_symbol: Variable = None,
        productions: dict = None,
    ):
        self.variables = variables or set()
        self.start_symbol = start_symbol
        self.productions = productions or dict()

    def to_text(self) -> str:
        """Returns a string representation of Extended Context Free Grammar"""
        return "\n".join(str(production) for production in self.productions.values())

    @classmethod
    def from_text(cls, text, start_symbol=Variable("S")):
        """Reads an Extended Context Free Grammar from a text"""
        variables = set()
        productions = dict()
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            production_lst = line.split("->")

            if len(production_lst) != 2:
                raise Exception(f"""Wrong line in text: {line}""")

            head_str, body_str = production_lst
            head = Variable(head_str.strip())

            if head in variables:
                raise Exception(f"{line}")

            variables.add(head)
            body = Regex(body_str.strip())
            productions[head] = ECFGProduction(head, body)

        return ECFG(
            variables=variables, start_symbol=start_symbol, productions=productions
        )
