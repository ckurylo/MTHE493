import numpy as np
import math
import sympy as sym
import csv



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


def Sn_function(G, deltaR, p_p):
    N = G.number_of_nodes()
    c = [0 for i in range(N)]
    d = [0 for i in range(N)]
    sigma = [0 for i in range(N)]
    xN = sym.symbols('x0:%d'%(N))  # N-tuple of vaccines deployed
    for i in G.nodes:
        node = G.nodes[i]['superUrn']

        # sum of all the red balls in a given super urn. note the use of p_p (pre_post). slicing of delta
        # depending on whether the optimization is pre-draw or post-draw (0 for pre, 1 for post)
        # so time indices of delta and Zn (which may be 1 time step ahead) are lined up
        s_delta = 1-p_p
        e_delta = len(node.delta)-p_p
        c[i] = node.super_R + sum([np.dot(j.delta[s_delta:e_delta], j.Zn[1:]) for j in node.Ni_list]) + \
               sum([deltaR*j.Zn[0] for j in node.Ni_list])

        d[i] = node.super_B + node.super_R + sum(node.delta[s_delta:e_delta]) + \
               sum([deltaR * j.Zn[0] for j in node.Ni_list])

        sigma[i] = sum([xN[j.key] * (1 - j.Zn[0]) for j in node.Ni_list])

    # y = str(sum([c[i]/(d[i] + sigma[i]) for i in range(N)])/N)
    # with open('Sn_function_10N.csv', "w+") as my_csv:
    #     csvWriter = csv.writer(my_csv, delimiter=',')
    #     csvWriter.writerow(y)

    return [xN, sum([c[i]/(d[i] + sigma[i]) for i in range(N)])/N]


def gradient(G, T, p_p, B, deltaR):
    N = G.number_of_nodes()
    y = [[] for i in range(T+1)]
    y[0] = [1 for i in range(N)]
    y_bar = y[:][:]
    [xN, f_n] = Sn_function(G, deltaR, p_p)
    f_partials = sym.derive_by_array(f_n, xN)
    if f_partials == N * [0]: return evenDistribution(N, B)  # if all partials are 0, do uniform dist of vaccines

    # f_part_def = [f_partials[i].subs([(xN[j], 1) for j in range(N)]) for i in range(N)]
    # index = np.argmin(f_part_def)
    for k in range(T):
        #
        f_part_def = [f_partials[i].subs([(xN[j], y[k][j]) for j in range(N)]) for i in range(N)]
        index = np.argmin(f_part_def)
        if k == 0:
            vip_node = index
        #
        y_bar[k] = [0 for i in range(N)]
        y_bar[k][index] = B
        #
        alpha_list = [i/100 for i in range(1, 101)]
        f_def = [f_n.subs([(xN[j], y[k][j] + alpha_list[i] * (y_bar[k][j]-y[k][j])) for j in range(N)])
                 for i in range(100)]
        alpha = alpha_list[np.argmin(f_def)]
        #
        y[k+1] = [y[k][i] + alpha * (y_bar[k][i] - y[k][i]) for i in range(N)]

    # round down final result so we dont have fractions of balls, and don't go over budget
    deltaB = [math.floor(y[-1][i]) for i in range(N)]
    # add remainder of budget to most influential node
    deltaB[vip_node] += B - sum(deltaB)
    return deltaB

