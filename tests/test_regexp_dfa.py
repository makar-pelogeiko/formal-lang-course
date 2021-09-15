from project.regexp_dfa import dfa_from_regexp
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, Symbol, State
from pyformlang.regular_expression import Regex


def test_correct_dfa():
    dfa_correct = DeterministicFiniteAutomaton()
    symbol_a = Symbol("a")
    symbol_b = Symbol("b")
    state_first = State(0)
    state_second = State(1)
    dfa_correct.add_final_state(state_second)
    dfa_correct.add_start_state(state_first)
    dfa_correct.add_transition(state_first, symbol_a, state_second)
    dfa_correct.add_transition(state_second, symbol_b, state_second)
    assert dfa_correct == dfa_from_regexp("a b*")


def test_accuracy_dfa():
    reg_exp = "abc|a"
    dfa_first = dfa_from_regexp(reg_exp)
    dfa_second = dfa_from_regexp(reg_exp)
    assert dfa_first == dfa_second


def test_is_deterministic():
    assert dfa_from_regexp("a|b(c|d)*").is_deterministic()


def test_word_accept():
    symbol_a = Symbol("a")
    symbol_b = Symbol("b")
    dfa = dfa_from_regexp("a b*")
    assert dfa.accepts([symbol_a, symbol_b, symbol_b])


def test_word_not_accept():
    symbol_a = Symbol("a")
    symbol_b = Symbol("b")
    dfa = dfa_from_regexp("a b*")
    assert not dfa.accepts([symbol_a, symbol_b, symbol_b, symbol_a])
