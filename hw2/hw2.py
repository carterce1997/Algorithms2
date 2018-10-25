import numpy as np

# READ PROBLEM #
# read transition matrix
with open('transition_matrix.txt', 'r') as f:
    lines = f.readlines()
    f.close()

transition_matrix = np.zeros((2,2))
for row, line in enumerate(lines):
    for col, p in enumerate(line.split(' ')):
        transition_matrix[row, col] = float(p)
print('Transition matrix:', transition_matrix)

# read probability of heads
with open('prob_heads.txt', 'r') as f:
    line = f.read()
    f.close()

emission_matrix = np.zeros((2,2))
for row, p in enumerate(line.split(' ')):
    emission_matrix[row, 0] = float(p)
    emission_matrix[row, 1] = 1 - float(p)
    
print('Emission matrix:', emission_matrix)

# read coin tosses
with open('coin_tosses.txt', 'r') as f:
    contents = f.read()
    f.close()

coin_tosses = np.array(list(contents.strip()))
print('Coin tosses:', coin_tosses)

# ALGORITHMIC IMPLEMENTATION #
