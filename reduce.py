import numpy as np
import networkx as nx
import pandas as pd
from networkx.algorithms import community
import matplotlib.pyplot as plt

#graph reduction algorithm, finds important nodes and builds paths to them
def reduce(g, n, c_alg):
    paths = [[]]
    g_reduced = nx.Graph()
    loc = getCommunities(g)
    for comm in loc:
        for k in comm:
            if getSCV(k, g) > getSCV(n, g):
                #print('adding')
                sp = getShortestPath(k, n, g)
                paths.append(sp)

    addToReducedGraph(paths, g_reduced)

    return g_reduced

# get communities based on some criteria
def getCommunities(g):
    community_generator = community.girvan_newman(g)
    top_level_communities = next(community_generator)
    next_level_communities = next(community_generator)
    list(sorted(map(sorted, next_level_communities)))
    return sorted(map(sorted, next_level_communities))

# build the graph out of "important" graphs
def addToReducedGraph(paths, g_reduced):
    for path in paths:
        g_reduced.add_path(path)

#might add other ways to do this -- doesnt really matter tho
def getShortestPath(v, n, g):
    return nx.dijkstra_path(g, v, n)

#selection criteria values -- will add more
def getSCV(v, g):
    return nx.degree_centrality(g)[v]

def plotGraph(reduced, g):
    colourmap = []
    for node in g.nodes:
        if node in reduced.nodes:
            print('kept!', node)
            colourmap.append('blue')
        else:
            colourmap.append('red')

    plt.figure(1)
    nx.draw(g, node_color=colourmap, layout=nx.spring_layout(g), with_labels=True, node_size=30, width=0.25)
    #plt.figure(2)
    #nx.draw(reduced, node_color='blue', layout=nx.spring_layout(reduced), with_labels=True, node_size=30, width=0.25)
    plt.show()

def main():
    adjFile = 'goodmad.csv'
    G = nx.from_numpy_matrix(pd.read_csv(adjFile, header=None).as_matrix())
    iterations = 6
    selection_criteria = 0
    start_node = 0
    community_alg = 0

    for i in range(iterations):
        reduced_graph = reduce(G, start_node, community_alg)
        G = reduced_graph

    plotGraph(reduced_graph, G)

if __name__=='__main__':
    main()
