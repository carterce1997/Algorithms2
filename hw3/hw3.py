import numpy as np

# READ PROBLEM #
# read graph
fileLines = []
with open('graph1.txt', 'r') as inputFile:
    fileLines = inputFile.readlines()
    inputFile.close()

graphlines = []
for fileLine in fileLines:
    graphlines.append( fileLine.split() )


for i in range( 1, len(graphlines)-2):
    print(graphlines[i])

