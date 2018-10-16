
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
filename = 'ex2.txt'
problem_name = os.path.splitext(filename)[0]
num_literals, num_clauses, clauses = read_circuit(filename)

edges = defaultdict(list)
edges_backwards = defaultdict(list)
for clause in clauses:
    (a, b) = clause
    edges[-a].append(b)
    edges[-b].append(a)

    edges_backwards[b].append(-a)
    edges_backwards[a].append(-b)

def dfs(graph, node, visited, finished):
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            visited, finished = dfs(graph, n, visited, finished)
        finished.append(node)
    return visited, finished

# compute forward finishing times
all_literals = [i for i in range(1, 1 + num_literals)]
all_literals.extend([-i for i in range(1, 1 + num_literals)])
visited = []
finished = []
for i in all_literals:
    visited, finished = dfs(edges, i, visited, finished)

# compute sccs backwards in reverse order of finishing time
visited_backwards = []
sccs = []
while finished:
    node = finished.pop(-1)
    if node not in visited_backwards:
        scc, _ = dfs(edges_backwards, node, [], [])
        sccs.append(scc)
        visited_backwards.extend(scc)

print([len(x) for x in sccs])

# i = 1
# all_literals = [i for i in range(1, num_literals + 1)]
# dfs_order = dict()
# visited = []
# while True:
#     visited = dfs(edges, i, visited)
#     dfs_order[i] = visited
#     unvisited = [i for i in all_literals if i not in visited]
#     if len(unvisited) == 0:
#         break
#     else:
#         i = min(unvisited)
#
# print(dfs_order)

# buff = open('output.txt', 'w')
# for x in range(1, num_literals + 1):
#     visited_switches = []
#     xi = x
#     buff.writelines(' '.join(['Switch', str(x), '\n\n']))
#     while True:
#         visited_switches.append(xi)
#         next_switches = [s for s in edges[xi] if s not in visited_switches]
#         buff.writelines(' '.join([str(xi), '->', str(next_switches), '\n']))
#         if next_switches == [-x]:
#             raise StopIteration
#         else:
#             if next_switches == []:
#                 buff.writelines('\n')
#                 break
#             else:
#                 xi = next_switches[0] # go to another switch
# buff.close()

# save results
# with open(''.join([problem_name, '_results.txt']), 'w+') as f:
#     if circuit_satisfied:
#         print_literals = list(map(str, literals))
#         f.write('TRUE:\n')
#         f.writelines([l + '\n' for l in print_literals])
#     else:
#         f.write(' '.join(['FALSE: p >', str(1 - probability_threshold)]))
