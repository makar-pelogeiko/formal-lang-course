"""Context Free Grammar Matrix based algorithm"""
from typing import Set, Tuple
from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from scipy import sparse
from project.cfg.cfg_normal_form import cfg_to_cnf

__all__ = ["matrix_based"]


def matrix_based(graph: MultiDiGraph, cfg: CFG) -> Set[Tuple[int, str, int]]:
    """Context-free path querying algorithm. Boolean matrix version"""
    cnf = cfg_to_cnf(cfg)

    var_productions = {p for p in cnf.productions if len(p.body) == 2}
    term_productions = {p for p in cnf.productions if len(p.body) == 1}
    eps_prod_heads = {p.head.value for p in cnf.productions if not p.body}

    nodes_num = graph.number_of_nodes()

    matrices = {
        var.value: sparse.dok_matrix((nodes_num, nodes_num), dtype=bool)
        for var in cnf.variables
    }

    for i, j, data in graph.edges(data=True):
        label = data["label"]
        for var in {p.head.value for p in term_productions if p.body[0].value == label}:
            matrices[var][i, j] = True

    for i in range(nodes_num):
        for var in eps_prod_heads:
            matrices[var][i, i] = True

    matrix_changed = True
    while matrix_changed:
        matrix_changed = False

        for prod in var_productions:
            old_nnz = matrices[prod.head.value].nnz
            matrices[prod.head.value] = matrices[prod.head.value] + (
                matrices[prod.body[0].value] @ matrices[prod.body[1].value]
            )
            new_nnz = matrices[prod.head.value].nnz

            matrix_changed = matrix_changed or old_nnz != new_nnz

    return {
        (i, var, j)
        for var, matrix in matrices.items()
        for i, j in zip(*matrix.nonzero())
    }
