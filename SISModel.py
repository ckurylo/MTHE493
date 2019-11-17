
import matplotlib.pyplot as plt
import pandas as pd
import csv


def SIS_Model(adj, N, Ri, Bi):
    lmax = 5.05
    betaSIS=0.15 #probability that a node will get infected through contact with a single infected neighbor
    deltaSIS= (lmax/10)*betaSIS  #probability that a node will recover from infection 
    T=100
    P0 = [Ri/(Ri+Bi) for x in range(0, N)]

    Pi=[0 for x in range(0,T)]
    Pi[0]=P0
    avgInfection = [0 for x in range(0,T)]
    avgInfection[0] = Ri/(Ri+Bi)

    for t in range(1, T):
        Pit = [0 for x in range(0,N)]
        #avg infection rate for all nodes at time t
        avgInfectionRate = 0
        for i in range(0,N):
            #calculating infection of nodes in the neighborhood
            neighborInfected = 1
            for j in range(0,N):
                if(adj[i][j]==1):
                    neighborInfected = neighborInfected*(1-betaSIS*Pi[t-1][j]) #
            Pit[i] = (Pi[t-1][i]*(1-deltaSIS) + (1-Pi[t-1][i])*(1-neighborInfected))#
            avgInfectionRate = avgInfectionRate+(1/N)*Pit[i]#
        Pi[t]=Pit
        avgInfection[t]=avgInfectionRate

    return T, avgInfection

def graphInfection(T, avgInf):
    tVal = [x for x in range(0,T)]
    plt.figure(1)
    plt.plot(tVal, avgInf)
    plt.title("SIS Infection Rate")
    plt.xlabel("Time t")
    plt.ylabel("Infection Rate")
    plt.show()



def main():
    data = list(csv.reader(open('network.csv')))
    N=200
    network = pd.read_csv('network.csv',sep=',')
    T, avgInf = SIS_Model(data, N, 2, 3)
    graphInfection(T, avgInf)

if __name__=='__main__':
    main()
