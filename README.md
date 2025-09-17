# Graphs Assignment CECS 427

### Command-Line Structure
'python ./graph.py [--input graph_file.gml] [--create_random_graph n c] [--multi_BFS a1 a2 ...] [--analyze] [--plot] [--output out_graph_file.gml][--show_components]'
# Student Side for Documentation
## Mo Gibson
## Philip Tran

## Usage Instructions
- '--input graph_file.gml': uses the NetworkX Library to read the graph from the file path given and save it locally

- '--create_random_graph n c': Generate new Erdos-Renyi graph with n nodes and edge probability p = (c * ln(n) ) / n. Overrides '--input'. Nodes must be labeled with strings ("0", "1", "2",..,"n-1")

- '--multi_BFS a1 a2 ...': uses the NetworkX Library to return a ragged array of the BFS at root nodes a1, a2, and so on. The root nodes must use inputs 0, 1, 2, ... n-1.

- '--analyze': perform additional structural analyses and printing it out including how many connected components exist, the isolated nodes of a graph (if there are any), if the graph has any cycles, the graph's density, and the average shortest path length

- '--plot': Creates a plot graph utalizing the Matplotlib Library, NetworkX Library, and helper functions draw_isolates, draw_default_nodes, draw_component_nodes, draw_edges, draw_labels, and draw_bfs to:
    - draw the isolated nodes in a distinct red color, and label each node with the corresponding the id
        - If '--multi_BFS' and  '--show_components' are not called: draw all edges and nodes in a default color
        - If '--multi_BFS' is called: Each edge is drawn in a specific color that correlates to the target node's level, and the adds the correlation to the legend
        - If '--show_components' is called draw the nodes of each separate component in a different color and add them to the legend

- '--output out_graph_file.gml': Save the final graph to the specified gml file path. Saves the node id, label, and the following metadata: Needs to be a .gml file.
    - If --multi_BFS is called: 
	    - source - to the closest root node 
	    - dist - computes the shortest path 
	    - parent - the node's parent . 
    - if --analyze is called: 
	    - num_components - the number of seperate components
	    - has_cycle - 1 is the graph has a cycle 0 otherwise
	    - density - the density of the graph
	    - avg_shortest_path - the average shortest distance of the graph 
	    - componentID - the id of the component the node is a part of
	    - isolate - is true if the node is an isolate false if it is not

- '--show_components': adds different coloring for separate components when called and adds them to the legend

## Implementation Reasoning

##### Architecture & modularity
A single file design was chosen in order to simplify the final submission and increase the ease of grading. however the design was kept modular for function reusability, minimize file size and increase readability. 

##### Multi-source BFS
When given an array of accepted node ids, our multi-source BFS function does both multiple individual BFS and (if --analyze is called) the closest root, the distance of the per-root shortest-path, and the parent of all nodes. If there are multiple roots with the same distance to the node, the root with the higher id number is chosen. For indiviual BFS, the NetworkX function single_source_shortest_path() is used to calculate the path in input root_node order and stored in a ragged array. It is then saved in a global variable in case it is needed for --plot. For multi-source BFS, all nodes have an "undefined" distance, in case they are isolated nodes. Then based on a calculated bfs queue, it loops through each node's distance from the root and parent, and only keeps the information from the shortest distance. Both parts has a complexity of O(R(V + E)) where R is the number of roots stated.
- If '--multi_BFS' is called: for each starting node in the list, create a ragged array where each row corresponds to a level, and the columns are the nodes corresponding to that level. Then draw each edge in a color that specifies the source node's level

#### Arg Parser
We implemented and arg parser to parse the arguments what were passed into the program. This was required and the only notable implantation was our addition of the -- show_components argument that was not included in the instructions. We chose to do this because the the instructions specify "Optional" visualization of individual connected components and given matplotlib does not have any toggle functionality we thought this was the best way to implement the optionality

##### Visualization
Many design choices were made here, for example in the case of visualizing the BFS we decided to use subplots in order to visualize all BFS paths at once instead of having them be graphed as a fill plot where you could only view one at a time. Also we chose to color the nodes instead of labeling them to increase visual readability. We also chose to use a gradient to choose the colors of the edge levels so that we did not have to hard code the colors. This has the added benefit of scalability in that nonmatter how many levels there are or if the number of levels differ from BFS to BFS in the same graph the correct colors will be assigned. Also isolates were chosen to be represented with a red border around the node 
##### Metadata
The metadata that we chose to add was the the data found in the --analyze as well as the data from the --multi_BFS. We chose only to include meta data that was either directly stated in the instructions or that was calculated for another function, because anymore would have been outside the scope of the assignment. 
##### Robustness & edge cases
The robustness was tested multiple ways to ensure the code will exit safely and print an error message if the users did not input in the correct format. We tested no --input or --create_random_graph, both an improper input and output file (that ends in something other than .gml), trying to take an input file that does not exist, trying to take a malformed input file, not enough requirements for --create_random_graph and --multi_BFS, and improper inputs for --create_random_graph (such as strings or doubles for the n value) and --multi_BFS (such as root node ids not existing).

There are a couple of edge cases for this file. Notably, larger graphs take a long time. This is due to choosing a spring_layout for rendering the graphs. The layout was chosen specifically so connected nodes are drawn closer together, the spacing allows for fewer overlaps/clutter, the same positioning 'seed' creates the same graph, and it is a very popular layout in NetworkX. This is also due to the time complexity of finding the shortest path in a multi-root per-root shortest path when calling --multi_BFS. However, this graph cleanly creates an all isolated nodes graph when c is 0, and when taking in all isolated nodes graph and the --output command, it reproduces the exact same graph.

## Examples of commands and outputs

python ./graph.py --create_random_graph 200 1.5 --multi_BFS 0 5 20 --analyze --plot --output final_graph.gml

![](Pasted%image%20250915210244.png)
![](Pasted%image%20250915210355.png)

python ./graph.py --input data.gml --analyze --plot
![](Pasted%image%20250915220116.png)
![](Pasted%image%20250915220157.png)

./graph.py --create_random_graph 20 1 --multi_BFS 0 5 10 --analyze --plot --output final_graph.gml --show_components
![](Pasted%image%20250916195823.png)
![](Pasted%image%20250916195852.png)