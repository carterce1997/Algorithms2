
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

# dump clauses into a graph
graph = defaultdict(set)
graph_backwards = defaultdict(set)
for clause in clauses:
    (a, b) = clause
    graph[-a].add(b)
    graph[-b].add(a)

    graph_backwards[b].add(-a)
    graph_backwards[a].add(-b)
graph = dict(graph)
graph_backwards = dict(graph_backwards)

def dfs(graph, start, visited = None, finished = None):
    if visited is None:
        visited = set()
    if finished is None:
        finished = list()
    visited.add(start)
    for next_ in graph.get(start, set()) - visited:
        dfs(graph, next_, visited, finished)
    finished.append(start)
    return visited, finished

# compute forward finishing times
visited = set()
finished = list()
for i in graph:
    visited, finished = dfs(graph, i, visited, finished)

# compute sccs backwards in reverse order of finishing time
visited_backwards = set()
sccs = []
for node in reversed(finished):
    if node not in visited_backwards:
        scc, _ = dfs(graph_backwards, node, set(), list())
        sccs.append(scc)
        visited_backwards.update(scc)

def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next_ in graph.get(vertex, set()) - set(path):
            if next_ is goal:
                yield path + [next_]
            else:
                stack.append((next_, path + [next_]))

def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next_ in graph.get(vertex, set()) - set(path):
            if next_ is goal:
                yield path + [next_]
            else:
                queue.append((next_, path + [next_]))

def bfs(graph, start):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph.get(vertex, set()) - visited)
    return visited

# determine if a contradiction exists
f = open(problem_name + '_output.txt', 'w')
contradiction = False
for scc in sorted(sccs, key=len):
    if contradiction:
        break
    for i in scc:
        if i in scc and -i in scc:
            contradiction = True

            print('Searching for path ' + str(i) + ' -> ' + str(-i))
            # i -> -i
            f.writelines('Contradiction: ' + str(i) + ' -> ' + str(-i) + ' and ' + str(-i) + ' -> ' + str(i) + '\n\n')
            
            f.writelines('Proof:\n' + 'We will show that ' + str(i) + ' -> ' + str(-i) + '.\n')
            
            path = next(dfs_paths(graph, i, -i))
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
            
            
            f.writelines('\nSo ' + str(i) + ' -> ' + str(-i) + '. We will now show that ' + str(-i) + ' -> ' + str(i) + '.\n')

            print('Searching for path ' + str(-i) + ' -> ' + str(i))
            # -i -> i
            print(bfs(graph, -i))

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
            break

# otherwise, provide a satisfying example
if not contradiction:
    solution = sorted(sccs, key=len)[0]
    f.writelines('Given literals\n' + '\n'.join(map(str, solution)) + '\n')
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
