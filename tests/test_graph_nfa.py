from project.graph_nfa import nfa_from_graph
from pyformlang.finite_automaton import Symbol
from project import graph_utils

graph = graph_utils.generate_two_cycle_graph(2, 3, ("a", "b"))


def test_non_deterministic():
    nfa = nfa_from_graph(graph)
    assert not nfa.is_deterministic()


def test_word_accept():
    symbol_a = Symbol("a")
    symbol_b = Symbol("b")
    nfa = nfa_from_graph(graph)
    # starts from state 1 ends in state 3 (nfa goes 1 ->(a) 2 ->(a) 0 ->(b) 3) - all states can be finale and start
    assert nfa.accepts([symbol_a, symbol_a, symbol_b])


def test_word_not_accept():
    symbol_a = Symbol("a")
    symbol_b = Symbol("b")
    nfa = nfa_from_graph(graph)
    # all states can be finale and start, but there is no way in graph with such labels
    assert not nfa.accepts([symbol_a, symbol_b, symbol_a])


def test_word_special_state_accept():
    symbol_a = Symbol("a")
    nfa = nfa_from_graph(graph, start_nodes=set([1]), finale_nodes=set([0]))
    # start state 1 and finale state 0, nfa goes 1 ->(a) 2 ->(a) 0
    assert nfa.accepts([symbol_a, symbol_a])
