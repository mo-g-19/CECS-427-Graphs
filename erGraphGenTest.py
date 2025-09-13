# copied example from https://networkx.org/documentation/stable/auto_examples/graph/plot_erdos_renyi.html
# Made some changes so i generates a random seed instead of the fixed seed

import time
import argparse
import matplotlib.pyplot as plt
import networkx as nx

n = 10  # 10 nodes
m = 20  # 20 edges
seed = int(time.time()) # changes made here

# Use seed for reproducibility
G = nx.gnm_random_graph(n, m, seed=seed)

# some properties
print("node degree clustering")
for v in nx.nodes(G):
    print(f"{v} {nx.degree(G, v)} {nx.clustering(G, v)}")

print()
print("the adjacency list")
for line in nx.generate_adjlist(G):
    print(line)

pos = nx.spring_layout(G, seed=seed)  # Seed for reproducible layout
nx.draw(G, pos=pos)
plt.show()