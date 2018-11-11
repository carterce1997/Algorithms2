
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
filename = input('Problem specification file: ')
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

def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        print(path)
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))

bad_components = []
for component in sccs:
    for i in range(1, num_literals):
        if i in component and -i in component:
            bad_components.append(component)
            break

if len(bad_components) > 0:
    contradiction = True
else:
    contradiction = False
    solution = set()
    for component in reversed(sccs):
        include = True
        for i in component:
            if -i in solution:
                include = False
                break
        if include:
            solution = solution.union(component)



def write_satisfaction_proof(solution, clauses, problem_name):
    f = open(problem_name + '_output.txt', 'w')
    f.writelines('Given literals\n' + ' '.join(map(str, solution)) + '\n')
    f.writelines('We have that\n\n')
    for clause in clauses:
        for literal in solution:
            if literal in clause:
                line = str(clauses.index(clause) + 3)
                f.writelines(str(literal) + ' satisfies ' + str(clause) + ' on line ' + line + '.\n')
                break

    # we are happy
    f.writelines('\nSo the circuit is satisfiable.')
    f.close()

def write_contradiction_proof(components, clauses, problem_name):
    f = open(problem_name + '_output.txt', 'w')
    for component in components:
        for i in component:
            if -i in component:
                # forward
                f.writelines('Contradiction: ' + str(i) + ' -> ' + str(-i) + ' and ' + str(-i) + ' -> ' + str(i) + '\n\n')
                f.writelines('Proof:\n' + 'We will show that ' + str(i) + ' -> ' + str(-i) + '.\n')

                path = next(bfs_paths(graph, i, -i))
                for first, second in zip(path, path[1:]):
                    implication = str(first) + ' -> ' + str(second)
                    if (-first, second) in clauses:
                        reason = str((-first, second))
                        line_number = str(clauses.index((-first, second)) + 3)
                    elif (second, -first) in clauses:
                        reason = str((second, -first))
                        line_number = str(clauses.index((second, -first)) + 3)
                    else:
                        f.writelines('Error in proof!')
                        break
                    f.writelines('By ' + reason + ' on line ' + line_number + ', ' + implication + '.\n')

                # backward
                f.writelines('\nSo ' + str(i) + ' -> ' + str(-i) + '. We will now show that ' + str(-i) + ' -> ' + str(i) + '.\n')

                path = next(bfs_paths(graph, -i, i))
                for first, second in zip(path, path[1:]):
                    implication = str(first) + ' -> ' + str(second)
                    if (-first, second) in clauses:
                        reason = str((-first, second))
                        line_number = str(clauses.index((-first, second)) + 3)
                    elif (second, -first) in clauses:
                        reason = str((second, -first))
                        line_number = str(clauses.index((second, -first)) + 3)
                    else:
                        f.writelines('Error in proof!')
                        break
                    f.writelines('By ' + reason + ' on line ' + line_number + ', ' + implication + '.\n')

                # the unavoidable conclusion
                f.writelines('\nTherefore, the circuit is unsatisfiable.')
            return

if contradiction:
    write_contradiction_proof(bad_components, clauses, problem_name)
else:
    write_satisfaction_proof(solution, clauses, problem_name)
