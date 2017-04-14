import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
import mmap
import time
import plotly.plotly as py
from scipy import sparse as sp
from plotly.graph_objs import *

"""
*** Goals ***
    Use plot_all only to start the create_adj function
    Use the youtube data base to load some specific periods of data
    read what happens during the period and make predictions on what is going to happen on the next periods
    pick a centrality measure
    implement directed and undirectedness for allison
    plot.ly 3d graphs and how to create the json file for what I am looking for (volume three web technologies 2 data serialization)
        dictio = {i: lista[i] for i in xrange(39)}
        import json
        import datetime
"""

def counter(filename):
    """
    Determines the number of nodes in the filename added
    """
    f = open(filename, "r+")
    buf = mmap.mmap(f.fileno(), 0)
    lines = 0
    readline = buf.readline
    while readline():
        lines += 1
    return lines

def loader(filename = "FB/facebook-wosn-links/out.facebook-wosn-links.txt", size = 0, timed_ = False, from_ = 1165708800, to_ = time.time()):
    """
    Inputs:
        Filename: Contains columns with first and second being source and target
            of the edge. It can contain weights and time of edge creation.
        Size: Number of lines to be read, number of edges to be taken into account.
        Timed: Are we taking into account a timed network?
        From: Epoch time of first node.
        To: Epoch time of last node.

    Outputs:
        An RXN array containing the edges of the given file. Rows are edges, co-
            lumns are source, target, weight, time respectively.

    * We are missing to do anything with the weight
    """
    # This part makes sure the entrance lines are cleared off.
    with open(filename) as myfile:
        head = [next(myfile) for x in xrange(5)]

    contador = 0
    for i in head:
        linea_head = i.strip().split(' ')
        if linea_head[0] == '%':
            contador += 1
        else:
            break

    this = counter(filename)

    # Number of Edges
    if size == False or size > this: # it makes sure that it either does the whole network or the size that you are looking for
        lines = this - contador #you can calculate the number of lines to ignore
    else:
        lines = size

    with open(filename, "r") as f:
        for i in xrange(contador):
            secon = next(f).strip().split(' ') # you are loosing your first line
        if timed_ == True:
            clear_mat = np.array([i.strip().split(' ') for i in f if int(i.strip().split(' ')[3])>from_ and int(i.strip().split(' ')[3]) < to_], int)
        else:
            clear_mat = np.array([next(f).strip().split(' ') for i in xrange(lines-contador+1)], int)

    return clear_mat

def create_adj(edges, plot_all = False, undirected = True):
    """
    Inputs:
        edges: column array containing the edges. It may contain extra info
            from weights and edge-stamp respectively (4 columns).
        plot_all: True- creates a matrix with a column/row for every node within
            the range, whether or not it is connected. False- It only creates a
            matrix with those nodes that are connected (degree centrality >=1).
        Undirected: True- makes the matrix to be symmetric. False- Makes a matrix
            that is not necessarily connected.

    Outputs:
        Returns a sparse lil_matrix representing the network.
    """
    m,n = np.shape(edges)

    if undirected == True:

        if plot_all == True:
            tam = max([max(edges[:,0]), max(edges[:,1])])
            adjacency = sp.lil_matrix((tam,tam))

            for i in xrange(m):
                adjacency[edges[i,0] - 1, edges[i,1] - 1] = 1.
                adjacency[edges[i,1] - 1, edges[i,0] - 1] = 1.

        elif plot_all == False:
            conjunto = set(edges[:,0]).union(edges[:,1])
            tam = len(conjunto)
            adjacency = sp.lil_matrix((tam,tam))
            listado = sorted(conjunto)

            for i in xrange(m):
                source = listado.index(edges[i,0])
                target = listado.index(edges[i,1])
                adjacency[source, target] = 1.
                adjacency[target, source] = 1.

    elif undirected == False:
        if plot_all == True:
            tam = max([max(edges[:,0]), max(edges[:,1])])
            adjacency = sp.lil_matrix((tam,tam))

            for i in xrange(m):
                adjacency[edges[i,0] - 1, edges[i,1] - 1] = 1.

        else:
            conjunto = set(edges[:,0]).union(edges[:,1])
            tam = len(conjunto)
            adjacency = sp.lil_matrix((tam,tam))
            listado = sorted(conjunto)

            for i in xrange(m):
                source = listado.index(edges[i,0])
                target = listado.index(edges[i,1])
                adjacency[source, target] = 1.

    return adjacency

def netx_plot(edges, plot_all = False, undirected = True, pos_ = False):
    """
    Inputs:
        edges: column array containing the edges. It may contain extra info
            from weights and edge-stamp respectively (4 columns).
        plot_all: True- creates a matrix with a column/row for every node within
            the range, whether or not it is connected. False- It only creates a
            matrix with those nodes that are connected (degree centrality >=1).
        undirected: True- makes the matrix to be symmetric. False- Makes a matrix
            that is not necessarily connected.

    Outputs:
        Plots a Networkx graph based on the conditions given.
    """

    if undirected:
        G = nx.Graph()
        if plot_all:
            tam = max([max(edges[:,0]), max(edges[:,1])])
            G.add_nodes_from(xrange(tam))
        G.add_edges_from(edges)
        bet_c = nx.betweenness_centrality(G)
        pos = nx.spring_layout(G, pos=pos_)
        nx.draw_networkx(G, pos=pos, with_labels=False, node_size=35, alpha=.7, node_color = bet_c.values(), width = .5,cmap=plt.cm.YlOrRd)
        plt.show()

    else:
        dG = nx.DiGraph()
        if plot_all:
            tam = max([max(edges[:,0]), max(edges[:,1])])
            dG.add_nodes_from(xrange(tam))
        dG.add_edges_from(edges)
        bet_c = nx.betweenness_centrality(dG)
        pos = nx.spring_layout(dG)
        nx.draw_networkx(dG, pos=pos, with_labels=False, node_size=35, alpha=.7, node_color = bet_c.values(), width = .5,cmap=plt.cm.YlOrRd)
        plt.show()

def plotly_3d():
    Edges = clear_mat
    G = ig.Graph(Edges, directed=False)

    layt = G.layout('kk', dim=3)
    N = num_of_nodes
    labels = listado

    Xn=[layt[k][0] for k in xrange(N)]# x-coordinates of nodes
    Yn=[layt[k][1] for k in xrange(N)]# y-coordinates
    Zn=[layt[k][2] for k in xrange(N)]# z-coordinates
    Xe=[]
    Ye=[]
    Ze=[]
    for e in Edges:
        Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
        Ye+=[layt[e[0]][1],layt[e[1]][1], None]
        Ze+=[layt[e[0]][2],layt[e[1]][2], None]

    trace1=Scatter3d(x=Xe,
                   y=Ye,
                   z=Ze,
                   mode='lines',
                   line=Line(color='rgb(125,125,125)', width=1),
                   hoverinfo='none'
                   )
    trace2=Scatter3d(x=Xn,
                   y=Yn,
                   z=Zn,
                   mode='markers',
                   name='actors',
                   marker=Marker(symbol='dot',
                                 size=6,
                                 color=group,
                                 colorscale='Viridis',
                                 line=Line(color='rgb(50,50,50)', width=0.5)
                                 ),
                   text=labels,
                   hoverinfo='text'
                   )
    axis=dict(showbackground=False,
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title=''
            )
    layout = Layout(
         title="Network of coappearances of characters in Victor Hugo's novel<br> Les Miserables (3D visualization)",
         width=1000,
         height=1000,
         showlegend=False,
         scene=Scene(
         xaxis=XAxis(axis),
         yaxis=YAxis(axis),
         zaxis=ZAxis(axis),
        ),
     margin=Margin(
        t=100
        ),
        hovermode='closest',
        annotations=Annotations([
           Annotation(
           showarrow=False,
            text="Data source: <a href='http://bost.ocks.org/mike/miserables/miserables.json'>[1]</a>",
            xref='paper',
            yref='paper',
            x=0,
            y=0.1,
            xanchor='left',
            yanchor='bottom',
            font=Font(
            size=14
            )
            )
        ]),    )

    data=Data([trace1, trace2])
    fig=Figure(data=data, layout=layout)

    py.iplot(fig, filename='Les-Miserables')

if __name__ == '__main__':
    # practice problems for the plotter
    edges = loader(filename = "subelj_euroroad/out.subelj_euroroad_euroroad.txt", size = 500)
    netx_plot(edges, undirected = False)
