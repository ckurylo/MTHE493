import numpy as np
import math
import sympy as sym


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
    sigma = [0 for i in range(G.number_of_nodes())]
    xN = sym.symbols('x0:%d'%(G.number_of_nodes()+1))  # N-tuple of vaccines deployed
    for i in G.nodes:
        node = G.nodes[i]['superUrn']
        c[i] = node.super_R + sum([np.dot(j.delta, j.Zn) for j in node.Ni_list])
        d[i] = node.super_B + node.super_R + sum(node.delta[1:]) + sum([j.delta[0] * j.Zn[0] for j in node.Ni_list])
        sigma[i] = sum([xN[j.key] * (1 - j.Zn[0]) for j in node.Ni_list])
    return [xN, sum([c[i]/(d[i] + sigma[i]) for i in range(len(c))])]


def gradient(G, T, B):
    N = G.number_of_nodes()
    y = [[] for i in range(T+1)]
    y[0] = [0 for i in range(N)]
    y[0][0] = B
    y_bar = y[:][:]
    [xN, f_n] = Sn_function(G)
    f_partials = sym.derive_by_array(f_n, xN)
    if f_partials == N * [0]: return evenDistribution(N, B)  # if all partials are 0, do uniform dist of vaccines
    for k in range(T):
        #
        f_part_def = [f_partials[i].subs([(xN[j], 1) for j in range(N)]) for i in range(N)]
        index = np.argmin(f_part_def)
        #
        y_bar[k] = [0 for i in range(N)]
        y[k][index] = B
        #
        alpha_list = [i/100 for i in range(1, 101)]
        f_def = [f_n.subs([(xN[j], y[k][j] + alpha_list[i] * (y_bar[k][j]-y[k][j])) for j in range(N)])
                 for i in range(100)]
        alpha = np.argmin(f_def)
        #
        y[k+1] = [y[k][i] + alpha * (y_bar[k][i] - y[k][i]) for i in range(N)]

    return y[-1]

