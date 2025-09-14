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

    final_BFS = []
    #np.zeros((len(start_nodes), (G.number_of_nodes())))
    #counter_BFS = 0

    G.add_nodes_from(list(n for n in G.nodes), visited=False)       #Instead of creating a visited array (which could make it O(n) if constantly searching through see if visited -> O(1) and an attribute) 0 -> not visited; 1 -> visited
    
    for node in start_nodes:
        final = []
        queue = []

        queue.append(node)

        while len(queue) > 0:
            x = queue.pop()

            if not G.nodes[x]['visited']:
                G.nodes[x]['visited'] = True

            for edge in G.edges(x):             #edge in (G.in_edges(x) + G.out_edges(x)):
                 if not G.nodes[edge[1]]['visited']:
                    queue.append(edge[1])
            
            final.append(x)
        
        final_BFS.append(final)

        for visited_node in G:
            G.nodes[visited_node]['visited'] = False

    return final_BFS

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

    G = None   # local graph variable

    if args.input:
        G = load_gml(args.input)

    if args.create_random_graph:
        n = int(args.create_random_graph[0])
        c = float(args.create_random_graph[1])
        G = create_random_graph(n, c)

    if args.multi_BFS and G:
        all_BFS = multi_BFS(G, args.multi_BFS)
        for indv_BFS in all_BFS:
            print(indv_BFS)

    if args.analyze and G:
        analyze_graph(G)

    if args.plot and G:
        plot_graph(G)

    if args.output and G:
        save_gml(G, args.output)

if __name__ == "__main__":
    main()
