from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    State,
)

__all__ = ["nfa_from_graph"]


def nfa_from_graph(graph, start_nodes: set = None, finale_nodes: set = None):
    """
    This function crate nfa from graph
    :param graph: MultiDiGraph
                  graph to create nfa
    :param start_nodes: set
                        nodes of graph which are represent start states of required nfa
                        default: all states are start states
    :param finale_nodes: set
                         nodes of graph which are represent finale states of required nfa
                         default: all states are finale states
    :return: NondeterministicFiniteAutomaton
             nfa from graph with set start and finale states
    """
    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)
    if finale_nodes == None:
        finale_nodes = set(graph.nodes)
    if start_nodes == None:
        start_nodes = set(graph.nodes)

    for node in start_nodes:
        nfa.add_start_state(State(node))
    for node in finale_nodes:
        nfa.add_final_state(State(node))
    return nfa
