#Following code lines 2-7 from video https://www.youtube.com/watch?time_continue=37&v=7OdXry0T9Vg&embeds_referring_euri=https%3A%2F%2Fvideo.search.yahoo.com%2Fsearch%2Fvideo%3B_ylt%3DAwrOsH5opMRoPy0Ek0JXNyoA%3B_ylu%3DY29sbwNncTEEcG9zAzIEdnRpZAMEc2VjA3Nj%3Ftype%3DE210US1&embeds_referring_origin=https%3A%2F%2Fvideo.search.yahoo.com&source_ve_path=MzY4NDIsMzY4NDIsMjM4NTE
"""import xml.etree.ElementTree as etree

#Load the GML file
data = et.parse("HT.gml")
root = data.getroot()
print(root) #this whill print the root element of the GML file

#Same video; trying to extract the data from gml file
result = []
for el in root.iter():
    if el.tag = '{http://www.opengis.net/gml/3.2}posList':
        result.append{el.text}
print(result)       #This will print a list of coordinates

#Same video; to use XPath to filter coordinates by specific parent tags
xpath_query = './/{html://namespaces.os.uk/open/oml/1.0}Building//{http://www.opengis.net/gml/3.2}postList'

#Extract the coordinates
result = []
for el in root.findall(xpath_query):
    result.append(el.text)

print(result)       #This outputs the coordinates specifically from Building elements"""

import time
import argparse
import matplotlib.pyplot as plt
import networkx as nx

def multi_BFS(G, start_nodes: list[int]):
    print(f"multi_BFS called on G with start_nodes={start_nodes}")

#Using the notes from CECS 328 when created a BFS
def general_BFS(G, initial_node){
    visited = []
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
