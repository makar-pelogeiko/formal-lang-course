import networkx
import pydot
import cfpq_data
import pytest
from project import graph_utils


graph = graph_utils.generate_two_cycle_graph(2, 3, ("a", "b"))
graph_utils.save_graph_dot(graph, "tests/data/graph1.dot")
dot_graph = pydot.graph_from_dot_file("tests/data/graph1.dot")[0]


def test_nodes():
    nx_graph = networkx.drawing.nx_pydot.from_pydot(dot_graph)
    assert nx_graph.number_of_nodes() == 6 or set(nx_graph.nodes) == {
        "4",
        "5",
        "\\n",
        "3",
        "1",
        "0",
        "2",
    }


def test_edges():
    nx_graph = networkx.drawing.nx_pydot.from_pydot(dot_graph)
    assert nx_graph.number_of_edges() == 7


def test_labels():
    nx_graph = networkx.drawing.nx_pydot.from_pydot(dot_graph)
    assert cfpq_data.get_labels(graph, verbose=False) == {"a", "b"}
