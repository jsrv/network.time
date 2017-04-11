import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
# import pandas as pd
# from matplotlib.widgets import Slider, Button, RadioButtons
import mmap
from scipy import sparse as sp
import time
import plotly.plotly as py
from plotly.graph_objs import *

def counter(filename):
    f = open(filename, "r+")
    buf = mmap.mmap(f.fileno(), 0)
    lines = 0
    readline = buf.readline
    while readline():
        lines += 1
    return lines


    # Use plot_all only to start the create_adj function
    # Use the youtube data base to load some specific periods of data
    # read what happens during the period and make predictions on what is going to happen on the next periods
    # pick a centrality measure
    # implement directed and undirectedness for allison
    # plot.ly 3d graphs and how to create the json file for what I am looking for (volume three web technologies 2 data serialization)
        # dictio = {i: lista[i] for i in xrange(39)}
        # import json
        # import datetime



# It loads a text file and creates a numpy array that has the edges stored
# you can determine the number of edges you want to load into the array
def loader(filename = "FB/facebook-wosn-links/out.facebook-wosn-links.txt", size = 0, from_ = 1165708801, to_ = time.time()):
    # print "From :", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(from_))
    # print "to :",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(to_))

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
        clear_mat = np.array([next(f).strip().split(' ') for i in xrange(lines-contador+1)], int)

        # clear_mat = np.array([i.strip().split(' ') for i in f if int(i.strip().split(' ')[3])>from_ and int(i.strip().split(' ')[3]) < to_], int)

    if contador == 2:
        nodes = int(secon[2]) #Get the nodes by means of sometimes
    else:
        nodes = 0

    return clear_mat


# def create_adj(filename = "FB/facebook-wosn-links/out.facebook-wosn-links.txt", size = 0, plot_all = False):
#     col_matrix, nodes, edges = loader(filename, size)
#     m,n = np.shape(col_matrix)
#
#     tam = max([max(col_matrix[:,0]), max(col_matrix[:,1])])
#     adjacency = sp.lil_matrix((tam,tam))
#
#     for i in xrange(m):
#         #print col_matrix[i,0],col_matrix[i,1]
#         adjacency[col_matrix[i,0] - 1, col_matrix[i,1] - 1] = 1.
#         adjacency[col_matrix[i,1] - 1, col_matrix[i,0] - 1] = 1.
#     #print "create adj 2"
#     return adjacency

# See a time snapchat where you have the top 5 nodes at each moment (are they the same or are they changing?)
# plot all the nodes that are going to exist by the end of the total period (trimestre) y dibujarlos hacia los lados

def plot_li():
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


# It creates an adjacency matrix from an array with the edges. It can be directed, undirected, including all possible nodes, or just restricted to the ones with an edge.
def create_adj(filename = "FB/facebook-wosn-links/out.facebook-wosn-links.txt", size = 0, plot_all = False, undirected = True):
    col_matrix = loader(filename, size)
    m,n = np.shape(col_matrix)

    if undirected == True:

        if plot_all == True:
            tam = max([max(col_matrix[:,0]), max(col_matrix[:,1])])
            adjacency = sp.lil_matrix((tam,tam))

            for i in xrange(m):
                adjacency[col_matrix[i,0] - 1, col_matrix[i,1] - 1] = 1.
                adjacency[col_matrix[i,1] - 1, col_matrix[i,0] - 1] = 1.

        elif plot_all == False:
            conjunto = set(col_matrix[:,0]).union(col_matrix[:,1])
            tam = len(conjunto)
            adjacency = sp.lil_matrix((tam,tam))
            listado = sorted(conjunto)

            for i in xrange(m):
                source = listado.index(col_matrix[i,0])
                target = listado.index(col_matrix[i,1])
                adjacency[source, target] = 1.
                adjacency[target, source] = 1.

    elif undirected == False:
        if plot_all == True:
            tam = max([max(col_matrix[:,0]), max(col_matrix[:,1])])
            adjacency = sp.lil_matrix((tam,tam))

            for i in xrange(m):
                adjacency[col_matrix[i,0] - 1, col_matrix[i,1] - 1] = 1.

        else:
            conjunto = set(col_matrix[:,0]).union(col_matrix[:,1])
            tam = len(conjunto)
            adjacency = sp.lil_matrix((tam,tam))
            listado = sorted(conjunto)

            for i in xrange(m):
                source = listado.index(col_matrix[i,0])
                target = listado.index(col_matrix[i,1])
                adjacency[source, target] = 1.

    return adjacency

def create_nx():
    print True

def time_shabang(filename = "subelj_euroroad/out.subelj_euroroad_euroroad.txt", size = 0, plot_all = False):
    G = nx.Graph()
    edgeses = loader(filename,size)

    if plot_all == True:
        tam = max([max(edgeses[:,0]), max(edgeses[:,1])])
        G.add_nodes_from(xrange(tam))

    G.add_edges_from(edgeses)
    print G.edges()
    print G.nodes()

    eig_c = nx.betweenness_centrality(G)
    {key: value for key, value in variable}
    pos = nx.spring_layout(G)
    for i in xrange(4):
        plt.subplot(2,2,i+1)
        nx.draw_networkx(G, pos=pos, with_labels=False, node_size=35, alpha=.7, node_color = eig_c.values(), width = .5,cmap=plt.cm.YlOrRd)
        size = (i+2)*250
        edgeses = loader(filename,size)
        G.add_edges_from(edgeses)
        pos = nx.spring_layout(G,pos=pos)
        eig_c = nx.betweenness_centrality(G)
    plt.show()


def the_whole_shabang(filename = "subelj_euroroad/out.subelj_euroroad_euroroad.txt", size = 0, plot_all = False, undirected = True):
    if undirected:
        c = time.time()
        G = nx.Graph()
        edgeses = loader(filename,size)
        if plot_all == True:
            tam = max([max(edgeses[:,0]), max(edgeses[:,1])])
            G.add_nodes_from(xrange(tam))
        G.add_edges_from(edgeses)
        eig_c = nx.betweenness_centrality(G)
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos=pos, with_labels=False, node_size=35, alpha=.7, node_color = eig_c.values(), width = .5,cmap=plt.cm.YlOrRd)
        print(time.time() - c)
        plt.show()

        # d = time.time() **** # works using the adjacency matrix I had created
        # adjacency = create_adj(filename, size, plot_all, undirected)
        # g = nx.from_scipy_sparse_matrix(adjacency)
        # eig_c = nx.betweenness_centrality(g)
        # nx.draw_networkx(g, with_labels=False, node_size=35, alpha=.7, node_color = eig_c.values(), width = .5,cmap=plt.cm.YlOrRd)
        # print(time.time() - d)
        # plt.show()

    elif undirected == False:
        return "directed"



if __name__ == '__main__':
    print loader(filename = "subelj_euroroad/out.subelj_euroroad_euroroad.txt", size = 0, from_ = 1165708801, to_ = time.time())
    time_shabang(filename = "subelj_euroroad/out.subelj_euroroad_euroroad.txt", size = 700, plot_all = False)
    time_shabang(filename = "subelj_euroroad/out.subelj_euroroad_euroroad.txt", size = 700, plot_all = True)


    # print "to :",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1165708801))
    # print "to :",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1185148800))
    # print True
    # c = time.time()
    # youtube = loader(filename = "YouTube/youtube-u-growth/out.youtube-u-growth.txt", size = 0, from_ = 1165708801, to_=1167708801)
    # print
    # print np.shape(youtube)
    # print max(youtube[:,3])
    # print(time.time() - c)



    # the_whole_shabang(filename = "subelj_euroroad/out.subelj_euroroad_euroroad.txt", size = 700, plot_all = True)
    # time_shabang(filename = "subelj_euroroad/out.subelj_euroroad_euroroad.txt", size = 250)
