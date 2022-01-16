"""Context Free Grammar Tensor based algorithm (Kroneker multiplication)"""
from pyformlang.cfg import CFG
from typing import Set, Tuple
from networkx import MultiDiGraph
from project.graph_nfa import nfa_from_graph
from scipy.sparse import dok_matrix
from project.cfg.cfg_normal_form import cfg_to_cnf
from project.ecfg_utils.ecfg_tools import ecfg_to_rsm
from project.ecfg_utils.ecfg_tools import cfg_to_ecfg
from project.rsm_utils.bool_rsm_automaton import BoolRSMAutomaton

__all__ = ["tensor_based"]


def tensor_based(graph: MultiDiGraph, cfg: CFG) -> set[Tuple[int, str, int]]:
    """Context Free Grammar path querying algorithm. RSM & kroneker version"""
    rsm = ecfg_to_rsm(cfg_to_ecfg(cfg))
    rsm_vars = {box.variable.value for box in rsm.boxes.values()}
    rsm_bm = BoolRSMAutomaton.from_rsm(rsm)
    # TODO graph to rsm bool matrix
    graph_bm = BoolRSMAutomaton.from_automaton(nfa_from_graph(graph))

    # Get all variables loops into matrices of graph
    for eps_state_allow in rsm_bm.start_states & rsm_bm.final_states:
        variable_eps = rsm_bm.variables_of_start_final_states.get(
            (eps_state_allow, eps_state_allow)
        )
        if variable_eps not in graph_bm.bool_matrices:
            graph_bm.bool_matrices[variable_eps] = dok_matrix(
                (graph_bm.num_states, graph_bm.num_states), dtype=bool
            )
        for i in range(graph_bm.num_states):
            graph_bm.bool_matrices[variable_eps][i, i] = True

    # Prepare: first action before cycle
    temp_tc = graph_bm.intersect(rsm_bm).transitive_closure()
    prev_nnz = temp_tc.nnz
    new_nnz = 0

    # Main action: while we add something to result matrices -> continue
    while prev_nnz != new_nnz:
        for i, j in zip(*temp_tc.nonzero()):
            rsm_from = i % rsm_bm.num_states
            rsm_to = j % rsm_bm.num_states
            variable_eps = rsm_bm.variables_of_start_final_states.get(
                (rsm_from, rsm_to)
            )
            if not variable_eps:
                continue
            graph_from = i // rsm_bm.num_states
            graph_to = j // rsm_bm.num_states
            if variable_eps not in graph_bm.bool_matrices:
                graph_bm.bool_matrices[variable_eps] = dok_matrix(
                    (graph_bm.num_states, graph_bm.num_states), dtype=bool
                )
            graph_bm.bool_matrices[variable_eps][graph_from, graph_to] = True

        temp_tc = graph_bm.intersect(rsm_bm).transitive_closure()

        prev_nnz, new_nnz = new_nnz, temp_tc.nnz

    return {
        (i, label, j)
        for label, bm in graph_bm.bool_matrices.items()
        if label in rsm_vars
        for i, j in zip(*bm.nonzero())
    }
