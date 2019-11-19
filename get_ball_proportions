import csv
import numpy as np
import pandas as pd


def get_ball_bounds(fileName, outputFile):
    adj = pd.read_csv(fileName, header=None)

    lmax = max(np.linalg.eig(adj)[0])
    print(lmax)
    deltaR = 2
    deltaB = int(deltaR * lmax / 60)+1
    delta = [deltaB, deltaR]
    deltaMax = max(delta)
    print(delta)
    B_bd = [deltaMax*5, int(deltaMax*5.5)+1]
    R_bd = [int(deltaMax*4.5)+1, deltaMax * 5]


    n_nodes = len(adj[0])

    ball_proportions = []
    p = 0
    for i in range(n_nodes):
        R = np.random.choice(R_bd)
        B = np.random.choice(B_bd)
        p += R/(R+B)
        ball_proportions.append([R, B])
    p /= n_nodes


    print(ball_proportions)
    print(p)


    with open(outputFile,"w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter='\t')
        csvWriter.writerows(ball_proportions)

    return [p, ball_proportions]
