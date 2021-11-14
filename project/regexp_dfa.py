from pyformlang.regular_expression import Regex

__all__ = ["dfa_from_regexp"]


def dfa_from_regexp(strin):
    """strin - string which contains regular expression from which equivalent DFA is builded
    OR already Regex object"""
    if type(strin) is str:
        regex = Regex(strin)
    else:
        regex = strin
    dfa = regex.to_epsilon_nfa().to_deterministic()
    dfa_min = dfa.minimize()
    return dfa_min
