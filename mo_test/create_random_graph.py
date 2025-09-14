import time
import math
import argparse
import numpy as np        #One I added
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
    all_BFS = []
    for indv_node in start_nodes:
        indv_BFS = nx.single_source_shortest_path(G, indv_node)
        #print(f"indv_BFS: {indv_BFS}")
        print(f"indv_BFS: {indv_BFS}")
        all_BFS.append(indv_BFS)
    return all_BFS

"""def multi_BFS(G, start_nodes: list[int]):
    print(f"multi_BFS called on G with start_nodes={start_nodes}")
    print()

    print(f"start_nodes len: {len(start_nodes)}")
    print(f"number of nodes: {G.number_of_nodes()}")
    print()


    final_BFS = []
    #np.zeros((len(start_nodes), (G.number_of_nodes())))
    #counter_BFS = 0

    G.add_nodes_from(list(n for n in G.nodes), visited=False)       #Instead of creating a visited array (which could make it O(n) if constantly searching through see if visited -> O(1) and an attribute) 0 -> not visited; 1 -> visited
    
    for node in start_nodes:
        final = []
        queue = []

        queue.append(node)

        while len(queue) > 0:
            print(f"queue: {queue}")
            current_node = queue.pop()
            print(f"current node: {current_node}")

            if not G.nodes[current_node]['visited']:
                print(f"current node visited: {G.nodes[current_node]['visited']}")
                G.nodes[current_node]['visited'] = True
                print(f"current node visited: {G.nodes[current_node]['visited']}")
                print()
                #nx.set_node_attributes(G, current_node, visited)

            for edge in G.edges(current_node):             #edge in (G.in_edges(current_node) + G.out_edges(current_node)):
            #every edge (current_node, y):
                print(f"edge for current node {current_node}: {edge[1]}")
                if not G.nodes[edge[1]]['visited']:
                    queue.append(edge[1])
            
            print()
            final.append(current_node)
            print(f"final: {final}")
            print()

        print(f"BFS for {node}: {final}")
        print()
        
        final_BFS.append(final)
        print(f"final_BFS: {final_BFS}")

        for visited_node in G:
            G.nodes[visited_node]['visited'] = False

    return final_BFS"""
    

#Using the notes from CECS 328 when created a BFS
def general_BFS(G, initial_node_id: int):
        final = []
        queue = []

        queue.append(initial_node_id)

        while len(queue) > 0:
            print(f"queue: {queue}")
            current_node = queue.pop()
            print(f"current node: {current_node}")

            if not G.nodes[current_node]['visited']:
                print(f"current node visited: {G.nodes[current_node]['visited']}")
                G.nodes[current_node]['visited'] = True
                print(f"current node visited: {G.nodes[current_node]['visited']}")
                print()
                #nx.set_node_attributes(G, x, visited)

            for edge in G.edges(current_node):             #edge in (G.in_edges(current_node) + G.out_edges(current_node)):
            #every edge (current_node, y):
                print(f"edge for current node {current_node}: {edge[1]}")
                if not G.nodes[edge[1]]['visited']:
                    queue.append(edge[1])
                    print(f"queue: {queue}")
                    print()

            print()
            print(f"final: {final}")
            print()
        return final

        """print()
        final.append(current_node)
        print(f"final: {final}")
        print()"""



# Main
# ====================================================================================================
def main():
    nodes = 8
    edge_creation = 3

    Graph = create_random_graph(nodes, edge_creation)
    
    #nx.set_node_attributes(Graph, False, "visited")     #https://stackoverflow.com/questions/54497929/networkx-setting-node-attributes-from-dataframe

    potential_q = multi_BFS(Graph, [1, 2])
    for indv_BFS in potential_q:
        print(indv_BFS)
    #print(potential_q)

    save_gml(Graph, "mo_analyze_graph.gml")

    """for list_order in potential_q[0].len():
        print(potential_q[-list_order])"""

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

"""
def multi_BFS(G, start_nodes: list[int]):
    print(f"multi_BFS called on G with start_nodes={start_nodes}")
    print()

    print(f"start_nodes len: {len(start_nodes)}")
    print(f"number of nodes: {G.number_of_nodes()}")
    print()


    final_BFS = []
    #np.zeros((len(start_nodes), (G.number_of_nodes())))
    #counter_BFS = 0

    G.add_nodes_from(list(n for n in G.nodes), visited=False)       #Instead of creating a visited array (which could make it O(n) if constantly searching through see if visited -> O(1) and an attribute) 0 -> not visited; 1 -> visited
    
    for node in start_nodes:
        final = general_BFS(G, node)

        print(f"BFS for {node}: {final}")
        print()
        
        for visited_node in G:
            G.nodes[visited_node]['visited'] = False

        final_BFS.append(final)
        print(f"final_BFS: {final_BFS}")

        
    return final_BFS
    

#Using the notes from CECS 328 when created a BFS
def general_BFS(G, initial_node_id: int):
        final = []
        queue = []

        queue.append(initial_node_id)

        while len(queue) > 0:
            print(f"queue: {queue}")
            current_node = queue.pop()
            print(f"current node: {current_node}")

            if not G.nodes[current_node]['visited']:
                print(f"current node visited: {G.nodes[current_node]['visited']}")
                G.nodes[current_node]['visited'] = True
                print(f"current node visited: {G.nodes[current_node]['visited']}")
                print()
                #nx.set_node_attributes(G, x, visited)

            for edge in G.edges(current_node):             #edge in (G.in_edges(current_node) + G.out_edges(current_node)):
            #every edge (current_node, y):
                print(f"edge for current node {current_node}: {edge[1]}")
                if not G.nodes[edge[1]]['visited']:
                    queue.append(edge[1])
                    print(f"queue: {queue}")
                    print()

            print()
            print(f"final: {final}")
            print()
        return final

""        print()
        final.append(current_node)
        print(f"final: {final}")
        print()"""
