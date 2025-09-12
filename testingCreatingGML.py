#Copying the example from https://networkx.org/documentation/stable/reference/readwrite/generated/networkx.readwrite.gml.generate_gml.html#networkx.readwrite.gml.generate_gml
#to see what happens

G = nx.Graph()
G.add_node("1")
print("\n".join(nx.generate_gml(G)))
graph [
  node [
    id 0
    label "1"
  ]
]
G = nx.MultiGraph([("a", "b"), ("a", "b")])
print("\n".join(nx.generate_gml(G)))
graph [
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
]