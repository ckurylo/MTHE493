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
        node_balls.append([R, B])
    return node_balls


def get_balls(ballName):
    g = pd.read_csv(ballName, header=None).values.tolist()
    balls = []
    for i in range(len(g)):
        RB = g[i][0].split('\t')
        RB[0] = int(RB[0])
        RB[1] = int(RB[1])
        balls.append(RB)
    return balls


def polya_sim_test(adjFile, ballFile, delta, max_n, num_sim, m_mem, num_nodes, outputFile):

    sum_metrics = [3*[0] for _ in range(max_n)]
    #node_balls = generateBallProportions(delta, num_nodes)
    node_balls = get_balls(ballFile)
    ave_p = 0
    for i in range(num_nodes):
        ave_p += node_balls[i][0] / sum(node_balls[i])
    ave_p /= num_nodes
    print(ave_p)

    for i in range(num_sim):
        print('simulation:')
        print('\r'+str(i), end='')
        metrics = polya.network_simulation(adjFile, delta, m_mem, max_n, node_balls)
        for j in range(max_n):
            for k in range(3):
                sum_metrics[j][k] = sum_metrics[j][k] + metrics[j][k]
    for i in range(max_n):
        for j in range(3): sum_metrics[i][j] /= num_sim

    with open(outputFile, "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(sum_metrics)

###############################
# PARAMETER INPUT
max_n = 10
m_mem = max_n + 1
num_sim = 1
adjFile = '100_node_adj.csv'
outputFile = '.csv'
ballFile = 'ball_proportions_100_nodes.csv'
########

adj_matrix = importG(adjFile)
lmax = max(numpy.linalg.eig(adj_matrix)[0])
print(lmax)
deltaB = int(lmax)
deltaR = deltaB*2

polya_sim_test(adjFile, ballFile, [deltaB, deltaR], max_n, num_sim, m_mem, len(adj_matrix[0]), outputFile)