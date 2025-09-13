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
def general_BFS(G, initial_node_id):
    final = []
    queue = []
    queue.append(int(initial_node_id))
    while len(queue) > 0:
        print(f"queue: {queue}")
        x = queue.pop()
        print(f"current node: {x}")
        if not G.nodes[x]['visited']:
            print(f"current node visited: {G.nodes[x]['visited']}")
            G.nodes[x]['visited'] = True
            print(f"current node visited: {G.nodes[x]['visited']}")
            print()
            #nx.set_node_attributes(G, x, visited)
        for edge in G.edges(x):             #edge in (G.in_edges(x) + G.out_edges(x)):
        #every edge (x, y):
            print(f"edge for current node {x}: {edge[1]}")
            if not G.nodes[edge[1]]['visited']:
                queue.append(edge[1])
        print()
        final.append(x)
    return final


# Main
# ====================================================================================================
def main():
    nodes = 20
    edge_creation = 0.5

    Graph = create_random_graph(nodes, edge_creation)
    Graph.add_nodes_from(list(n for n in Graph.nodes), visited=False)       #Instead of creating a visited array (which could make it O(n) if constantly searching through see if visited -> O(1) and an attribute) 0 -> not visited; 1 -> visited
    #nx.set_node_attributes(Graph, False, "visited")     #https://stackoverflow.com/questions/54497929/networkx-setting-node-attributes-from-dataframe

    save_gml(Graph, "mo_analyze_graph.gml")

    potential_q = general_BFS(Graph, "1")
    print(potential_q)

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