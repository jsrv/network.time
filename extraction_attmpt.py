import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import mmap


def loader(filename = "subelj_euroroad/out.subelj_euroroad_euroroad.txt"):
    lines = counter(filename)
    text_file = open(filename, "r")
    text_raw = text_file.read()
    text_lines = text_raw.split('\n')
    # print lines
    # print text_lines
    clear_mat = np.zeros((lines-2,2))

    for i in xrange(lines-2):
        this = text_lines[i+2].split(' ')
        # print this
        clear_mat[i,0],clear_mat[i,1] = this[0],this[1]
    # print np.shape(clear_mat)
    return clear_mat.astype(int)

def create_adj():
    col_matrix = loader()

    m,n = np.shape(col_matrix)
    # print m,n
    adjacency = np.zeros((1174,1174))
    for i in xrange(m):
        print col_matrix[i,0],col_matrix[i,1]
        adjacency[col_matrix[i,0]-1,col_matrix[i,1]-1] = 1.
        adjacency[col_matrix[i,1]-1,col_matrix[i,0]-1] = 1.
    return adjacency

#attempt to only plot the connected nodes
def create_adj(filename = "FB/facebook-wosn-links/out.facebook-wosn-links.txt", size = 0, plot_all = False, undirected = True):
    col_matrix, nodes, edges = loader(filename, size)
    m,n = np.shape(col_matrix)

    if undirected == True:

        if plot_all == True:
            tam = max([max(col_matrix[:,0]), max(col_matrix[:,1])])
            adjacency = sp.lil_matrix((tam,tam))

            for i in xrange(tam):
                #print col_matrix[i,0],col_matrix[i,1]
                adjacency[col_matrix[i,0] - 1, col_matrix[i,1] - 1] = 1.
                adjacency[col_matrix[i,1] - 1, col_matrix[i,0] - 1] = 1.

        else:
            conjunto = set(col_matrix[:,0]).union(col_matrix[:,1])
            tam = len(conjunto)
            adjacency = sp.lil_matrix((tam,tam))
            listado = sorted(tam)

            for i in xrange(tam):
                source = listado.index(col_matrix[i,0])
                target = listado.index(col_matrix[i,1])
                adjacency[source, target] = 1.
                adjacency[target, source] = 1.

    elif undirected == False:
        return undirected

    return adjacency


def counter(filename):
    f = open(filename, "r+")
    buf = mmap.mmap(f.fileno(), 0)
    lines = 0
    readline = buf.readline
    while readline():
        lines += 1
    return lines

if __name__ == "__main__":
    b = create_adj()
    t = nx.from_numpy_matrix(b)
    nx.draw_networkx(t, with_labels=False, node_size=10,  alpha=.5,cmap=plt.cm.YlOrRd)
    plt.show()
