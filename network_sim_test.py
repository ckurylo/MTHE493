import network_polya as polya
import pandas as pd
import numpy
import csv
import file_io as io
import write_ball_proportions as wbp


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


def polya_sim_test(adjFile, ballFile, outputBallFile, delta, max_n, num_sim, m_mem, num_nodes, outputMetricsFile,
                   outputDirectory, opt_method, tenacity):

    sum_metrics = [4*[0] for _ in range(max_n)]

    #node_balls = generateBallProportions(delta, num_nodes)
    node_balls = get_balls(ballFile)
    ave_p = 0
    for i in range(num_nodes):
        ave_p += node_balls[i][1] / sum(node_balls[i])
    ave_p /= num_nodes
    print(ave_p)

    total_time = 0
    if num_sim > 1:
        for i in range(num_sim):
            print('simulation:')
            print('\r'+str(i+1), end='')
            metrics, sim_time = polya.network_simulation(adjFile, delta, m_mem, max_n, node_balls,
                                                         opt_method, tenacity)[0:1]
            total_time += sim_time
            for j in range(max_n):
                for k in range(3):
                    sum_metrics[j][k] = sum_metrics[j][k] + metrics[j][k]
        for i in range(max_n):
            for j in range(4): sum_metrics[i][j] /= num_sim
        sum_metrics[0].append(total_time)
        with open(outputDirectory + outputMetricsFile, "w+") as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(sum_metrics)
    #######
    #  single simulation case for the purpose of saving final ball proportions
    else:
        metrics, sim_time, G = polya.network_simulation(adjFile, delta, m_mem, max_n, node_balls, opt_method, tenacity)
        metrics[0].append(sim_time)
        with open(outputDirectory + outputMetricsFile, "w+") as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(metrics)
        wbp.write_balls_from_G(G, outputDirectory + outputBallFile)


###############################
# PARAMETER INPUT
### Initial Conditions File
ini_fileName = 'ini2_demo.txt'
# predraw_factor = 1
# max_n = predraw_factor * 200
# m_mem = predraw_factor * 10
# budget = 20 / predraw_factor
# deltaR = 2 / predraw_factor

#########################################
# Create ini file once, comment out after
# OR run file_io.py to create your ini file separately
# io.ini_to_ini_file(predraw_factor, max_n, m_mem, budget, deltaR, ini_fileName)
##########################################
# Read ini file
iniList = io.ini_file_to_ini(ini_fileName)
predraw_factor = iniList[0]
max_n = iniList[1]
m_mem = iniList[2]
budget = iniList[3]
deltaR = iniList[4]
ballFile = iniList[5]

### Network Conditions Parameters
num_sim = 1
adjFile = 'adj_files/6N_bridge_adj.csv'
adj_matrix = importG(adjFile)
num_nodes = len(adj_matrix[0])
ballFile = 'ball_proportion_files/6node_proportions.csv'
outputDirectory = 'demo_files/'
#######
outputBallFile = 'ball_prop_demo.csv'  # fileName for creating ball proportions from running a disease
# set budget to 0 in this case, max_n to the time at which we want to pull out ball proportions, and num_sim to 1


opt_method = [1, 1, 0]
# opt_method: [1] for uniform vaccine deployment, [2] for random
# [3, i] for heuristic with i = 1 for deg cent, 2 for close cent, 3 for bet cent, 4 for perc cent
# [4, T, k] for gradient descent, T the number of iterations of the algo for each time step
# k = 0 for pre-draw optimization, k = 1 for post-draw optimization


outputFile = io.graph_to_string(num_sim, opt_method, num_nodes, adjFile[10:-8],
                                ini_fileName.strip('.txt'), ballFile.strip('.csv')[22:])



polya_sim_test(adjFile, ballFile, outputBallFile, [budget, deltaR], max_n, num_sim, m_mem, num_nodes, outputFile,
               outputDirectory, opt_method, tenacity=1)

# lmax = max(numpy.linalg.eig(adj_matrix)[0])
# print(lmax)

