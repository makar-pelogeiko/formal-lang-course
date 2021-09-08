import networkx
import pydot
import cfpq_data


from project import console_lib


def test_save_to_dot():
    graph = console_lib.generate_two_cycle_graph(2, 3, ("a", "b"))
    console_lib.save_graph_dot(graph, "tests/data/graph1.dot")
    dot_graph = pydot.graph_from_dot_file("tests/data/graph1.dot")[0]
    nx_graph = networkx.drawing.nx_pydot.from_pydot(dot_graph)
    assert nx_graph.number_of_nodes() == 6
    assert nx_graph.number_of_edges() == 7
    assert cfpq_data.get_labels(graph, verbose=False) == {"a", "b"}