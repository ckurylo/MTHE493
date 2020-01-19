

def evenDistribution():

def heuristic(n, B, N, C, S):
    deltaB = [0]*n
    totalInfectionCentralityRatio = 0
    for i in range(n):
        totalInfectionCentralityRatio += N[i]*C[i]*S[i]
    for i in range(n):
        deltaB[i] = B*N[i]*C[i]*S[i] / totalInfectionCentralityRatio

    return deltaB


def gradient():
