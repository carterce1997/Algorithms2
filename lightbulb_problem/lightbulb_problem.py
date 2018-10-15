
import numpy as np # for easy randomization
import progressbar # for entertainment
import os.path

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
filename = input('Problem specification file: ')
verbose = input('Verbose? [y/n]: ')
problem_name = os.path.splitext(filename)[0]
num_literals, num_clauses, clauses = read_circuit(filename)

# attempt solution
probability_threshold = .025
num_iter = int(num_literals ** 2 / probability_threshold)

circuit_satisfied = False
literals = np.multiply(np.arange(1, 1 + num_literals), np.random.choice([1,-1], size = num_literals))
for iteration in progressbar.progressbar(range(num_iter)):
    if verbose is 'y':
        print(literals)
    if is_satisfied(clauses, literals): # if satisfied, report
        circuit_satisfied = True
        print('Circuit satisfied!')
        break
    else:
        random_literal = np.random.randint(0, num_literals)
        literals[random_literal] *= -1 # else flip a random switch

if not circuit_satisfied:
    print('Unsatisfiable with probability greater than', 1 - probability_threshold)

# save results
with open(''.join([problem_name, '_results.txt']), 'w+') as f:
    if circuit_satisfied:
        print_literals = list(map(str, literals))
        f.write('TRUE:\n')
        f.writelines([l + '\n' for l in print_literals])
    else:
        f.write(' '.join(['FALSE: p >', str(1 - probability_threshold)]))
