import numpy as np

def evenDistribution(n, b):
    deltaB = [b/n for i in range(n)]
    return deltaB

def randomDistribution(n, b):
    values = [0.0, b] + list(np.random.uniform(low=0.0,high=b,size=n-1))
    values.sort()
    deltaB = [values[i+1] - values[i] for i in range(n)]
    return deltaB

def heuristic(n, b, N, C, S):
    deltaB = [0]*n
    totalInfectionCentralityRatio = 0
    for i in range(n):
        totalInfectionCentralityRatio += N[i]*C[i]*S[i]
    for i in range(n):
        deltaB[i] = b*N[i]*C[i]*S[i] / totalInfectionCentralityRatio
    return deltaB


def gradient():
