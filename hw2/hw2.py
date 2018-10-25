import numpy as np


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

prob_heads = np.array([float(p) for p in line.split(' ')])
print('Probability of heads:', prob_heads)

# read coin tosses
with open('coin_tosses.txt', 'r') as f:
    contents = f.read()
    f.close()

coin_tosses = np.array(list(contents.strip()))
print('Coin tosses:', coin_tosses)


