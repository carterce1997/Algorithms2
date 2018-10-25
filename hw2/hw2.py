import numpy as np
from compute_transitions import compute_transitions

# READ PROBLEM #
# read chain
with open('chain_ex.txt', 'r') as f:
    lines = f.readlines()
    f.close()

chain = np.zeros((2,2))
for row, line in enumerate(lines):
    for col, p in enumerate(line.split()):
        chain[row, col] = float(p)
print('Transition matrix:', chain)

# read probability of heads
with open('emit_ex.txt', 'r') as f:
    line = f.read()
    f.close()

emit = np.zeros((2,2))
for col, p in enumerate(line.split()):
    emit[0, col] = float(p)
    emit[1, col] = 1 - float(p)
    
print('Emission matrix:', emit)

# read coin tosses
with open('obs_ex.txt', 'r') as f:
    contents = f.read()
    f.close()

# 1 if heads, 0 if tails
coin_tosses = np.array(list(map(int, contents.split(' '))))
print('Coin tosses:', coin_tosses)

# ALGORITHMIC IMPLEMENTATION #
compute_transitions(coin_tosses, chain, emit)
