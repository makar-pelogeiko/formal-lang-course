import cfpq_data
import project.graph_utils
import networkx


def input_int(text):
    print(text)
    while True:
        num = input()
        if num.isdigit():
            return int(num)
        print("need integer positive number (or zero)")


def call_get_info(lst):
    name = lst[0]
    g_info = project.graph_utils.get_graph_info(name)
    print(
        f"""Ifo about graph:\nName: {g_info[0]}\nNodes: {g_info[1]}\nEdges{g_info[2]}\nLabels:{g_info[3]}\n"""
    )


def call_generate_and_save_graph(lst):
    first = int(lst[0])
    second = int(lst[1])
    left = lst[2]
    right = lst[3]
    label = [left, right]
    graph = project.graph_utils.generate_two_cycle_graph(first, second, label)
    path = lst[4]
    project.graph_utils.save_graph_dot(graph, path)


def run_console_app(item: int, lst):
    func_items = [call_get_info, call_generate_and_save_graph]
    if not (0 <= item < 2):
        return
    func_items[item](lst)
