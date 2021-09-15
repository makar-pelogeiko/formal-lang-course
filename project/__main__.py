from project.console import run_console_app
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "menu_item",
        help="int number of menu item 0 - get info about graph; 1 - create 2 cycles graph and "
        "save it to .DOT --data key is necessary",
        type=int,
    )
    parser.add_argument(
        "--data",
        nargs="+",
        default=[],
        help="for 0 menu_item type name of graph, for 1 menu item "
        "type number of nodes in first cycle, second cycle, "
        "left label, right label, path to save graph with "
        "name.dot (test/myGraph.dot)",
    )
    args = parser.parse_args()
    run_console_app(args.menu_item, args.data)


if __name__ == "__main__":
    main()
