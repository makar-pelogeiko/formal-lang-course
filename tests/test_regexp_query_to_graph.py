from project import rpq as rpq
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol
import project.bool_finite_automaton as bools
import pytest
from project import graph_utils

pytestmark = pytest.mark.skip("github workflow can't run these tests, run it local")
# can not generate 2 cycle graph


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
    graph = graph_utils.generate_two_cycle_graph(2, 3, ("a", "b"))
    return graph


def test_corect_intersect_nfa_positive(simple_nfa):
    symbol_a = Symbol("a")
    symbol_b = Symbol("b")
    bool_set = bools.BoolFiniteAutomaton.bool_matrices_from_nfa(simple_nfa)
    result_bnfa = bool_set.intersect(bool_set)
    nfa = result_bnfa.get_nfa()
    assert nfa.accepts([symbol_a, symbol_b])


def test_corect_intersect_nfa_negative(simple_nfa):
    symbol_a = Symbol("a")
    symbol_b = Symbol("b")
    bool_set = bools.BoolFiniteAutomaton.bool_matrices_from_nfa(simple_nfa)
    result_bnfa = bool_set.intersect(bool_set)
    nfa = result_bnfa.get_nfa()
    assert not nfa.accepts([symbol_a, symbol_b, symbol_a])


@pytest.mark.parametrize(
    "start_states,final_states,regexp,expected",
    [
        (None, None, "a b*", {(0, 1), (2, 4), (1, 2), (2, 0), (2, 3), (2, 5)}),
        (set([1]), set([1]), "a* b*", {(1, 1)}),
        (set([1]), set([1]), "a b*", set()),
    ],
)
def test_rpq_results(graph, start_states, final_states, regexp, expected):
    res = rpq.rpq_graph(
        graph, regexp, start_nodes=start_states, finale_nodes=final_states
    )
    assert expected == res
