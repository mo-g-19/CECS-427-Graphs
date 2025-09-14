#Copying the example from https://networkx.org/documentation/stable/reference/readwrite/generated/networkx.readwrite.gml.generate_gml.html#networkx.readwrite.gml.generate_gml
#to see what happens
import networkx as nx

import time
import math
import argparse
import matplotlib.pyplot as plt
import networkx as nx

def load_gml(path: str):
    print(f"load_gml called with path={path}")
    Graph = nx.read_gml(path)
    return Graph

    #return "PLACEHOLDER"

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