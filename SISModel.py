import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def SIS_Model(adj, N, init, plot):
    lmax = max(np.linalg.eig(adj)[0])
    betaSIS = 0.15 #probability that a node will get infected through contact with a single infected neighbor

    #deltaSIS = betaSIS
    if(plot == 'a'):
        deltaSIS = (lmax/10)*betaSIS  #probability that a node will recover from infection 
    elif(plot == 'b'):
        deltaSIS = (lmax*1.01)*betaSIS
    else:
        deltaSIS = betaSIS

    T = 100
    P0 = [int(init[x][0])/(int(init[x][0])+int(init[x][1])) for x in range(0, N)]

    Pi=[0 for x in range(0,T)]
    Pi[0]=P0
    avgInfection = [0 for x in range(0,T)]
    avgInfection[0] = sum(P0)/N

    for t in range(1, T):
        Pit = [0 for x in range(0,N)]
        #avg infection rate for all nodes at time t
        avgInfectionRate = 0
        for i in range(0,N):
            #calculating infection of nodes in the neighborhood
            neighborInfected = 1
            for j in range(0,N):
                if(adj[i][j]==1):
                    neighborInfected = neighborInfected*(1-betaSIS*Pi[t-1][j])
            Pit[i] = (Pi[t-1][i]*(1-deltaSIS) + (1-Pi[t-1][i])*(1-neighborInfected))
            avgInfectionRate = avgInfectionRate+(1/N)*Pit[i]
        Pi[t]=Pit
        avgInfection[t]=avgInfectionRate

    return T, avgInfection

def graphInfection(T, avgInf):
    tVal = [x for x in range(0,T)]
    plt.figure()
    plt.plot(tVal, avgInf)
    plt.title("SIS Infection Rate")
    plt.xlabel("Time t")
    plt.ylabel("Infection Rate")
    #plt.show()

def main():
    data = pd.read_csv('100_node_adj.csv', header=None)
    prop = list(csv.reader(open('ball_proportions_100_nodes.csv'), delimiter='\t'))
    N=100
    T, avgInfa = SIS_Model(data, N, prop, 'a')
    graphInfection(T, avgInfa)
    T, avgInfb = SIS_Model(data, N, prop, 'b')
    graphInfection(T, avgInfb)
    T, avgInfc = SIS_Model(data, N, prop, 'c')
    graphInfection(T, avgInfc)
    plt.show()

if __name__=='__main__':
    main()
