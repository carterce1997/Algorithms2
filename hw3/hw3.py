import numpy as np
from collections import defaultdict

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
    Graph[source].update({dest : capacity});
Graph = dict(Graph)
print(Graph)
print(Graph[1])