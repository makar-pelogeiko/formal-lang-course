import cfpq_data
import console_lib
import networkx


def input_int(text):
    print(text)
    while (True):
        num = input()
        if num.isdigit():
            return int(num)
        print('need integer positive number (or zero)')


def call_get_info():
    name = input('input name of graph: ')
    console_lib.get_graph_info(name)


def call_generate_and_save_graph():
    first = input_int('number of nodes in first cycle')
    second = input_int('number of nodes in second cycle')
    label = ('dd', 'ff')
    graph = console_lib.generate_two_cycle_graph(first, second, label)
    path = input('type the path to save .DOT file')
    console_lib.save_graph_dot(graph, path)




def menu(items_lst: list[str]):
    while (1 == 1):
        print(f"""{items_lst[0]}\n""")
        num = 1
        for item in items_lst[1:]:
            print(f"""{num} - {item}""")
            num = num + 1
        response = input('input number: ')
        if (response.isdigit()):
            int_resp = int(response)
            if (int_resp > 0) and (int_resp < num):
                return int_resp
        print('you did not chose corect. type number of menu-element and hit <enter>')


def run_console_app():
    func_items = [call_get_info, call_generate_and_save_graph]
    while True:
        menu_lst = ['menu list:', 'exit', 'get info about graph', 'create 2 cycles graph and save it to .DOT']
        element = menu(items_lst=menu_lst) - 2
        if element == -1:
            return
        func_items[element]()
