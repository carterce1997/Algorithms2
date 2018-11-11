import numpy as np
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
def dfs(CapacityNetwork, FlowNetwork, S, T, maxPathFlow = sys.maxsize, curPath = None):
    if curPath is None:
        curPath = list()

    curPath = curPath.copy()

    # Insert the current node to the start of the curPath array.
    curPath.append(S)    
   
    # Check if the current node is the ending node (T node).
    if S == T:
        return curPath, maxPathFlow
    
    # Current node is not ending node. Continue to DFS through network.
    for dest in (FlowNetwork[S].keys() - curPath):
        # Find the flow from the current node (S) to next node (dest).
        possibleFlowToDest = CapacityNetwork[S][dest] - FlowNetwork[S][dest]
        if possibleFlowToDest > 0:
            # Update the min capacity.
            maxPathFlow = min(maxPathFlow, possibleFlowToDest)
            path, maxPathFlow = dfs(CapacityNetwork, FlowNetwork, dest, T, maxPathFlow, curPath)
            if path is not None:
                return path, maxPathFlow

    # Could not reach a path to T from this (S) node.
    return None, sys.maxsize

def FordFulkerson(CapacityNetwork, FlowNetwork, source, sink):
    augmentedPath, maxPathFlow = dfs(CapacityNetwork, FlowNetwork, source, sink)
    while augmentedPath is not None:
        # For each edge in augmentedPath
        for i in range( len(augmentedPath)-1 ):
            start = augmentedPath[i]
            end = augmentedPath[i+1]
            FlowNetwork[start][end] += maxPathFlow 

        print("Path: " + str(augmentedPath))
        print("maxPathFlow: " + str(maxPathFlow))
        print("Flow network: ")
        pprint(FlowNetwork)

        print("Capacity network: ")
        pprint(CapacityNetwork)
        print()

        augmentedPath, maxPathFlow = dfs(CapacityNetwork, FlowNetwork, source, sink)

    maxFlow = 0
    for dest in FlowNetwork[source].keys():
        maxFlow += FlowNetwork[source][dest]

    print("Max Flow = " + str(maxFlow))

    write_graph(FlowNetwork, outputFilename)



# READ GRAPH #
fileLines = []
with open(inputFilename, 'r') as inputFile:
    fileLines = inputFile.readlines()
    inputFile.close()

graphlines = []
for fileLine in fileLines:
    graphlines.append( fileLine.split() )

CapacityNetwork = defaultdict(dict)
FlowNetwork = defaultdict(dict)
for i in range( 1, len(graphlines)-2):
    source = int(graphlines[i][0])
    dest = int(graphlines[i][2])
    capacity = int(graphlines[i][3].split("\"")[1])
    # Initialize graph unchanged.
    CapacityNetwork[source].update({dest : capacity})

    # Create starting residual network.
    FlowNetwork[source].update({dest : 0})

CapacityNetwork = dict(CapacityNetwork)
FlowNetwork = dict(FlowNetwork)

S = int(graphlines[1][0])
T = int(graphlines[len(graphlines)-3][2])

FordFulkerson(CapacityNetwork, FlowNetwork, S, T)


#for u in Graph:
#    for v in Graph[u]:
#        print(v)
