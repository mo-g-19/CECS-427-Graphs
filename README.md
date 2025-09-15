# Graphs Assignment CECS 427
## Mo Gibson
The goals of this assignment is to "advance your skills in **graph theory, algorithmic analysis, and professional software development**" through "Erdos-Renyi random graph generation, analysis, transformation, and visualization". Below is a quick summary of the submission instructions

## What this program is capabale of: 
- Generating and exporting Erdos-Renyi graphs
- Importing and analyzing graphs from .gml files
- Performing multi-source BFS with path tracking
- Identifying **connected components**
- Detecting **cycles and isolated nodes**
- Visualizing graphs with **annotated paths and substructures**
- Exporting computed metadata alongside the graphs

## Functional Requirements
Must implement Python script graph.py and command-line parameters -> corresponding operations below

### Command-Line Structure
'python ./graph.py [--input graph_file.gml] [--create_random_graph n c] [--multi_BFS a1 a2 ...] [--analyze] [--plot] [--output out_graph_file.gml]'

### Descriptons
- '--input graph_file.gml': reads a graph from given .gml file and uses for subsequent operations
- '--create_random_graph n c': Generate new Erdos-Renyi graph with n nodes and edge probability p = (c * ln(n) ) / n. Overrides '--input'. Nodes must be labeled with strings ("0", "1", "2",..,"n-1")
- '--nulti_BFS a1 a2 ...': accepts one or more starting nodes and computes BFS trees from each, storing all shortest paths. Each BFS tree must be independently visualized and compared
- '--analyze': perform additional structural analyses:
    - **Connected Components**: Count how many distinct connected subgraphs exist
    - **Cycle Detection**: Determine whether the graph contains any cycles
    - **Isolated Nodes**: Identify any nodes not connected to one another
    - **Graph Density**: Compute how dense the graph is (how many edges compared to the maximum possible)
    - **Average Shortest Path Legenth**: If graph is connected, computes the average number of steps along the shortest paths for all pairs of nodes.
- '--plot': Visualizes the plot with:
    - Highlighted shortest baths from each BFS root node
    - Distinct styling for isolated nodes
    - Optional visualization of individual connected components
- '--output out_graph_file.gml': Save the final graph, with all computed attributes to specified .gml file'

### Examples
'python ./graph.py --create_random_graph 200 1.5 --multi_BFS 0 5 20 --analyze --plot --output final_graph.gml'
Creates a 200-node graph, computes BFS trees from nodes 0, 5, and 20, performs full structural analysis, plots all findings, and saves the graph to final_graph.gml.

'python ./graph.py --input data.gml --analyze --plot'
Reads a pre-defined graph, analyzes its structure, and displays a visualization.

### Design Expectations
Use **Modular code strcture**, with seperate components for:
- Graph generation
- File I/O
- Graph algorithms (BFS, component detection, cycle detection)
- Visualization
- Argument parsing and orchestration
Implement **robust error handling**, including:
- File not found
- Malformed input graphs
- Invalid node IDs
- Insufficient parameters
**Document code thoroughly with function docstrings and comments**

## Submission Instructions:
A compressed archive (.zip or .tar.gz) containing:
- source code (graph.py)
- any additional modules (e.g. a utils/ directory)
- A README.md file containing:
    - Usage instructions
    - Description of your implementation
    - Examples of commands and outputs
    - Names and IDs of both team members
- A sample input .gml file and a corresponding output .gml file
- Screenshots of plotted graphs (optional but recommended)

# Student Side for Documentation
## Mo Gibson

## Usage Instructions

## Implementation Reasoning
- '--input graph_file.gml': uses the NetworkX Library to read the graph from the file path given and save it locally

- '--create_random_graph n c': Generate new Erdos-Renyi graph with n nodes and edge probability p = (c * ln(n) ) / n. Overrides '--input'. Nodes must be labeled with strings ("0", "1", "2",..,"n-1")

**Need
- '--multi_BFS a1 a2 ...': uses the NetworkX Library to return a ragged array of the BFS at root nodes a1, a2, and so on. The root nodes need

accepts one or more starting nodes and computes BFS trees from each, storing all shortest paths. Each BFS tree must be independently visualized and compared
- '--analyze': perform additional structural analyses:
    - **Connected Components**: Count how many distinct connected subgraphs exist
    - **Cycle Detection**: Determine whether the graph contains any cycles
    - **Isolated Nodes**: Identify any nodes not connected to one another
    - **Graph Density**: Compute how dense the graph is (how many edges compared to the maximum possible)
    - **Average Shortest Path Legenth**: If graph is connected, computes the average number of steps along the shortest paths for all pairs of nodes.
- '--plot': Visualizes the plot with:
    - Highlighted shortest baths from each BFS root node
    - Distinct styling for isolated nodes
    - Optional visualization of individual connected components
- '--output out_graph_file.gml': Save the final graph, with all computed attributes to specified .gml file'

## Examples of commands and outputs