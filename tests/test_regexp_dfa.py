from project.regexp_dfa import mdfa_from_regexp
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, Symbol, State


def test_correct_minimal_dfa():
    dfa_correct = DeterministicFiniteAutomaton()
    symbol_a = Symbol("a")
    symbol_b = Symbol("b")
    state_first = State(0)
    state_second = State(1)
    dfa_correct.add_final_state(state_second)
    dfa_correct.add_start_state(state_first)
    dfa_correct.add_transition(state_first, symbol_a, state_second)
    dfa_correct.add_transition(state_second, symbol_b, state_second)
    assert dfa_correct == mdfa_from_regexp("a b*")


def test_is_deterministic():
    assert mdfa_from_regexp("a|b(c|d)*").is_deterministic()
