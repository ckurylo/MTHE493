import numpy as np
import networkx as nx
import pandas as pd
from networkx.algorithms import community
import matplotlib.pyplot as plt

#graph reduction algorithm, finds important nodes and builds paths to them
def reduce(g, r, n, c_alg):
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

def plotGraph(g):
    print(type(g))
    nx.draw(g, layout=nx.spring_layout(g), with_labels=True, node_size = 30, width = 0.25)
    plt.show()

def main():
    adjFile = 'goodmad.csv'
    G = nx.from_numpy_matrix(pd.read_csv(adjFile, header=None).as_matrix())
    iterations = 10
    selection_criteria = 0
    start_node = 0
    community_alg = 0

    reduced_graph = reduce(G, iterations, start_node, community_alg)
    plotGraph(reduced_graph)

    #layout = nx.spring_layout(reduced_graph)
    #nx.draw(reduced_graph, pos=layout, node_size=30, width=0.25)


if __name__=='__main__':
    main()
