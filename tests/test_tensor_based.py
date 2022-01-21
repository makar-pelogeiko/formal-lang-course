import pytest
from pyformlang.cfg import CFG
from project.cfpq_utils.tensor_algo import tensor_based
from project.graph_utils import generate_two_cycle_graph
from cfpq_data import labeled_cycle_graph
from networkx import MultiDiGraph

# pytest.skip("skipping", allow_module_level=True)
graph_simple = MultiDiGraph()
graph_simple.add_node(0)
graph_simple.add_node(1)
graph_simple.add_edge(0, 1, label="a")
graph_simple.add_edge(1, 1, label="b")

##
# Alllow to stay in 1 node by epsilon
##
@pytest.mark.parametrize(
    "cfg_text, graph, expect_set",
    [
        (
            "S -> epsilon",
            graph_simple,
            {(0, "S", 0), (1, "S", 1)},
        ),
        (
            """
                S -> a B
                B -> epsilon | b
                """,
            graph_simple,
            {(0, "S", 1), (1, "B", 1)},
            # not this variant because a - terminal letter, we need only non terminals
            # {(0, "S", 1), (0, "a", 1), (1, "B", 1)},
        ),
        (
            """
                    S -> a
                    """,
            labeled_cycle_graph(4, "a", verbose=False),
            {
                (0, "S", 1),
                (1, "S", 2),
                (2, "S", 3),
                (3, "S", 0),
            },
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
            {
                (0, "A", 1),
                (0, "B", 2),
                (0, "F", 0),
                (0, "F", 2),
                (0, "F", 3),
                (0, "S", 0),
                (0, "S", 2),
                (0, "S", 3),
                (1, "A", 0),
                (1, "F", 0),
                (1, "F", 2),
                (1, "F", 3),
                (1, "S", 0),
                (1, "S", 2),
                (1, "S", 3),
                (2, "B", 3),
                (3, "B", 0),
            },
        ),
    ],
)
def test_tensor(cfg_text, graph, expect_set):
    f = tensor_based(graph, CFG.from_text(cfg_text))
    assert f == expect_set
