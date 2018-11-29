import numpy as np
from compute_transitions import compute_transitions

# READ IN PROBLEM #

# Read in transition matrix file.
lines = []
with open('chain_ex.txt', 'r') as file:
    lines = file.readlines()
    file.close()

# The transitionMatrix determines the probability of 
# the next coin based on the current coin. 
transitionMatrix = []
for line in lines:
    subchain = []
    for number in line.split():
        subchain.append(float(number))
    if not subchain == []:
        transitionMatrix.append(subchain)

transitionMatrix = np.array(transitionMatrix)
print('Transition matrix:')
print(transitionMatrix)

# Read emissions (the probability of heads for each coin).
with open('emit_ex.txt', 'r') as file:
    line = file.read()
    file.close()

emissions = np.array(list(map(float, line.split())))  
print('Emission matrix:', emissions)

# Read observed coin tosses.
with open('obs_ex.txt', 'r') as f:
    contents = f.read()
    f.close()

# 1 if heads, 0 if tails
coin_tosses = np.array(list(map(int, contents.split(' '))))
print('Coin tosses:', coin_tosses)

# ALGORITHMIC IMPLEMENTATION #
compute_transitions(coin_tosses, transitionMatrix, emissions)
