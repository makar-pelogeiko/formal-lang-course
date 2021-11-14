"""Class representing a production of an Extended Context Free Grammar"""
from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex


class ECFGProduction:
    """A production in ECFG class"""

    def __init__(self, head_in: Variable, body_in: Regex):
        self.head = head_in
        self.body = body_in

    def __str__(self):
        return str(self.head) + " -> " + str(self.body)
