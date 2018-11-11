
def write_graph(graph,fname):

    with open(fname, 'w') as f:
        f.write("digraph {\n")
        for i in graph:
            for j in graph[i]:
                phrase = '\t' + str(i) + ' -> ' + str(j) + ' [label="' + str(graph[i][j]) + '"];' + '\n'
                f.write(str(phrase))
        f.write("}")
        
        f.close()


