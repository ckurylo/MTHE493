import network_polya as polya
import pandas as pd
import numpy
import csv


def importG(graphName):
    return pd.read_csv(graphName, header=None).values.tolist()


def generateBallProportions(delta, n):
    maxdelta = max(delta)
    B_bd = [maxdelta * 10, maxdelta * 11]
    R_bd = [maxdelta * 9, maxdelta * 10]
    node_balls = []
    for i in range(n):
        R = numpy.random.choice(range(R_bd[0], R_bd[1]))
        B = numpy.random.choice(range(B_bd[0], B_bd[1]))
        node_balls.append([B, R])
    return node_balls


def get_balls(ballName):
    g = pd.read_csv(ballName, header=None).values.tolist()
    balls = []
    for i in range(len(g)):
        BR = g[i][0].split('\t')
        BR[0] = int(BR[0])
        BR[1] = int(BR[1])
        balls.append(BR)
    return balls


def polya_sim_test(adjFile, ballFile, delta, max_n, num_sim, m_mem, num_nodes, outputFilePolya, outputFileSIS, opt_method, tenacity):

    sum_metrics = [3*[0] for _ in range(max_n)]
    sum_SIS = [0 for i in range(max_n)]
    #node_balls = generateBallProportions(delta, num_nodes)
    node_balls = get_balls(ballFile)
    ave_p = 0
    for i in range(num_nodes):
        ave_p += node_balls[i][1] / sum(node_balls[i])
    ave_p /= num_nodes
    print(ave_p)

    for i in range(num_sim):
        print('simulation:')
        print('\r'+str(i+1), end='')
        metrics, SIS = polya.network_simulation(adjFile, delta, m_mem, max_n, node_balls, opt_method, tenacity, SIS=1)
        for j in range(max_n):
            for k in range(3):
                sum_metrics[j][k] = sum_metrics[j][k] + metrics[j][k]
            sum_SIS[j] = sum_SIS[j] + SIS[j]
    for i in range(max_n):
        for j in range(3): sum_metrics[i][j] /= num_sim
        sum_SIS[i]= [sum_SIS[i]/ num_sim]

    with open(outputFilePolya, "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(sum_metrics)
    my_csv.close()
    with open(outputFileSIS, "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(sum_SIS)
    my_csv.close()

###############################
# PARAMETER INPUT
max_n = 200
m_mem = 10
num_sim = 50
# adjFile = '100_node_adj_2.csv'
# outputFile = 'weight_demo_metrics.csv'
# ballFile = 'ball_proportions_100_nodes.csv'

adjFile = '10node.csv'
outputFilePolya = 'polya_heur_bet_even_B30_10N_50sim.csv'
outputFileSIS = 'SIS_heur_bet_even_B30_10N_50sim.csv'
ballFile = '10node_proportions_even.csv'
########
budget = 30
deltaR = 2
tenacity = 1  # weight of node's own Urn in Super Urn
adj_matrix = importG(adjFile)
# lmax = max(numpy.linalg.eig(adj_matrix)[0])
# print(lmax)
# deltaB = int(lmax)
# deltaR = deltaB*2

opt_method = [3,3,0]
# opt_method: [1] for uniform vaccine deployment, [2] for random
    # [3, i] for heuristic with i = 1 for deg cent, 2 for close cent, 3 for bet cent
    # [4, T, k] for gradient descent, T the number of iterations of the algo for each time step
            # k = 0 for pre-draw optimization, k = 1 for post-draw optimization


polya_sim_test(adjFile, ballFile, [budget, deltaR], max_n, num_sim, m_mem, len(adj_matrix[0]), 
    outputFilePolya, outputFileSIS, opt_method, tenacity)