from collections import deque
import time
import math
import argparse
import random
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
    
    mapping = {i: str(i) for i in G.nodes()}    #Making all the lables strings as per sinstructions
    G = nx.relabel_nodes(G, mapping)
    for v in G.nodes():
        G.nodes[v]["label"] = v
    return  G

def multi_BFS(G, start_nodes: list[str]):
    all_BFS = []
    for indv_node in start_nodes:
        indv_BFS = nx.single_source_shortest_path(G, indv_node)
        all_BFS.append(indv_BFS)
    return all_BFS

def compute_bfs_meta(G: nx.Graph, roots):
    # checks all the roots to make sure they are in g and also that they are stings
    roots = [str(r) for r in (roots or []) if str(r) in G]

    dist, parent, source = {}, {}, {}
    q = deque()

    # initializes the queues
    for r in roots:
        dist[r] = 0
        parent[r] = None
        source[r] = r
        q.append(r)

    # BFS
    while q:
        u = q.popleft()
        for v in G.neighbors(u):            # loop pretty much runs bfs again but this time keeps track of distance parent and source for all nodes
            if v not in dist:           
                dist[v]   = dist[u] + 1
                parent[v] = u
                source[v] = source[u]
                q.append(v)

    return dist, parent, source

def attach_bfs_meta(G: nx.Graph, dist, parent, source):
    for v in G.nodes():
        if v in dist:
            G.nodes[v]["dist"] = int(dist[v])
            G.nodes[v]["source"] = str(source[v])
            G.nodes[v]["parent"] = str(parent[v]) if parent[v] is not None else "undefined"
        else:
            G.nodes[v]["dist"] = "undefined"
            G.nodes[v]["source"] = "undefined"
            G.nodes[v]["parent"] = "undefined"

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


def plot_graph(G, root):
    if len(root_nodes) < 1:
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
        plt.clf()
    
    else: 
        for root in n:
            #Isolated nodes list
            isolated_nodes = list(nx.isolates(G))

            #Connected nodes list
            connected_nodes = list([node for components in nx.connected_components(G) for node in components])


            #drawing the connected nodes first (default color)
            nx.draw_networkx_nodes(G, pos, nodelist=list(connected_nodes))
            #root node -> different color
            nx.draw_networkx_nodes(G, pos, nodelist=[str(root)], node_color='lightcoral', linewidths=3.0)
            #isolated node -> different color (red)
            nx.draw_networkx_nodes(G, pos, nodelist=isolated_nodes, node_color='lightcoral')

            #labeling the node number
            nx.draw_networkx_labels(G,pos, labels={node: node for node in G.nodes})
            #Highlighting BFS route
            setting_up_levels(G, pos, root)
            #Drawing all other edges in the graph
            nx.draw_networkx_edges(G, pos, edgelist=G.edges())

            plt.draw()
            #Specific save -> review later (need to change to pop up graphs)
            plt.show()
            #clear so doesn't clutter up the next graph
            plt.clf()

def random_color():
  return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def setting_up_levels(G, pos, root):

  #Compute BFS tree from root
  bfs_tree = nx.bfs_tree(G, str(root))

  #Shortest path from root
  path_dir = nx.single_source_shortest_path(G, str(root))

  #BFS level of each node
  level_dir = {}
  for node in path_dir:
    level_dir[node] = len(path_dir[node]) - 1

  #print(f"level_dir: {level_dir}")

  #Group edges of BFS tree by level
  level_edges = {}
  for edge in bfs_tree.edges():
    level_edge_check = level_dir[edge[1]]
    if level_edge_check not in level_edges:
      level_edges[level_edge_check] = []
    level_edges[level_edge_check].append(edge)

  #print(f"level_edges: {level_edges}")


  #level_edges -> ragged array to use for edgelist
  ragged_edge_array = [level_edges[level] for level in level_edges.keys()]
  row_in_ragged = []
  for list_level in level_edges:
    row_in_ragged.append(level_edges[list_level])

  #   print(f"ragged_edge_array: {ragged_edge_array}")
  #Iterate through and save the colors
  color_holder = []
  for indv_list in ragged_edge_array:
    #print(f"indv_list: {indv_list}")
    current_color = random_color()
    color_holder.append(current_color)
    nx.draw_networkx_edges(G, pos, edgelist=indv_list, edge_color=current_color, width=2.0)
  #print(f"color_holder: {color_holder}")




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
        type=str,
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
        analyze_components(G)
        analyze_cycles(G)
        analyze_isolates(G)
        analyze_density(G)
        analyze_avg_shortest_path(G)

    if args.plot and G:
        plot_graph(G, root_nodes)

    if args.output and G:
        dist, parent, source = compute_bfs_meta(G, args.multi_BFS)
        attach_bfs_meta(G, dist, parent, source)

        save_gml(G, args.output)
        

if __name__ == "__main__":
    main()
