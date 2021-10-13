import project.bool_finite_automaton as bools
import project.graph_nfa as gr_nfa
import project.regexp_dfa as reg_dfa
from pyformlang.finite_automaton import State


def rpq_graph(
    graph, regexp, start_nodes: set = None, finale_nodes: set = None, matrixEngine=bools
):
    """
    This function crosses graph and regexp and returns pairs - start and final nodes, which can be reached in crossed
    graph
    :param graph: MultiGraph
    :param regexp: string with regular expression
    :param start_nodes: set of graph nodes which will be start states in NFA
    :param finale_nodes: set of graph nodes which will be final states in NFA
    :return: set pairs of graph nodes - rpq answer after crossing graph and regexp
    """
    nfa_source = gr_nfa.nfa_from_graph(
        graph, start_nodes=start_nodes, finale_nodes=finale_nodes
    )
    dfa_query = reg_dfa.dfa_from_regexp(regexp)
    dfa_bool_automaton = matrixEngine.BoolFiniteAutomaton.bool_matrices_from_nfa(
        dfa_query
    )
    bool_nfa = matrixEngine.BoolFiniteAutomaton.bool_matrices_from_nfa(nfa_source)
    bresult_auto = bool_nfa.intersect(dfa_bool_automaton)
    rpq_matrix = matrixEngine.BoolFiniteAutomaton.transitive_closure(
        matrixEngine.BoolFiniteAutomaton.sum_matrixLst(
            list(bresult_auto.bool_matrices.values())
        )
    )
    result_set = set()
    for i, j in zip(*matrixEngine.BoolFiniteAutomaton.nonZeroPairs(rpq_matrix)):
        if (
            State(i) in bresult_auto.start_states
            and State(j) in bresult_auto.final_states
        ):
            result_set.add((i // len(dfa_query.states), j // len(dfa_query.states)))
    return result_set
