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
def DFS(ResidualNetwork, source, sink, curPath = None, visited = set()):
    if curPath is None:
        curPath = list()
    
    # Insert the current node into the curPath.
    curPath.append(source)   

    key = str(curPath)

    print(str(curPath) + "       " + str(source)+ "       " + str(sink))

    visited.add(key)
    
    #print(curPath)
    #print()


    # Check if the current node is the ending node (T node).
    if source is sink:
        return curPath
    
    # Current node is not ending node. Continue to DFS through network.
    for dest in (ResidualNetwork[source].keys() - curPath):
        # Find the flow from the current node (S) to next node (dest).
        if ResidualNetwork[source][dest] > 0:
            path = DFS(ResidualNetwork, dest, sink, curPath, visited)
    
    # Could not reach a path to T from this (S) node.
    curPath.pop()


def FordFulkerson(ResidualNetwork, source, sink):
    DFS(ResidualNetwork, source, sink)




# READ GRAPH #
fileLines = []
with open(inputFilename, 'r') as inputFile:
    fileLines = inputFile.readlines()
    inputFile.close()

graphlines = []
for fileLine in fileLines:
    graphlines.append( fileLine.split() )

CapacityNetwork = defaultdict(dict)
ResidualNetwork = defaultdict(dict)

for i in range( 1, len(graphlines)-2):
    source = int(graphlines[i][0])
    dest = int(graphlines[i][2])
    capacity = int(graphlines[i][3].split("\"")[1])

    # Initialize graph unchanged.
    CapacityNetwork[source].update({dest : capacity})

    # Create starting residual network.
    ResidualNetwork[source].update({dest : capacity})
    ResidualNetwork[dest].update({source : 0})

CapacityNetwork = dict(CapacityNetwork)
ResidualNetwork = dict(ResidualNetwork)

source = int(graphlines[1][0])
sink = int(graphlines[len(graphlines)-3][2])

FordFulkerson(ResidualNetwork, source, sink)
