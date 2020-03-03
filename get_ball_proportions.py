import csv
import numpy as np
import pandas as pd

def get_ball_bounds(fileName, outputFile):
    adj = pd.read_csv(fileName, header=None)

    n_nodes = len(adj[0])

    ball_proportions = []
    p = 0
    for i in range(n_nodes):
        #R = np.random.choice(R_bd)
        #B = np.random.choice(B_bd)
        R = 6
        B = 4
        p += R/(R+B)
        ball_proportions.append([B, R])
    p /= n_nodes


    print(ball_proportions)
    print(p)


    with open(outputFile,"w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter='\t')
        csvWriter.writerows(ball_proportions)

    return [p, ball_proportions]



get_ball_bounds('100N_barabasi_adj.csv', 'ball_proportions_100_nodes.csv')