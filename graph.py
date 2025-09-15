from collections import deque
import time
import math
import argparse
from matplotlib.patches import Patch
import matplotlib.cm as cm
import matplotlib.colors as mcolors
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

def compute_component_ids(G: nx.Graph) -> dict:
    comp_id = {}
    for i, comp in enumerate(nx.connected_components(G)):
        for v in comp:
            comp_id[v] = i
    return comp_id

def attach_component_ids(G: nx.Graph, comp_id: dict):
    for v, cid in comp_id.items():
        G.nodes[v]["componentID"] = int(cid)

def compute_isolates(G: nx.Graph) -> list:
    return list(nx.isolates(G))

def attach_isolate_attr(G: nx.Graph, isolates: list):
    for v in G.nodes():
        if v in isolates:
            G.nodes[v]["isolate"] = "true"
        else:
            G.nodes[v]["isolate"] = "false"

def plot_graph(G, root_nodes):
    seed = 951369
    pos = nx.spring_layout(G, seed=seed)
    
    if len(root_nodes) < 1:

        #spliting the nodes into two groups isolated and non isolated
        isolates = set(nx.isolates(G))
        
        # creates a color map to give each component a diffrent color
        comp_id = compute_component_ids(G)
        unique_cids = sorted(set(comp_id.values()))

        max_cid = max(unique_cids, default=0)
        norm = mcolors.Normalize(vmin=0, vmax=max_cid)
        cmap = cm.tab20

        # draws all components in a diffrent color
        for cid in unique_cids:
            nodes = [v for v,c in comp_id.items() if c==cid]
            if nodes:
                nx.draw_networkx_nodes(
                    G, 
                    pos, 
                    nodelist=nodes, 
                    node_color=[cmap(cid)], 
                )
        
        # draws all isolates
        if isolates:
            nx.draw_networkx_nodes(
                G,
                pos,
                nodelist=isolates,
                node_color="none",
                edgecolors="red",
                linewidths=2.0
                )   
        
        # draw edges
        nx.draw_networkx_edges(
            G, 
            pos, 
            edge_color="lightgray", 
            width=4.0, 
            alpha=0.8
        )
        
        #its supposed to make the legend for components but it makes it for the isolates too isk what to do about that
        legend_handles = [
            Patch(facecolor=cmap(norm(cid)), edgecolor='black', label=f"Component {cid}")
            for cid in unique_cids
        ]
        plt.legend(handles=legend_handles, title="Connected Components", loc="best")
        
        # adds lables to the nodes not required i just added this in when i was verifying the graph will delete later
        nx.draw_networkx_labels(G, pos, labels={n: n for n in G.nodes()}, font_size=10)

        plt.show()
        plt.clf()
    
    else: 
        for root in root_nodes:
            #Isolated nodes list
            isolated_nodes = list(nx.isolates(G))

            #Connected nodes list
            connected_nodes = list([node for components in nx.connected_components(G) for node in components])

            #Compute BFS tree from root
            bfs_tree = nx.bfs_tree(G, str(root))
            bfs_edges = {tuple(sorted(e)) for e in bfs_tree.edges()}    #list of edges in the bfs
            all_edges = {tuple(sorted(e)) for e in G.edges()}           #list of all edges
            bg_edges  = list(all_edges - bfs_edges)                     #list of 
            
            #drawing the connected nodes first (default color)
            nx.draw_networkx_nodes(
                G, 
                pos, 
                nodelist=list(connected_nodes),
                node_color="paleturquoise",
            )
            #root node -> different color
            nx.draw_networkx_nodes(
                G, 
                pos, 
                nodelist=[str(root)], 
                node_color='purple', 
                linewidths=3.0
            )
            #isolated node -> different color (red)
            nx.draw_networkx_nodes(
                G, 
                pos, 
                nodelist=isolated_nodes, 
                node_color="none",
                edgecolors="red",
                linewidths=2.0
            )

            #labeling the node number
            nx.draw_networkx_labels(
                G,
                pos, 
                labels={node: node for node in G.nodes}
            )
            
            #Drawing all other edges in the graph
            nx.draw_networkx_edges(
                G, 
                pos, 
                edgelist=bg_edges, 
                edge_color="lightgray",
                width=4.0,
                alpha=0.5
            )
            
            #Highlighting BFS route
            setting_up_levels(G, pos, root, bfs_tree)

            plt.draw()
            #Specific save -> review later (need to change to pop up graphs)
            plt.show()
            #clear so doesn't clutter up the next graph
            plt.clf()


def setting_up_levels(G, pos, root, bfs_tree):

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
        
    #creates a color map for the amout of levels we have
    max_level = max(level_edges.keys(), default=1)
    norm = mcolors.Normalize(vmin=0, vmax=max_level)
    cmap = cm.viridis
    
    #   print(f"ragged_edge_array: {ragged_edge_array}")
    #Iterate through and save the colors
    for i, indv_list in enumerate(ragged_edge_array):
        #print(f"indv_list: {indv_list}")
        color = cmap(norm(i))
        nx.draw_networkx_edges(
            G, 
            pos, 
            edgelist=indv_list, 
            edge_color=[color], 
            width=4.0
        )
    #print(f"color_holder: {color_holder}")
    
    
    # creates the legend for the bfs edges
    legend_handles = [
        Patch(facecolor=cmap(norm(i)), edgecolor='black', label=f"Level {i}")
        for i in range(len(ragged_edge_array))
    ]
    plt.legend(handles=legend_handles, title="BFS Levels", loc="best")




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
        comp_id = compute_component_ids(G)
        attach_component_ids(G, comp_id)

        save_gml(G, args.output)
        

if __name__ == "__main__":
    main()
