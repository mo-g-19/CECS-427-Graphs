#Copying the example from https://networkx.org/documentation/stable/reference/readwrite/generated/networkx.readwrite.gml.generate_gml.html#networkx.readwrite.gml.generate_gml
#to see what happens
import networkx as nx

import time
import math
import argparse
import matplotlib
#matplotlib.use("TKAgg")
import matplotlib.pyplot as plt
import networkx as nx

#Functions needed
#Shortest path per root
#   recently thought of alternative might be better: nx.bfs_tree
#               returns touples of edges which can turn into highlights
#
#   nx.single_source_shortest_path(): get the dictionary for shortest path
#   https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.unweighted.single_source_shortest_path.html
#   turn each path into edges
#       maybe a map: what did with fibonacci sequence
#       maybe a list: go backwards from farthest layer up,
#                     Another list -> set the colors for degrees of seperation (might be wrong track)
#                     Highest degree of seperation -> set max number of layers
#                     each hop between nodes -> different color
#                     List of nodes already visited
#                  Feels wayyy too complicated. Might need to rethink this one
#                  Could also use .bfs_tree(G, source) -> help
#                       Need to check, but if in strict order, could use a simple O(n) to change to a new color

#Isolated Nodes
#   nx.isolates():
#       find the degree of 0
#   https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw_networkx_nodes.html#networkx.drawing.nx_pylab.draw_networkx_nodes
#   standout nodes -> nx.draw_networkx_nodes -> different color

#Highlighting on plot
#   https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw.html
#   nx.draw(): base graph
#   https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw_networkx_edges.html#networkx.drawing.nx_pylab.draw_networkx_edges
#   nx.draw_networkx_edges(): overlay highlighted path edges
#                     also need to do a specific highlight to do shortest path

#Outline for needed testing
#Pull from mo_analyze_graph.gml
def load_gml(path: str):
    print(f"load_gml called with path={path}")
    Graph = nx.read_gml(path)
    return Graph


#Try out using nx.draw(G)
# Main
# ====================================================================================================
def main():
  G = load_gml("mo_load_gml.gml")
  roots = [1, 2]

  nx.draw(G, pos=nx.spring_layout(G))
  plt.draw()
  plt.savefig("bfs_visualization_mo_analyze.png", dpi=300)

if __name__ == "__main__":
    main()





















#from https://networkx.org/documentation/stable/reference/readwrite/generated/networkx.readwrite.gml.read_gml.html
"""def load_gml(path: str):
    print(f"load_gml called with path={path}")  
    Graph = nx.read_gml(path)
    return Graph

def save_gml(G, path: str):
    nx.write_gml(G, path)
    print(f"Graph saved to {path}")


# Main
# ====================================================================================================
def main():
    saved_graph = load_gml("mo_analyze_graph.gml")
    save_gml(saved_graph, "mo_load_gml.gml")
    #"mo_load_gml.gml"

if __name__ == "__main__":
    main()
"""
















"""G = nx.Graph()
G.add_node("1")
print("\n".join(nx.generate_gml(G)))"""
"""graph [
  node [
    id 0
    label "1"
  ]
]"""
"""G = nx.MultiGraph([("a", "b"), ("a", "b")])
print("\n".join(nx.generate_gml(G)))"""
"""graph [
  multigraph 1
  node [
    id 0
    label "a"
  ]
  node [
    id 1
    label "b"
  ]
  edge [
    source 0
    target 1
    key 0
  ]
  edge [
    source 0
    target 1
    key 1
  ]
]"""