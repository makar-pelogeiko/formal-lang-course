from project import regexp_query_to_graph as rpq
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol
import project.bool_matrices_utils as bools
import pytest
from networkx import MultiDiGraph


@pytest.fixture
def simple_nfa():
    symbol_a = Symbol("a")
    symbol_b = Symbol("b")
    state_z = State(0)
    state_f = State(1)
    nfa = NondeterministicFiniteAutomaton()
    nfa.add_transition(state_z, symbol_a, state_f)
    nfa.add_transition(state_f, symbol_b, state_f)
    nfa.add_start_state(state_z)
    nfa.add_final_state(state_f)
    return nfa


@pytest.fixture
def graph():
    graph = MultiDiGraph()
    graph.add_node(0)
    graph.add_node(1)
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 1, label="b")
    return graph


def test_corect_crossed_nfa_positive(simple_nfa):
    symbol_a = Symbol("a")
    symbol_b = Symbol("b")
    bool_set = bools.BoolMatricesGroup.bool_matrices_from_nfa(simple_nfa)
    result_nfa, trash = bool_set.cross_automats(simple_nfa)
    assert result_nfa.accepts([symbol_a, symbol_b])


def test_corect_crossed_nfa_negative(simple_nfa):
    symbol_a = Symbol("a")
    symbol_b = Symbol("b")
    bool_set = bools.BoolMatricesGroup.bool_matrices_from_nfa(simple_nfa)
    result_nfa, trash = bool_set.cross_automats(simple_nfa)
    assert not result_nfa.accepts([symbol_a, symbol_b, symbol_a])


def test_rpq_positive(graph):
    res = rpq.query_graph_regexp(graph, "a* b*")
    assert {(0, 1), (1, 1)} == res


def test_rpq_part_first(graph):
    res = rpq.query_graph_regexp(graph, "a b*")
    assert {(0, 1)} == res


def test_rpq_part_second(graph):
    res = rpq.query_graph_regexp(
        graph, "a* b*", start_nodes=set([1]), finale_nodes=set([1])
    )
    assert {(1, 1)} == res


def test_rpq_negative(graph):
    res = rpq.query_graph_regexp(
        graph, "a b*", start_nodes=set([1]), finale_nodes=set([1])
    )
    assert set() == res
