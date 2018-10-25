import numpy as np
from collections import defaultdict

# Example of graph will be:
# { 
#   0: {1: 20, 2: 10}, 
#   1: {2: 10, 3: 10}, 
#   2: {3: 20}
# }
def dfs(Graph, S, T, visited = None):
    if visited is None:
        visited = list()
    if S == T:
        print(visited)
        return
    visited.append(S)    
    for dest in Graph[S]:
        capacity = Graph[S][dest]
        if dest not in visited:
            dfs(Graph, dest, T, visited)
    visited.remove(S)
    


# READ PROBLEM #
# read graph
fileLines = []
with open('graph1.txt', 'r') as inputFile:
    fileLines = inputFile.readlines()
    inputFile.close()

graphlines = []
for fileLine in fileLines:
    graphlines.append( fileLine.split() )

Graph = defaultdict(dict)
for i in range( 1, len(graphlines)-2):
    source = int(graphlines[i][0])
    dest = int(graphlines[i][2])
    capacity = int(graphlines[i][3].split("\"")[1])
    Graph[source].update({dest : capacity})
Graph = dict(Graph)

S = int(graphlines[1][0])
T = int(graphlines[len(graphlines)-3][2])

dfs(Graph, S, T)