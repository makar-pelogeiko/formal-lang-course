import networkx
import pydot
import cfpq_data
import pytest
from project import graph_utils

# pytestmark = pytest.mark.skip("github workflow can't run these tests, run it local")
# uncomment this
graph = graph_utils.generate_two_cycle_graph(2, 3, ("a", "b"))
graph_utils.save_graph_dot(graph, "tests/data/graph1.dot")
dot_graph = pydot.graph_from_dot_file("tests/data/graph1.dot")[0]


def test_nodes():
    nx_graph = networkx.drawing.nx_pydot.from_pydot(dot_graph)

    assert set(nx_graph.nodes) == {1, 2, 0, 3, 4, 5, 777}
    assert nx_graph.number_of_nodes() == 6


def test_edges():
    nx_graph = networkx.drawing.nx_pydot.from_pydot(dot_graph)
    assert nx_graph.number_of_edges() == 7


def test_labels():
    nx_graph = networkx.drawing.nx_pydot.from_pydot(dot_graph)
    assert cfpq_data.get_labels(graph, verbose=False) == {"a", "b"}
