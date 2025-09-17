"""
9/16/2025
This file was created by Mo Gibson and Philip Tran
Purpose: To take in graph files or make a random Erods-Renjy graph, find the BFS path of a set of root nodes, analyze graph features, plot the graph, and return a .gml graph file with additional graph or bfs data
"""

from collections import deque
import time
import math
import argparse
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import networkx as nx
import sys



# GML Set Up Functions 
# ====================================================================================================

"""To take in a graph .gml file, and check that the input ID values are ints
Input: either a local file with just the name, or the file's entire path
Output: the graph that corresponds to the the file name
"""
def load_gml(path: str):
    print(f"load_gml called with path={path}")
    Graph = nx.read_gml(path)

    for node in Graph.nodes():
        if node.isdigit() is False:
            raise ValueError(f"--input: node id {node} is not appropriate. Must be an int.")

    return Graph

"""To save a graph to a specific .gml file
Input: the output file name and a graph
Output:
"""
def save_gml(G, path: str):
    nx.write_gml(G, path)
    print(f"Graph saved to {path}")

"""To make a random Erdos-Renyi graph with a given number of nodes and edge probability liklihood
Input: The number of nodes in the graph (n: int) and the likilihood of edge probability (c: float)
Output: An Erdos-Renyi graph
"""
def create_random_graph(n: int, c: float):
    seed = int(time.time())
    p = (c * math.log(n)) / n                   #calculating the probablility based off the probablilty funtion in the assignment
    G = nx.erdos_renyi_graph(n, p, seed=seed)    #generating the graph
    
    mapping = {i: str(i) for i in G.nodes()}    #Making all the lables strings as per sinstructions
    G = nx.relabel_nodes(G, mapping)
    for v in G.nodes():
        G.nodes[v]["label"] = v
    return  G




# GML Metadata Functions 
# ====================================================================================================
"""For a given list of root nodes, return back the multi-source dictionaries for all node's shortest-path to a root node, which root node it was, and the parent of the node for that BFS path
Input: A graph and a list of root node ids
Output: Based on the shortest BFS path in the list of root nodes, dictionaries for all node's shortest-path to a root node, which root node it was, and the parent of the node for that BFS path
"""
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

"""To take the dictionaries of multi-source BFS from compute_bfs_meta, and add the data as attributes to the nodes in the graph.
    If the node isn't connected to any listed BFS, the attributes are undefined
Input: A graph and dictionaries for a previously defined list of root nodes the current node's shortest distance, the root node in that distance, and it's parent in that path
Output: 
"""
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

""" To create a dictionary where all the nodes in a subgraph of connected_components have the same value
Input: A graph
Output: A dictionary that groups nodes that are connected to each other with the same value
"""
def compute_component_ids(G: nx.Graph) -> dict:
    comp_id = {}
    for i, comp in enumerate(nx.connected_components(G)):
        for v in comp:
            comp_id[v] = i
    return comp_id

"""Save the information found in compute_component_ids as one of the node's attribute
Input: A graph and a dictionary where all the nodes connected to each other have the same value
Output: 
"""
def attach_component_ids(G: nx.Graph, comp_id: dict):
    for v, cid in comp_id.items():
        G.nodes[v]["componentID"] = int(cid)

""" Returns a list of isolated nodes
Input: A graph
Output: A list of isolated nodes' ids
"""
def compute_isolates(G: nx.Graph) -> list:
    return list(nx.isolates(G))

"""Add an attribute where if a node is isolated, it is true, and false if not.
Input: A graph and a list of the isolated nodes in that graph
Output: 
"""
def attach_isolate_attr(G: nx.Graph, isolates: list):
    for v in G.nodes():
        if v in isolates:
            G.nodes[v]["isolate"] = "true"
        else:
            G.nodes[v]["isolate"] = "false"

"""The following 4 functions are to add the meta data, specifically the number of components, whether the graph is a cycle, the graph density, and if a bfs is calculated previously, what the shortest distance is
"""
def attach_components_meta(G, num_comps):
    G.graph["num_components"] = num_comps

def attach_cycles_meta(G, is_cycle):
    G.graph["has_cycle"] = is_cycle

def attach_density_meta(G, density):
    G.graph["density"] = density

def attach_avg_shortest_path_meta(G, avg_len):
    G.graph["avg_shortest_path"] = avg_len if avg_len is not None else "undefined"
            
            
            
# BFS Functions
# ====================================================================================================
"""To list the BFS starting at one of the list of root_nodes given
Input: A graph and a list of root nodes
Output: A ragged array of BFS where the row corresponds to the root node list order
"""
def multi_BFS(G, start_nodes: list[str]):
    all_BFS = []
    for indv_node in start_nodes:
        indv_BFS = nx.single_source_shortest_path(G, indv_node)
        all_BFS.append(indv_BFS)
    return all_BFS




# Print Analysis Functions
# ====================================================================================================
"""To print out and return a list of connected nodes (nodes that have edges)
Input: A graph
Output: A list of all the connected components
"""
def analyze_components(G):
    num_comps = nx.number_connected_components(G)
    print("Number of connected components:", num_comps)
    return num_comps

"""To determine if a graph has a cycle or not
Input: A graph
Output: A true/false that corresponds to if it has a cycle or not
"""
def analyze_cycles(G):
    is_cycle = bool(not nx.is_forest(G))
    if is_cycle:
        print("This graph has a cycle.")
    else:
        print("This graph is acyclic (a forest).")
    return is_cycle

"""To see if a graph has any isolated nodes
Input: A graph
Output: 
"""
def analyze_isolates(G):
    isolates = list(nx.isolates(G))
    if isolates:
        print("Graph has isolated nodes:", isolates)
    else:
        print("No isolated nodes.")

"""To return the graph's density
Input: A graph
Output: A float that corresponds to the graph's density
"""
def analyze_density(G):
    density = nx.density(G)
    print("Density:", density)
    return density
    
"""If the graph does have edges, use the NetworkX function to see the average path length for the shortest distance between possible pairs (only if they are connected nodes)
Input: A graph
Output: 
"""
def analyze_avg_shortest_path(G):
    if nx.is_connected(G):
        avg_len = nx.average_shortest_path_length(G)
        print("Average shortest path length:", avg_len)
        return avg_len
    else:
        print("This graph is not connected; average shortest path length is undefined.")
    return None




# Plotting Helper Functions
# ====================================================================================================
"""Take all the isolate nodes and draw them in red to differentiate them
Input: A graph, the set positioning for the entire graph, and the axis for isolated nodes
Output: A matplot patch that is 2D containing the face color and edge color for a graph
"""
def draw_isolates(G, pos, ax):
    #spliting the nodes into two groups isolated and non isolated
    isolates = set(nx.isolates(G))
    
    # draws all isolates
    if isolates:
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=isolates,
            node_color="none",
            edgecolors="red",
            linewidths=2.0,
            ax=ax
            )   
    iso_handle = Patch(      # creating the legend handle for isolates
        facecolor="none",    # hollow fill
        edgecolor="red",     # red border
        linewidth=2.0,
        label="Isolates"
    )
    return iso_handle
        
"""When no BFS is called, draw all nodes the same color
"""
def draw_default_nodes(G, pos, ax):
    #drawing the connected nodes first (default color)
    nx.draw_networkx_nodes(
        G, 
        pos, 
        nodelist=G.nodes(),
        node_color="paleturquoise",
        ax=ax
    )

"""Take all the nodes that aren't isolated or the root and draw them in a soft color to differentiate them
Input: A graph, the set positioning for the entire graph, and the axis for isolated nodes
Output: A matplot patch that is 2D containing the face color and edge color for a graph
"""
def draw_component_nodes(G, pos, ax):
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
                ax=ax
            )
    
    #Draws Legend for components
    comp_handles  = [
    Patch(facecolor=cmap(norm(cid)), edgecolor='black', label=f"Component {cid}")
    for cid in unique_cids
    ]
    return comp_handles

"""Sets the color and dimension for all edges"""
def draw_edges(G, pos, ax):
#Drawing all edges in the graph
        nx.draw_networkx_edges(
            G, 
            pos, 
            edge_color="lightgray",
            width=4.0,
            alpha=0.7,
            ax=ax
        )

"""Sets the size and lable name for numbering all nodes"""
def draw_lables(G, pos, ax):
    #labeling the node number
    nx.draw_networkx_labels(
        G,
        pos, 
        labels={node: node for node in G.nodes},
        ax=ax
    )

"""Creating a ragged array where the row number corresponds to the level of the nodes inside the ragged array, and return the maximum number of levels
"""
def compute_all_BFS_level(G, root):
    #Compute BFS tree from root
    bfs_tree = nx.bfs_tree(G, str(root))

    #Shortest path from root
    path_dir = nx.single_source_shortest_path(G, str(root))

    #BFS level of each node
    level_dir = {}
    for node in path_dir:
        level_dir[node] = len(path_dir[node]) - 1


    #Group edges of BFS tree by level
    level_edges = {}
    for edge in bfs_tree.edges():
        level_edge_check = level_dir[edge[1]]
        if level_edge_check not in level_edges:
            level_edges[level_edge_check] = []
        level_edges[level_edge_check].append(edge)

    max_level = max(level_edges.keys(), default=1)

    #level_edges -> ragged array to use for edgelist
    ragged_edge_array = [level_edges[level] for level in level_edges.keys()]
    row_in_ragged = []
    for list_level in level_edges:
        row_in_ragged.append(level_edges[list_level])
    return ragged_edge_array, max_level

"""Takes the ragged array of levels and the maximum number of levels to create a BFS graph where an edge corresponds to the node's level for that specific root
"""
def draw_bfs(G, pos, root, ax):

    ragged_edge_array, max_level = compute_all_BFS_level(G, root)
        
    #creates a color map for the amout of levels we have
    norm = mcolors.Normalize(vmin=0, vmax=max_level)
    cmap = cm.hsv
    
    #Iterate through and save the colors
    for i, indv_list in enumerate(ragged_edge_array):
        color = cmap(norm(i))
        nx.draw_networkx_edges(
            G, 
            pos, 
            edgelist=indv_list, 
            edge_color=[color], 
            width=4.0,
            ax=ax
        )
    
    #root node -> different color
    nx.draw_networkx_nodes(
        G, 
        pos, 
        nodelist=[str(root)], 
        node_color='red', 
        linewidths=3.0,
        ax=ax
    )    
    
    # creates the legend for the bfs edges
    bfs_handles = [
        Line2D([0], [0], color=cmap(norm(i)), lw=3, label=f"Level {i}")
        for i in range(len(ragged_edge_array))
    ]
    return bfs_handles




# Plotting  Function
# ====================================================================================================
"""Takes all the helper functions to create either:
-if no bfs was called: the isolated nodes a different color and a regular graph with edges
-if bfs was previously called: create a graph for each root node, and the color of the edges corresponds to the node's bfs level
"""
def plot_graph(G, root_nodes, show_components):
    seed = 951369
    pos = nx.spring_layout(G, seed=seed)
    
    #if bfs isnt done and there are no roots
    if len(root_nodes) < 1:
        fig, ax = plt.subplots(1, 1, figsize=(7, 7))
        
        combined_handles = []
        #if show_components is called in the comand line
        if show_components:
            comp_handles = draw_component_nodes(G, pos, ax)
            combined_handles += comp_handles
        else:
            draw_default_nodes(G, pos, ax)
            
        iso_handle = draw_isolates(G, pos, ax)
        combined_handles.append(iso_handle)
        
        draw_edges(G, pos, ax)
                
        # adds lables to the nodes not required i just added this in when i was verifying the graph will delete later
        draw_lables(G, pos, ax)

        #combines all legend handles into one legend
        if combined_handles:
            ax.legend(handles=combined_handles, title="Legend", loc="best")
            
        plt.show()
        plt.clf()
    #if bfs is done and there are roots
    else: 
        # Make subplots: 1 row, N columns
        fig, axes = plt.subplots(1, len(root_nodes), figsize=(6 * len(root_nodes), 6))
        if len(root_nodes) == 1:
            axes = [axes]  # keep it iterable
        #loop to make a one sub plot per root
        for ax, root in zip(axes,root_nodes):
            #if show components was called in cmd line
            if show_components:
                comp_handles = draw_component_nodes(G, pos, ax)
            else:
                draw_default_nodes(G, pos, ax) 
            
            iso_handle = draw_isolates(G, pos, ax)
            draw_edges(G, pos, ax)
                                    
            #Highlighting BFS route
            bfs_handles = draw_bfs(G, pos, root, ax)
            
            draw_lables(G, pos, ax)
            
            ax.set_title(f"BFS from root {root}")
            
            #combines legend handles and outputs them to a single legend
            combined_handles = []
            if show_components and comp_handles:
                combined_handles += comp_handles
            combined_handles += bfs_handles
            combined_handles.append(iso_handle)  
            
            ax.legend(handles=combined_handles, title="Legend", loc="best")
            
        plt.tight_layout()
        plt.show()




# Arg Parser
# ====================================================================================================
"""To take all the arguments in the command line, save relevant information needed to compute the functions, and make some checks that it follows the input instructions
"""
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Graph CLI")

    #require that at least --input or --create_random_graph is called
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--input",
        type=argparse.FileType("r"),
        help="Path to input GML file"
        )
    parser.add_argument(
        "--output", 
        type=str,
        help="Path to output GML file"
        )

    group.add_argument(
        "--create_random_graph",
        nargs=2,
        metavar=("n", "c"),
        type=str,
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
    
    parser.add_argument(
    "--show_components",
    action="store_true",
    help="Shows Components as differently colored nodes",
    )


    return parser




# Main
# ====================================================================================================
"""Builds the parser, and calls the functions that correspond to said argument. It also checks for additional erros such as requiring a .gml file, ensuring that the input .gml file is properly made, the node ids are digits and within range, etc.
"""
def main():
    parser = build_parser()
    args = parser.parse_args()

    G = None            # local graph variable -> all functions
    root_nodes = []     # local root nodes variable -> made in multi_BFS, used in plot

    #ensure the paths (input and output end with .gml)
    if args.input and not args.input.name.endswith(".gml"):
        parser.error("--input file must be a .gml file")

    if args.output and not args.output.endswith(".gml"):
        parser.error("--output file must be a .gml file")


    #To figure out the different possible errors: https://pelegm-networkx.readthedocs.io/en/latest/_modules/networkx/readwrite/gml.html
    #NetworkXError:
    #ValueError:
    #   didn't apply a stringizer or destringizer when writting to the gml file pulling from
    #NetworkXError:
    #   input can't be parsed(value is not string with stringizer is None)
    #UnicodeDecodeError:
    #   type of NetworkXError where input isn't ASCII-encoded

    #Into regular calls
    if args.input:
        try:
            G = load_gml(args.input.name)
        except (nx.NetworkXError, ValueError, UnicodeDecodeError) as err:
            parser.error(f"--input: Malformed GML in {getattr(args.input, 'name', '<stdin>')}: {err}")

    if args.create_random_graph:
        #check that n is an int and c is a float/int
        if args.create_random_graph:
            raw_n, raw_c = args.create_random_graph

            try:
                n = int(raw_n)
            except ValueError:
                parser.error("--create_random_graph n: must be an int")
            if n <= 0:
                parser.error("--create_random_graph n: must be > 0")
            
            try:
                c = float(raw_c)
            except ValueError:
                parser.error("--create_random_graph c: must be a float or an int")
            if c < 0:
                parser.error("--create_random_graph c: not be < 0")

        G = create_random_graph(n, c)

    if args.multi_BFS is not None and len(args.multi_BFS) == 0:
        parser.error("--multi_BFS: require at least one root node")

    if args.multi_BFS and G:
        bad = []
        holder_for_n = G.number_of_nodes() - 1
        for node in args.multi_BFS:
            if not node.isdigit():
                parser.error(f"--multi_BFS {node!r} is not valid int node id (must be positive value)")
            node_val = int(node)
            if node_val > holder_for_n or node_val < 0:
                bad.append(node)
        if bad:
            parser.error(f"--multi_BFS contains out-of-range node ids: {bad}. Valid range is [0, {holder_for_n}]")

        root_nodes = args.multi_BFS
        all_BFS = multi_BFS(G, root_nodes)
        
        if args.analyze:
            dist, parent, source = compute_bfs_meta(G, args.multi_BFS)
            attach_bfs_meta(G, dist, parent, source)

    if args.analyze and G:
        attach_components_meta(G, analyze_components(G))
        comp_id = compute_component_ids(G)
        attach_component_ids(G, comp_id)

        attach_cycles_meta(G, analyze_cycles(G))

        analyze_isolates(G)
        isolates = compute_isolates(G)
        attach_isolate_attr(G, isolates)

        attach_density_meta(G, analyze_density(G))
        attach_avg_shortest_path_meta(G, analyze_avg_shortest_path(G))

    if args.plot and G:
        plot_graph(G, root_nodes, args.show_components)

    if args.output and G:
        save_gml(G, args.output)
        

if __name__ == "__main__":
    main()
