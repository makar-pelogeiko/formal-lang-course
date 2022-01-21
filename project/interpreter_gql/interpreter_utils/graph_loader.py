import networkx
import pydot
import cfpq_data
import pytest
from project import graph_utils


def load_from_disk(path):
    dot_graph = pydot.graph_from_dot_file(path)[0]
    graph = networkx.drawing.nx_pydot.from_pydot(dot_graph)
    return graph


def load_from_network(path):
    graph = cfpq_data.graph_from_dataset(path, verbose=False)
    return graph
