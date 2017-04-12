import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
import mmap
from scipy import sparse as sp
import time
import plotly.plotly as py
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
    Determines the number of nodes in the
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
    * We are missing to do anything with the
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
        if timed == True:
            clear_mat = np.array([i.strip().split(' ') for i in f if int(i.strip().split(' ')[3])>from_ and int(i.strip().split(' ')[3]) < to_], int)
        else:
            clear_mat = np.array([next(f).strip().split(' ') for i in xrange(lines-contador+1)], int)

    return clear_mat
