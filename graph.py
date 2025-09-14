import time
import math
import argparse
import matplotlib.pyplot as plt
import networkx as nx


# Functions
# ====================================================================================================
def load_gml(path: str):
    print(f"load_gml called with path={path}")
    Graph = nx.read_gml(path)
    return Graph

def save_gml(G, path: str):
    nx.write_gml(G, path)
    print(f"Graph saved to {path}")


def create_random_graph(n: int, c: float):
    seed = int(time.time())
    p = (c * math.log(n)) / n                   #calculating the probablility based off the probablilty funtion in the assignment
    G = nx.erdos_renyi_graph(n, p, seed=seed)    #generating the graph
    return  G

def multi_BFS(G, start_nodes: list[int]):
    all_BFS = []
    for indv_node in start_nodes:
        indv_BFS = nx.single_source_shortest_path(G, indv_node)
        all_BFS.append(indv_BFS)
    return all_BFS

def analyze_graph(G):
    print("analyze_graph called on G")


def plot_graph(G):
    seed = int(time.time())
    pos = nx.spring_layout(G, seed=seed)    #Honesly dont know what this does just copied this from the test code 
    nx.draw(G, pos=pos)                     #place holder anyway this whole funtion needs to be redone
    plt.show()




# Arg Parser
# ====================================================================================================
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Graph CLI")

    parser.add_argument(
        "--input",
        type=str,
        help="Path to input GML file"
        )
    parser.add_argument(
        "--output", 
        type=str,
        help="Path to output GML file"
        )

    parser.add_argument(
        "--create_random_graph",
        nargs=2,
        metavar=("n", "c"),
        help="Generate random graph with n nodes and parameter c",
    )

    parser.add_argument(
        "--multi_BFS",
        nargs="+",
        type=int,
        metavar="start_nodes",
        help="Run multi-source BFS from given nodes",
    )

    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Print graph analysis",
    )

    parser.add_argument(
        "--plot",
        action="store_true",
        help="Show graph plot",
    )

    return parser



# Main
# ====================================================================================================
def main():
    parser = build_parser()
    args = parser.parse_args()

    G = None            # local graph variable -> all functions
    root_nodes = []     # local root nodes variable -> made in multi_BFS, used in plot

    if args.input:
        G = load_gml(args.input)

    if args.create_random_graph:
        n = int(args.create_random_graph[0])
        c = float(args.create_random_graph[1])
        G = create_random_graph(n, c)

    if args.multi_BFS and G:
        root_nodes = args.multi_BFS
        all_BFS = multi_BFS(G, root_nodes)
        for indv_BFS in all_BFS:
            for target, path in indv_BFS.items():
                print(f"{target}: {path}")
            print()

    if args.analyze and G:
        analyze_graph(G)

    if args.plot and G:
        plot_graph(G)

    if args.output and G:
        save_gml(G, args.output)

if __name__ == "__main__":
    main()
