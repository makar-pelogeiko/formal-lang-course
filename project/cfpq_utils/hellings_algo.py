"""Hellings algorithm"""
from pyformlang.cfg import CFG
from typing import Set, Tuple
from networkx import MultiDiGraph
from project.cfg.cfg_normal_form import cfg_to_cnf

__all__ = ["hellings"]


def hellings(graph: MultiDiGraph, cfg: CFG) -> Set[Tuple[int, str, int]]:
    wcnf = cfg_to_cnf(cfg)
    """Hellings algorithm Context Free reachability"""
    term_productions = {p for p in wcnf.productions if len(p.body) == 1}
    var_productions = {p for p in wcnf.productions if len(p.body) == 2}
    eps_productions = {p.head.value for p in wcnf.productions if not p.body}

    r = {
        (i, label, i)
        for i in range(graph.number_of_nodes())
        for label in eps_productions
    } | {
        (v, prod.head.value, u)
        for prod in term_productions
        for v, u, edge_data in graph.edges(data=True)
        if prod.body[0].value == edge_data["label"]
    }

    m_empty = r.copy()
    while m_empty:
        v, N, u = m_empty.pop()
        add_temp_set = set()

        for i, M, j in r:
            if j == v:
                trips = set()
                for prod in var_productions:
                    if (
                        prod.body[0].value == M
                        and prod.body[1].value == N
                        and (i, prod.head.value, u) not in r
                    ):
                        trips.add((i, prod.head.value, u))

                add_temp_set |= trips
                trips.clear()

        m_empty |= add_temp_set
        r |= add_temp_set

        add_temp_set.clear()

        for i, M, j in r:
            if i == u:
                trips = set()
                for prod in var_productions:
                    if (
                        prod.body[0].value == N
                        and prod.body[1].value == M
                        and (v, prod.head.value, j) not in r
                    ):
                        trips.add((v, prod.head.value, j))

                add_temp_set |= trips
                trips.clear()

        m_empty |= add_temp_set
        r |= add_temp_set

        add_temp_set.clear()

    return r
