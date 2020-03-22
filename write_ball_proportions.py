import csv
import numpy as np
import pandas as pd
import math

def get_ball_bounds(fileName, outputFile):
    adj = pd.read_csv(fileName, header=None)

    n_nodes = len(adj[0])

    ball_proportions = []
    p = 0
    for i in range(n_nodes):
        T = 41702
        #R = np.random.choice(R_bd)
        #B = np.random.choice(B_bd)
        R = 0
        B = T
        if i in [0, 4, 12, 29, 44]:
            R = math.floor(0.42*T)
            B = T-R
        p += R/(R+B)
        ball_proportions.append([B, R])
    p /= n_nodes


    print(ball_proportions)
    print(p)


    with open(outputFile,"w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter='\t')
        csvWriter.writerows(ball_proportions)

    return [p, ball_proportions]


def write_balls_from_G(G, fileName):
    ball_proportions = []
    for i in range(G.number_of_nodes()):
        B = round((1 - G.nodes[i]['superUrn'].Um[0]) * (G.nodes[i]['superUrn'].T + sum(G.nodes[i]['superUrn'].delta)))
        R = round(G.nodes[i]['superUrn'].Um[0] * (G.nodes[i]['superUrn'].T + sum(G.nodes[i]['superUrn'].delta)))
        B = int(B)
        R = int(R)

        ball_proportions.append([B, R])

    with open(fileName, "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter='\t')
        csvWriter.writerows(ball_proportions)


adj_dir = 'adj_files/'
ball_dir = 'ball_proportion_files/'
get_ball_bounds(adj_dir + 'madagascar_weighted_adj.csv', ball_dir + '94N_pre_disease_proportions.csv')
