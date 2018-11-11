import numpy as np
import sys
from write_graph import write_graph
from collections import defaultdict
from pprint import pprint 

inputFilename = sys.argv[1]
outputFilename = sys.argv[2]

# minCapacity is an array of size 1 because this value needs to be passed by reference.
# Example of ResidualNetwork will be a dictionary of type:
# { 
#   0: {1: 20, 2: 10}, 
#   1: {2: 10, 3: 10}, 
#   2: {3: 20}
# }
def dfs(ResidualNetwork, S, T, minCapacity, curPath = None, i = 0):
    if curPath is None:
        curPath = list()

    # Insert the current node to the start of the curPath array.
    curPath = curPath.copy()
    curPath.insert(0, S)    
    #print("Inside DFS: " + str(curPath))
    #print("minCapacity: " + str(minCapacity) + "   i: " + str(i) + "   S: " +  str(S) + "   T: " + str(T) + "   len(curPath): " + str(len(curPath)))

    # Check if the current node is the ending node (T node).
    if S == T:
        return curPath, minCapacity
    
    # Current node is not ending node. Continue to DFS through network.
    for dest in (ResidualNetwork[S].keys() - curPath):
        # Find the flow from the current node (S) to next node (dest).
        curFlow = ResidualNetwork[S][dest]
        if curFlow > 0:
            # Update the min capacity.
            minCapacity = min(minCapacity, curFlow)
            path, minCapacity = dfs(ResidualNetwork, dest, T, minCapacity, curPath, i+1)
            if path is not None:
                return path, minCapacity

    # Could not reach a path to T from this (S) node. Remove S from the current path. 
    print("NONE" + str(i))
    return None, sys.maxsize

def FordFulkerson(Graph, ResidualNetwork, source, sink):
    maxFlow = 0
    minCapacity = sys.maxsize
    augmentedPath, minCapacity = dfs(ResidualNetwork, source, sink, minCapacity)

    while augmentedPath is not None:
        #print("augmentedPathCheck: " + str(augmentedPath))

        # For each edge in augmentedPath
        for i in range( len(augmentedPath)-1 ):
            start = augmentedPath[i]
            end = augmentedPath[i+1]
            ResidualNetwork[start][end] += minCapacity 
            ResidualNetwork[end][start] -= minCapacity            

        maxFlow += minCapacity
       # print('Maximizing flow of', maxFlow, 'on path', str(augmentedPath))
        
        augmentedPath, minCapacity = dfs(ResidualNetwork, source, sink, sys.maxsize)

    print("Max flow: " + str(maxFlow))
    pprint(ResidualNetwork)
    write_graph(ResidualNetwork, outputFilename)



# READ GRAPH #
fileLines = []
with open(inputFilename, 'r') as inputFile:
    fileLines = inputFile.readlines()
    inputFile.close()

graphlines = []
for fileLine in fileLines:
    graphlines.append( fileLine.split() )

Graph = defaultdict(dict)
ResidualNetwork = defaultdict(dict)
for i in range( 1, len(graphlines)-2):
    source = int(graphlines[i][0])
    dest = int(graphlines[i][2])
    capacity = int(graphlines[i][3].split("\"")[1])
    # Initialize graph unchanged.
    Graph[source].update({dest : capacity})

    # Create starting residual network.
    ResidualNetwork[source].update({dest : capacity})
    ResidualNetwork[dest].update({source : 0})

ResidualNetwork = dict(ResidualNetwork)
Graph = dict(Graph)

S = int(graphlines[1][0])
T = int(graphlines[len(graphlines)-3][2])

#print(len(ResidualNetwork))

#print("Before")
#print(Graph)
#print(ResidualNetwork)
#print()

FordFulkerson(Graph, ResidualNetwork, S, T)


#for u in Graph:
#    for v in Graph[u]:
#        print(v)
