import time
import math
import argparse
import matplotlib.pyplot as plt
import networkx as nx


def create_random_graph(n: int, c: float):
    seed = int(time.time())
    p = (c * math.log(n)) / n                   #calculating the probablility based off the probablilty funtion in the assignment
    G = nx.erdos_renyi_graph(n, p, seed=seed)    #generating the graph
    return  G

def save_gml(G, path: str):
    nx.write_gml(G, path)
    print(f"Graph saved to {path}")


def multi_BFS(G, start_nodes: list[int]):
    print(f"multi_BFS called on G with start_nodes={start_nodes}")

#Using the notes from CECS 328 when created a BFS
def general_BFS(G, initial_node){
    final = []
    queue = []
    queue.append(initial_node)
    while queue is not empty:
        x = queue.pop()
        if (x is not in visited):
            visited.append(x)
        for every edge (x, y):
            if y is not in visited:
                queue.append(y)
}

# Main
# ====================================================================================================
def main():
    nodes = 20
    edge_creation = 0.5

    Graph = create_random_graph(nodes, edge_creation)
    Graph.add_nodes_from(list(n for n in Graph.nodes), visited=0)       #Instead of creating a visited array (which could make it O(n) if constantly searching through see if visited -> O(1) and an attribute) 0 -> not visited; 1 -> visited
    
    save_gml(Graph, "mo_analyze_graph.gml")

if __name__ == "__main__":
    main()


""" Next on agenda

def analyze_graph(G):
    print("analyze_graph called on G")


def plot_graph(G):
    seed = int(time.time())
    pos = nx.spring_layout(G, seed=seed)    #Honesly dont know what this does just copied this from the test code 
    nx.draw(G, pos=pos)                     #place holder anyway this whole funtion needs to be redone
    plt.show()

"""