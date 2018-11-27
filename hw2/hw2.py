import numpy as np
from compute_transitions import compute_transitions

# READ PROBLEM #
# read chain
with open('chain_ex.txt', 'r') as f:
    lines = f.readlines()
    f.close()

chain = []
for line in lines:
    subchain = []
    for p in line.split():
        subchain.append(float(p))
    if not subchain == []:
        chain.append(subchain)
chain = np.array(chain)
print('Transition matrix:')
print(chain)

# read probability of heads
with open('emit_ex.txt', 'r') as f:
    line = f.read()
    f.close()

emit = np.array(list(map(float, line.split())))
    
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
