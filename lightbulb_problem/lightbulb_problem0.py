
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

edges = defaultdict(set)
edges_backwards = defaultdict(set)
for clause in clauses:
    (a, b) = clause
    edges[-a].add(b)
    edges[-b].add(a)

    edges_backwards[b].add(-a)
    edges_backwards[a].add(-b)
edges = dict(edges)

def dfs(graph, start, visited = None, finished = None):
    if visited is None:
        visited = set()
    if finished is None:
        finished = list()
    visited.add(start)
    for next in graph.get(start, set()) - visited:
        dfs(graph, next, visited, finished)
    finished.append(start)
    return visited, finished

# compute forward finishing times
visited = set()
finished = list()
for i in edges:
    visited, finished = dfs(edges, i, visited, finished)
    # if sps is not '':
        # print(sps)

# compute sccs backwards in reverse order of finishing time
visited_backwards = set()
sccs = []
while finished:
    node = finished.pop()
    if node not in visited_backwards:
        scc, _ = dfs(edges_backwards, node, set(), list())
        sccs.append(scc)
        visited_backwards.update(scc)

# find largest sccs (some are subcomponents)
largest_sccs = []
for scc in sccs:
    include_new = True
    for scc2 in largest_sccs:
        if scc < scc2:
            include_new = False

    if include_new:
        largest_sccs.append(scc)

    sccs_to_remove = []
    for scc2 in largest_sccs:
        if scc2 < scc:
            sccs_to_remove.append(scc2)

    for scc in sccs_to_remove:
        largest_sccs.remove(scc)

def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph.get(vertex, set()) - set(path):
            if next is goal:
                return path + [next]
            else:
                stack.append((next, path + [next]))

f = open(problem_name + '_output.txt', 'w')
for i in scc:
    if i in scc and -i in scc:
        f.writelines('Contradiction: ' + str(i) + ' -> ' + str(-i) + '\n')
        path = dfs_paths(edges, i, -i)
        path = ' -> '.join(list(map(str, path)))
        f.writelines(path)


# print(is_satisfied(clauses, largest_sccs[0]))


f.close()
