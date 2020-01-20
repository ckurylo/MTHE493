import numpy as np
import math


def evenDistribution(n, b):
    deltaB = [math.floor(b/n) for i in range(n)]
    return deltaB

def randomDistribution(n, b):
    values = [0.0, b] + list(np.random.uniform(low=0.0,high=b,size=n-1))
    values.sort()
    deltaB = [math.floor(values[i+1] - values[i]) for i in range(n)]
    return deltaB

def heuristic(n, b, N, C, S):
    deltaB = [0]*n
    totalInfectionCentralityRatio = 0
    for i in range(n):
        totalInfectionCentralityRatio += N[i]*C[i]*S[i]
    for i in range(n):
        deltaB[i] = math.floor(b*N[i]*C[i]*S[i] / totalInfectionCentralityRatio)
    return deltaB


def Sn_function(G):
    c = [0 for i in range(G.number_of_nodes())]
    d = [0 for i in range(G.number_of_nodes())]
    for i in G.nodes:
        node = G.nodes[i]['superUrn']
        c[i] = node.super_R + sum([np.dot(j.delta, j.Zn) for j in node.Ni_list])
        #d[i] = c[i] + node.super_B +



def gradient():
    #gradient descent algorithm
    return


