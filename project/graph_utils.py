import cfpq_data
import networkx
from typing import Tuple
from pathlib import Path
from networkx import MultiDiGraph
import pydot


def get_graph_info(name: str):
    graph = cfpq_data.graph_from_dataset(name, verbose=False)
    return (
        name,
        graph.number_of_nodes(),
        graph.number_of_edges(),
        cfpq_data.get_labels(graph, verbose=False),
    )


def generate_two_cycle_graph(
    nodes_first: int, nodes_second: int, labels: Tuple[str, str]
):
    return cfpq_data.labeled_two_cycles_graph(
        nodes_first, nodes_second, edge_labels=labels, verbose=False
    )


def save_graph_dot(graph: MultiDiGraph, full_path: str):
    graph_dot = networkx.drawing.nx_pydot.to_pydot(graph)
    file = open(full_path, "w")
    graph_dot.write_raw(full_path)
    file.close()
    print(f"Graph was saved in {full_path}")
    return full_path
