"""Hellings algorithm"""
from pyformlang.cfg import CFG, Variable
from typing import Set, Tuple, Callable
from networkx import MultiDiGraph
from project.cfg.cfg_normal_form import cfg_to_cnf
from project.cfpq_utils.hellings_algo import hellings

__all__ = ["cfpq"]


def cfpq(
    graph: MultiDiGraph,
    cfg: CFG,
    start_symbol: Variable = Variable("S"),
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
    engine: Callable[[MultiDiGraph, CFG], Set[Tuple[int, str, int]]] = hellings,
) -> Set[Tuple[int, int]]:
    """Context Free Path Querying with specific algorithm"""
    cfg._start_symbol = start_symbol
    cnf = cfg_to_cnf(cfg)

    result_pairs = {
        (i, j)
        for i, symbol, j in engine(graph, cnf)
        if symbol == cnf.start_symbol.value
    }

    if start_nodes:
        result_pairs = {(i, j) for i, j in result_pairs if i in start_nodes}
    if final_nodes:
        result_pairs = {(i, j) for i, j in result_pairs if j in final_nodes}

    return result_pairs
