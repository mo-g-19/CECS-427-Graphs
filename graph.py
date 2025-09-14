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
        #print(f"indv_BFS: {indv_BFS}")
        all_BFS.append(indv_BFS)
    return all_BFS

def analyze_components(G):
    comps = list(nx.connected_components(G))
    print("Connected components:", comps)

def analyze_cycles(G):
    if not nx.is_forest(G):
        print("This graph has a cycle.")
    else:
        print("This graph is acyclic (a forest).")

def analyze_isolates(G):
    isolates = list(nx.isolates(G))
    if isolates:
        print("Graph has isolated nodes:", isolates)
    else:
        print("No isolated nodes.")

def analyze_density(G):
    print("Density:", nx.density(G))

def analyze_avg_shortest_path(G):
    if nx.is_connected(G):
        avg_len = nx.average_shortest_path_length(G)
        print("Average shortest path length:", avg_len)
    else:
        print("This graph is not connected; average shortest path length is undefined.")


def plot_graph(G):
    seed = 951369
    pos = nx.spring_layout(G, seed=seed)
    
    #spliting the nodes into two groups isolated and non isolated
    isolates = set(nx.isolates(G))
    non_isolates = [v for v in G.nodes() if v not in isolates]
    
    # draws all non_isolates
    if non_isolates:
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=non_isolates,
            node_color="cyan",
            node_size=500,
    )

    # draws all isolates
    if isolates:
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=isolates,
            node_color="lightcoral",
            node_size=500,
    )
    
    # draw edges
    nx.draw_networkx_edges(
        G, 
        pos, 
        edge_color="lightgray", 
        width=1.0, 
        alpha=0.6
    )
    
    # adds lables to the nodes not required i just added this in when i was verifying the graph will delete later
    nx.draw_networkx_labels(G, pos, labels={n: n for n in G.nodes()}, font_size=10)

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
            #print(indv_BFS)
            #print()
            for target, path in indv_BFS.items():
                print(f"{target}: {path}")
            print()

    if args.analyze and G:
        analyze_components(G)
        analyze_cycles(G)
        analyze_isolates(G)
        analyze_density(G)
        analyze_avg_shortest_path(G)

    if args.plot and G:
        plot_graph(G)

    if args.output and G:
        save_gml(G, args.output)

if __name__ == "__main__":
    main()
