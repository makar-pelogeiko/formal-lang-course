import project.bool_finite_automaton as bools
import project.graph_nfa as gr_nfa
import project.regexp_dfa as reg_dfa
from scipy.sparse.csgraph import floyd_warshall
import math
from pyformlang.finite_automaton import State


def rpq_graph(graph, regexp, start_nodes: set = None, finale_nodes: set = None):
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
    dfa_bool_automaton = bools.BoolFiniteAutomaton.bool_matrices_from_nfa(dfa_query)
    bool_nfa = bools.BoolFiniteAutomaton.bool_matrices_from_nfa(nfa_source)
    # answer_nfa, b_result = bool_nfa.intersect(dfa_bool_automaton)
    bresult_auto = bool_nfa.intersect(dfa_bool_automaton)
    matrix_answer = sum(bresult_auto.bool_matrices.values())
    # rpq_matrix = floyd_warshall(matrix_answer)
    # floyd algo puts zeros on main diagonal, i don't know why
    # rpq_matrix[matrix_answer.nonzero()] = 1.0
    ###
    # tc = sum(self.bmatrix.values())
    prev_nnz = matrix_answer.nnz
    curr_nnz = 0

    while prev_nnz != curr_nnz:
        matrix_answer += matrix_answer @ matrix_answer
        prev_nnz, curr_nnz = curr_nnz, matrix_answer.nnz
    rpq_matrix = matrix_answer
    ###
    result_set = set()
    for i, j in zip(*rpq_matrix.nonzero()):
        if (
            State(i) in bresult_auto.nfa.start_states
            and State(j) in bresult_auto.nfa.final_states
        ):
            result_set.add((i // len(dfa_query.states), j // len(dfa_query.states)))
    return result_set
