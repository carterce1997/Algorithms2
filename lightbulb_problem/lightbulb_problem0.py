
import numpy as np # for easy randomization
import progressbar # for entertainment
import os.path
from collections import defaultdict

def read_circuit(filename):
    with open(filename) as f:
        lines = f.readlines()

    num_literals = int(lines.pop(0)) # pop front element - number of switches
    num_clauses = int(lines.pop(0)) # pop front again - number of bulbs

    clauses = []
    for line in lines:
        clause = line.split(' ') # split by space
        clause = tuple(map(int, clause)) # map string to int
        clauses.append(clause)

    return num_literals, num_clauses, clauses

def is_satisfied(clauses, literals):
    for clause in clauses:
        clause_satisfied = False
        for literal in literals:
            if literal in clause:
                clause_satisfied = True
                break
        if not clause_satisfied:
            return False
    return True

# read data
# filename = input('Problem specification file: ')
filename = 'ex1.txt'
problem_name = os.path.splitext(filename)[0]
num_literals, num_clauses, clauses = read_circuit(filename)

edges = defaultdict(list)
for clause in clauses:
    (a, b) = clause
    edges[-a].append(b)
    edges[-b].append(a)

print(edges)

with open('output.txt', 'w') as buff:
    visited_switches = []
    for x in range(1, num_literals + 1):
        xi = x
        buff.writelines(' '.join(['Switch', str(x), '\n\n']))
        while True:
            visited_switches.append(xi)
            next_switches = edges[xi]
            if -x in next_switches and x not in next_switches:
                print('contradiction')
                break # contradiction
            else:
                # pick a new switch to visit
                unvisited_switches = [s for s in next_switches if s not in visited_switches]
                buff.writelines(' '.join([str(xi), '->', str(unvisited_switches), '\n']))
                if unvisited_switches == []:
                    print('done')
                    buff.writelines('\n')
                    break
                else:
                    xi = unvisited_switches[0] # go to another switch
buff.close()

# save results
# with open(''.join([problem_name, '_results.txt']), 'w+') as f:
#     if circuit_satisfied:
#         print_literals = list(map(str, literals))
#         f.write('TRUE:\n')
#         f.writelines([l + '\n' for l in print_literals])
#     else:
#         f.write(' '.join(['FALSE: p >', str(1 - probability_threshold)]))
