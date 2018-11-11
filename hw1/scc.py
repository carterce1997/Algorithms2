import os.path
from collections import defaultdict
import pprint

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
filename = 'example.txt'
problem_name = os.path.splitext(filename)[0]
num_literals, num_clauses, clauses = read_circuit(filename)

all_literals = [x for x in range(1, 1 + num_literals)]
all_literals.extend([-x for x in range(1, 1 + num_literals)])


graph = dict()
for literal in all_literals:
    graph[literal] = set()

for clause in clauses:
    (a, b) = clause
    graph[-a].add(b)
    graph[-b].add(a)

def transpose(graph):
    graph_transpose = dict()
    for literal in all_literals:
        graph_transpose[literal] = set()

    for start, neighbors in graph.items():
        for neighbor in neighbors:
            graph_transpose[neighbor].add(start)
    return graph_transpose


def dfs_visit(graph, start, finished, visited):
    visited.add(start)
    for vertex in graph[start] - visited:
        dfs_visit(graph, vertex, finished, visited)
    if start not in finished:
        finished.append(start)

def dfs(graph, finished = list()):
    visited = set()
    for vertex in graph:
        if vertex not in visited:
            dfs_visit(graph, vertex, finished, visited)
    return finished

def scc(graph):
    graph_transpose = transpose(graph)
    finished = dfs(graph)
    visited_scc = set()

    sccs = []
    while len(finished) > 0:
        start = finished[-1]
        finished_scc = list()
        dfs_visit(graph_transpose, start, finished_scc, visited_scc)
        for vertex in finished_scc:
            graph_transpose[vertex] = set()
            finished.remove(vertex)
        sccs.append(set(finished_scc))
    return sccs

sccs = scc(graph)
print(sccs)
