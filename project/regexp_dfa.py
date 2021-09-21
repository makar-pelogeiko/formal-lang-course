from pyformlang.regular_expression import Regex

__all__ = ["dfa_from_regexp"]


def dfa_from_regexp(strin: str):
    """strin - string which contains regular expression from which equivalent DFA is builded"""
    regex = Regex(strin)
    dfa = regex.to_epsilon_nfa().to_deterministic()
    dfa_min = dfa.minimize()
    return dfa_min
