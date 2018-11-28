import sys
from write_graph import write_graph
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
                    print(path)
                    return path + [end]
                else:
                    visited.add(node)
                    queue.append( (node, path + [node]) )
    return None


def FordFulkerson(ResidualNetwork, FlowGraph, source, sink):
    augmentedPath = BFS(ResidualNetwork, source, sink)
    while augmentedPath is not None:
        # Find the maximum possible flow on this path.
        bottleneckFlow = sys.maxsize
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

            print("start="+str(start) + "   end="+str(end))

            if start in FlowGraph.keys():
                FlowGraph[start][end] += bottleneckFlow
            else:
                FlowGraph[end][start] -= bottleneckFlow

        print("Path: " + str(augmentedPath))
        #print("bottleneckFlow: " + str(bottleneckFlow))
        #print("ResidualNetwork network: ")
        #pprint(ResidualNetwork)

        augmentedPath = BFS(ResidualNetwork, source, sink)

    maxFlow = 0
    for dest in FlowGraph[source].keys():
        maxFlow += FlowGraph[source][dest]

    print("Max Flow = " + str(maxFlow))

    write_graph(ResidualNetwork, outputFilename)



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

for i in range( 1, len(graphlines)-1):
    source = int(graphlines[i][0])
    dest = int(graphlines[i][2])
    capacity = int(graphlines[i][3].split("\"")[1])

    # Initialize graph unchanged.
    FlowGraph[source].update({dest : 0})

    # Create starting residual network.
    ResidualNetwork[source].update({dest : 0})
    ResidualNetwork[dest].update({source : 0})

for i in range( 1, len(graphlines)-1):
    source = int(graphlines[i][0])
    dest = int(graphlines[i][2])
    capacity = int(graphlines[i][3].split("\"")[1])

    # Create starting residual network.
    ResidualNetwork[source].update({dest : capacity})    

FlowGraph = dict(FlowGraph)
ResidualNetwork = dict(ResidualNetwork)

source = int(graphlines[1][0])
sink = int(graphlines[len(graphlines)-2][2])

for line in graphlines:
    print(line)

print(source)
print(sink)

FordFulkerson(ResidualNetwork, FlowGraph, source, sink)
pprint(FlowGraph)
print()
pprint(ResidualNetwork)
