import cfpq_data
import networkx
from typing import Tuple
from pathlib import Path
from networkx import MultiDiGraph
import pydot


def get_graph_info(name: str):
    graph = cfpq_data.graph_from_dataset(name, verbose=False)
    print(f"""info about {name}:\n""")
    print(
        f"""Nodes: {graph.number_of_nodes()}\nEdges: {graph.number_of_edges()}\nLabels: {cfpq_data.get_labels(graph, verbose=False)}""")
    print('end of graph info\n')


"""
"""

"""
По количеству вершин в циклах и именам меток
строить граф из двух циклов и сохранять его в указанный файл в формате DOT (использовать pydot).
"""


def generate_two_cycle_graph(nodes_first: int, nodes_second: int, labels: Tuple[str, str]):
    return cfpq_data.labeled_two_cycles_graph(nodes_first, nodes_second, edge_labels=labels, verbose=False)


def save_graph_dot(graph: MultiDiGraph, path_way: str):
    graph_dot = networkx.drawing.nx_pydot.to_pydot(graph)
    full_path = f"{path_way}/{graph.name}.dot"
    file = open(full_path, "w")
    graph_dot.write_raw(full_path)
    file.close()
    print(f"Graph was saved in {full_path}")
    return full_path
