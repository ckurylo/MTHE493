import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import OptimizationMethods as opt

def initialParameters(plot, lmax, N):
    betaSIS = [0.15]*N #probability that a node will get infected through contact with a single infected neighbor
    #deltaSIS is probability that a node will recover from infection 
    if(plot == 'a'):
        deltaSIS = (lmax/10)*betaSIS  
    elif(plot == 'b'):
        deltaSIS = (lmax*1.01)*betaSIS
    else:
        deltaSIS = betaSIS

    return betaSIS, deltaSIS

def calculateParameters(G, N, deltaB, deltaR):
    lmax = max(np.linalg.eig(G)[0])

    betaSIS = [0.15]*N #probability that a node will get infected through contact with a single infected neighbor

    deltaSIS = [betaSIS[i]*deltaB[i]/deltaR[i] for i in range(0,N)]

    return betaSIS, deltaSIS

def SISInitilize(T, N, initial):
    P0 = [int(initial[x][0])/(int(initial[x][0])+int(initial[x][1])) for x in range(0, N)]

    Pi=[0 for x in range(0,T)]
    Pi[0]=P0
    avgInfection = [0 for x in range(0,T)]
    avgInfection[0] = sum(P0)/N

    return Pi, avgInfection

def SISModelStep(adjFile, N, deltaB, deltaR, Pi, avgInfSIS, t):
    adj = pd.read_csv(adjFile, header=None)
    deltaSIS, betaSIS = calculateParameters(adj, N, deltaB, deltaR)

    Pit = [0 for x in range(0,N)]
    #avg infection rate for all nodes at time t
    avgInfectionRate = 0
    for i in range(0,N):
        #calculating infection of nodes in the neighborhood
        neighborInfected = 1
        for j in range(0,N):
            if(adj[i][j]==1):
                neighborInfected = neighborInfected*(1-betaSIS[i]*Pi[t-1][j])
        Pit[i] = (Pi[t-1][i]*(1-deltaSIS[i]) + (1-Pi[t-1][i])*(1-neighborInfected))
        avgInfectionRate = avgInfectionRate+(1/N)*Pit[i]
    Pi[t] = Pit
    avgInfSIS[t] = avgInfectionRate    

    return Pi, avgInfSIS

def main():
    data = pd.read_csv('100_node_adj.csv', header=None)
    prop = list(csv.reader(open('ball_proportions_100_nodes.csv'), delimiter='\t'))
    N=100

if __name__=='__main__':
    main()