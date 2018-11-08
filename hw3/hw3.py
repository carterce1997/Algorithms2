import numpy as np
import sys
from collections import defaultdict
from pprint import pprint 

filename = sys.argv[1]

# Example of graph will be:
# { 
#   0: {1: 20, 2: 10}, 
#   1: {2: 10, 3: 10}, 
#   2: {3: 20}
# }
def dfs(ResidualNetwork, S, T, minCapacity, curPath = None):
    if curPath is None:
        curPath = list()
    curPath.insert(0, S)    
    if S == T:
        return curPath
    for dest in ResidualNetwork[S]:
        curFlow = ResidualNetwork[S][dest]
        if curFlow > 0 and dest not in curPath:
            minCapacity[0] = min(minCapacity[0], curFlow)
            path = dfs(ResidualNetwork, dest, T, minCapacity, curPath)
            if path is not None:
                return path

    curPath.pop(0)            
    return None


def bfs(ResidualNetwork, S, T, minCapacity):
    visited, queue, tree = list(), [S], defaultdict(set)
    path = list()
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.append(node)
            for dest in ResidualNetwork[node]:
                if ResidualNetwork[node][dest] > 0 and dest not in visited:
                    minCapacity = min(minCapacity, ResidualNetwork[node, dest])
                    queue.append(dest)
                    tree[node].add(dest)
                    if dest == T:
                        visited.append(dest)
                        return visited[::-1] # return visited in reverse order
    

verbose = True
def FordFulkerson(Graph, ResidualNetwork, source, sink):
    maxFlow = 0
    minCapacity = [sys.maxsize]
    # augmentedPath = dfs(ResidualNetwork, source, sink, minCapacity)
    augmentedPath = bfs(ResidualNetwork, source, sink, minCapacity)
    while augmentedPath is not None:
        # For each edge in augmentedPath
        for i in range( len(augmentedPath)-1 ):
            start = augmentedPath[i]
            end = augmentedPath[i+1]
            ResidualNetwork[start][end] += minCapacity[0] 
            ResidualNetwork[end][start] -= minCapacity[0]             
            
        maxFlow += minCapacity[0]
        if verbose:
            print('Current max flow:', maxFlow)

            print("source: " + str(source) + "  sink: " + str(sink))
            print("Augmented path: " + str(augmentedPath))
            print("ResidualNetwork: " + str(ResidualNetwork))
            print()
        
        minCapacity = [sys.maxsize]
        # augmentedPath = dfs(ResidualNetwork, source, sink, minCapacity)
        augmentedPath = bfs(ResidualNetwork, source, sink, minCapacity)
    print("Max flow: " + str(maxFlow))
    pprint(ResidualNetwork)




# READ GRAPH #
fileLines = []
with open(filename, 'r') as inputFile:
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

#print("Before")
#print(Graph)
#print(ResidualNetwork)
#print()

FordFulkerson(Graph, ResidualNetwork, S, T)


#for u in Graph:
#    for v in Graph[u]:
#        print(v)
