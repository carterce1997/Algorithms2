import sys
from collections import defaultdict
from pprint import pprint 

inputFilename = sys.argv[1]
outputFilename = sys.argv[2]

# Example of ResidualNetwork will be a dictionary of type:
# { 
#   0: {1: 20, 2: 10}, 
#   1: {2: 10, 3: 10}, 
#   2: {3: 20}
# }
def BFS(ResidualNetwork, start, end):
    if start == end:
        return [start]

    # Create a queue for vertices and their shortest path to them.
    queue = [ (start, [start]) ]
    visited = set()
    # While the queue is not empty
    while queue:
        # Pop the first vertex and its path from the queue
        vertex, path = queue.pop(0)
        visited.add(vertex)
        # Iterate through this vertex's neighbors.
        for node in ResidualNetwork[vertex]:
            # Make sure that this edge's flow is > 0
            if ResidualNetwork[vertex][node] > 0 and node not in visited:
                if node == end:
                    return path + [end]
                else:
                    visited.add(node)
                    queue.append( (node, path + [node]) )
    return None

def findMinCut(ResidualNetwork, source):
    startCut = set()
    endCut = set()

    # All vertices lie in the residual network keys.
    for vertex in ResidualNetwork.keys():
        if BFS(ResidualNetwork, source, vertex) is not None:
            startCut.add(vertex)
        else:
            endCut.add(vertex)
    return startCut, endCut



def FordFulkerson(ResidualNetwork, FlowGraph, source, sink):
    augmentedPath = BFS(ResidualNetwork, source, sink)
    while augmentedPath is not None:
        # Find the maximum possible flow on this path.
        bottleneckFlow = ResidualNetwork[0][1]
        for i in range( len(augmentedPath)-1 ):
            start = augmentedPath[i]
            end = augmentedPath[i+1]
            bottleneckFlow = min(bottleneckFlow, ResidualNetwork[start][end])

        # For each edge in augmentedPath.
        for i in range( len(augmentedPath)-1 ):
            start = augmentedPath[i]
            end = augmentedPath[i+1]
            ResidualNetwork[start][end] -= bottleneckFlow 
            ResidualNetwork[end][start] += bottleneckFlow 
            
            # Check if edge is in input graph.
            if start in FlowGraph.keys():
                if end in FlowGraph[start].keys():
                    FlowGraph[start][end] += bottleneckFlow
                else:
                    print("ERROR")
            else:
                if start in FlowGraph[end].keys():
                    FlowGraph[end][start] -= bottleneckFlow
                else:
                    print("ERROR")

        # print("Path: " + str(augmentedPath))
        # print("bottleneckFlow: " + str(bottleneckFlow))
        # print("ResidualNetwork network: ")
        # pprint(ResidualNetwork)

        augmentedPath = BFS(ResidualNetwork, source, sink)

    maxFlow = 0
    for dest in FlowGraph[source].keys():
        maxFlow += FlowGraph[source][dest]

    print("Max Flow = " + str(maxFlow))


# READ GRAPH #
fileLines = []
with open(inputFilename, 'r') as inputFile:
    fileLines = inputFile.readlines()
    inputFile.close()

graphlines = []
for fileLine in fileLines:
    graphlines.append( fileLine.split() )

FlowGraph = defaultdict(dict)
ResidualNetwork = defaultdict(dict)

# Initialize all edges to 0.
for i in range( 1, len(graphlines)-2):
    source = int(graphlines[i][0])
    dest = int(graphlines[i][2])
    capacity = int(graphlines[i][3].split("\"")[1])

    # Initialize graph unchanged.
    FlowGraph[source].update({dest : 0})

    # Create starting residual network.
    ResidualNetwork[source].update({dest : 0})
    ResidualNetwork[dest].update({source : 0})

# Go back over all edges initializing residual graph.
for i in range( 1, len(graphlines)-2):
    source = int(graphlines[i][0])
    dest = int(graphlines[i][2])
    capacity = int(graphlines[i][3].split("\"")[1])

    # Create starting residual network.
    ResidualNetwork[source].update({dest : capacity})    

FlowGraph = dict(FlowGraph)
ResidualNetwork = dict(ResidualNetwork)

source = min(ResidualNetwork.keys())
sink = max(ResidualNetwork.keys())

# Find the max flow and the final residual graph.
FordFulkerson(ResidualNetwork, FlowGraph, 0, 199)

startCut, endCut = findMinCut(ResidualNetwork, source)
print("Start cut:")
print(startCut)
print()
print("End cut:")
print(endCut)