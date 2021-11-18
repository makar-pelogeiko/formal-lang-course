"""Class representing a box of RSM"""
from pyformlang.cfg import Variable
from pyformlang.finite_automaton import DeterministicFiniteAutomaton


class Box:
    """A box for Recursive State Machine"""

    def __init__(
        self, variable: Variable = None, dfa: DeterministicFiniteAutomaton = None
    ):
        self.dfa = dfa
        self.variable = variable

    def __eq__(self, second: "Box"):
        return self.variable == second.variable and self.dfa.is_equivalent_to(
            second.dfa
        )

    def minimize(self):
        self.dfa = self.dfa.minimize()
