import pytest
from pyformlang.cfg import CFG, Variable
from project import generate_two_cycle_graph
from project.hellings_algo import cfpq
from cfpq_data import labeled_cycle_graph
from networkx import MultiDiGraph


graph_simple = MultiDiGraph()
graph_simple.add_node(0)
graph_simple.add_node(1)
graph_simple.add_edge(0, 1, label="a")
graph_simple.add_edge(1, 1, label="b")


@pytest.mark.parametrize(
    "cfg_text, graph, start_var, start_nodes, fin_nodes, expect_set",
    [
        (
            """
                    S -> epsilon
                    """,
            labeled_cycle_graph(10, "a", verbose=False),
            Variable("S"),
            {0, 1},
            {0, 1, 2, 3, 4},
            {(0, 0), (1, 1)},
        ),
        (
            """
                    S -> a B
                    B -> epsilon | b
                """,
            graph_simple,
            Variable("S"),
            {0},
            {1},
            {(0, 1)},
        ),
        (
            """
                    S -> A B
                    S -> F B
                    F -> A S
                    A -> a
                    B -> b
                        """,
            generate_two_cycle_graph(1, 2, ("a", "b")),
            Variable("S"),
            None,
            None,
            {(1, 2), (0, 0), (0, 3), (0, 2), (1, 0), (1, 3)},
        ),
    ],
)
def test_cfpq_t(cfg_text, graph, start_var, start_nodes, fin_nodes, expect_set):
    cfg = CFG.from_text(cfg_text)
    result = cfpq(graph, cfg, start_var, start_nodes, fin_nodes)

    assert expect_set == result
