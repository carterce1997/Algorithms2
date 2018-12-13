import numpy as np
from cvxopt import blas, lapack, solvers, matrix
from collections import defaultdict
import pygraphviz as pgv

# read graph into list
graph_file = 'graph.txt'

lines = []
with open(graph_file, 'r') as f:
    for line in f.readlines():
        lines.append(line.strip().strip(';'))

lines.pop(0) # graph{
lines.pop(-1) # }

pairs = []
for line in lines:
    splitted = line.split(' -- ')
    pairs.append((int(splitted[0]), int(splitted[1])))

# dump graph into dict structure
graph = defaultdict(set)
for pair in pairs:
    first, second = pair
    graph[first].add(second)
    graph[second].add(first)

# build adjacency matrix
w = np.zeros((len(graph), len(graph)))
for first in graph:
    for second in graph[first]:
        w[first-1, second-1] = 1

# I found this esoteric obfuscated code online
def mcsdp(w):
    """
    Returns solution x, z to

        (primal)  minimize    sum(x)
                  subject to  w + diag(x) >= 0

        (dual)    maximize    -tr(w*z)
                  subject to  diag(z) = 1
                              z >= 0.
    """

    n = w.size[0]
    c = matrix(1.0, (n,1))

    def G(x, y, alpha = 1.0, beta = 0.0, trans = 'N'):
        """
            y := alpha*(-diag(x)) + beta*y.
        """

        if trans=='N':
            # x is a vector; y is a symmetric matrix in column major order.
            y *= beta
            y[::n+1] -= alpha * x

        else:
            # x is a symmetric matrix in column major order; y is a vector.
            y *= beta
            y -= alpha * x[::n+1]


    def cngrnc(r, x, alpha = 1.0):
        """
        Congruence transformation

            x := alpha * r'*x*r.

        r and x are square matrices.
        """

        # Scale diagonal of x by 1/2.
        x[::n+1] *= 0.5

        # a := tril(x)*r
        a = +r
        tx = matrix(x, (n,n))
        blas.trmm(tx, a, side = 'L')

        # x := alpha*(a*r' + r*a')
        blas.syr2k(r, a, tx, trans = 'T', alpha = alpha)
        x[:] = tx[:]

    dims = {'l': 0, 'q': [], 's': [n]}

    def F(W):
        """
        Returns a function f(x, y, z) that solves

                      -diag(z)     = bx
            -diag(x) - r*r'*z*r*r' = bz

        where r = W['r'][0] = W['rti'][0]^{-T}.
        """

        rti = W['rti'][0]

        # t = rti*rti' as a nonsymmetric matrix.
        t = matrix(0.0, (n,n))
        blas.gemm(rti, rti, t, transB = 'T')

        # Cholesky factorization of tsq = t.*t.
        tsq = t**2
        lapack.potrf(tsq)

        def f(x, y, z):
            """
            On entry, x contains bx, y is empty, and z contains bz stored
            in column major order.
            On exit, they contain the solution, with z scaled
            (vec(r'*z*r) is returned instead of z).

            We first solve

               ((rti*rti') .* (rti*rti')) * x = bx - diag(t*bz*t)

            and take z = - rti' * (diag(x) + bz) * rti.
            """

            # tbst := t * bz * t
            tbst = +z
            cngrnc(t, tbst)

            # x := x - diag(tbst) = bx - diag(rti*rti' * bz * rti*rti')
            x -= tbst[::n+1]

            # x := (t.*t)^{-1} * x = (t.*t)^{-1} * (bx - diag(t*bz*t))
            lapack.potrs(tsq, x)

            # z := z + diag(x) = bz + diag(x)
            z[::n+1] += x

            # z := -vec(rti' * z * rti)
            #    = -vec(rti' * (diag(x) + bz) * rti
            cngrnc(rti, z, alpha = -1.0)

        return f

    sol = solvers.conelp(c, G, w[:], dims, kktsolver = F)
    return sol['x'], sol['z']

# solve SDP
n = w.shape[0]
soln = mcsdp(matrix(w))
x, z = soln[0], soln[1]

# Cholesky decompose solution matrix
z = np.reshape(z, (n, n))
v = np.linalg.cholesky(z).T

# generate random hyperplane
r = np.random.uniform(-1, 1, size = n)
r = r / np.sqrt(np.sum(np.square(r)))

# generate cut
solved_cut = np.sign(r.dot(v))

cut = defaultdict(set)
for i, val in enumerate(solved_cut):
    cut[val].add(i)

cut_edges = set()
for v in cut[1]:
    for u in graph[v]:
        if v < u:
            cut_edges.add((v, u))
        else:
            cut_edges.add((u, v))

cut_value = len(cut_edges)

print('Cut value:', cut_value)
print('Optimum Value:', - w.dot(z).trace() / 2)

# save graph cover
G = pgv.AGraph(graph_file)
for v in cut[1]:
    G.get_node(v).attr['color'] = 'red'

for e in cut_edges:
    u, v = e
    G.get_edge(u, v).attr['color'] = 'red'

G.draw(graph_file.split('.')[0] + '.png', prog = 'neato', args = '-Goverlap=scale')
