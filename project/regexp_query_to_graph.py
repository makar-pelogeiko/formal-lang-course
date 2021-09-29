import project.bool_matrices_utils as bools
import project.graph_nfa as gr_nfa
import project.regexp_dfa as reg_dfa
from scipy.sparse.csgraph import floyd_warshall
import math
from pyformlang.finite_automaton import State


def query_graph_regexp(
    graph, regexp, start_nodes: set = None, finale_nodes: set = None
):
    """
    This function crosses graph and regexp and returns pairs - start and final nodes, which can be reached in crossed
    graph
    :param graph: MultiGraph
    :param regexp: string
    :param start_nodes: set of graph
    :param finale_nodes: set of graph
    :return: set pairs of graph nodes - rpq answer after crossing graph and regexp
    """
    nfa_source = gr_nfa.nfa_from_graph(
        graph, start_nodes=start_nodes, finale_nodes=finale_nodes
    )
    dfa_query = reg_dfa.dfa_from_regexp(regexp)
    bool_nfa = bools.BoolMatricesGroup.bool_matrices_from_nfa(nfa_source)
    answer_nfa, b_result = bool_nfa.cross_automats(dfa_query)
    matrix_answer = sum(b_result.values())
    rpq_matrix = floyd_warshall(matrix_answer)
    # floyd algo puts zeros on main diagonal, i don't know why
    rpq_matrix[matrix_answer.nonzero()] = 1.0
    result_set = set()
    for i, j in zip(*rpq_matrix.nonzero()):
        if (
            rpq_matrix[i, j] != math.inf
            and State(i) in answer_nfa.start_states
            and State(j) in answer_nfa.final_states
        ):
            result_set.add((i // len(dfa_query.states), j // len(dfa_query.states)))
    return result_set
