import network_polya as polya
import pandas as pd
import numpy
import csv
import file_io as io
import write_ball_proportions as wbp
import os
from pathlib import Path

def get_user_input(prompt):
    print(prompt + ':', end='\t')
    return input()


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
        BR[0] = int(float(BR[0]))
        BR[1] = int(float(BR[1]))
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
            print('\nsimulation:')
            print('\r'+str(i+1), end='')
            metrics, sim_time = polya.network_simulation(adjFile, delta, m_mem, max_n, node_balls, Tlist,
                                                           opt_method, tenacity)[0:2]
            total_time += sim_time
            for j in range(max_n):
                for k in range(4):
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
        metrics, sim_time, G = polya.network_simulation(adjFile, delta, m_mem, max_n, node_balls, Tlist,
                                                        opt_method, tenacity)
        metrics[0].append(sim_time)
        with open(outputDirectory + outputMetricsFile, "w+") as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(metrics)
        wbp.write_balls_from_G(G, 'ball_proportion_files/' + outputBallFile)


###############################
# PARAMETER INPUT

if get_user_input('Input parameters manually? (y/n)') == 'n':
    ### Initial Conditions File
    ini_fileName = 'topology_test_6N.txt'
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
    ### Network Conditions Parameters
    num_sim = 100
    adjFile = 'adj_files/6N_bridge_adj.csv'
    ballFile = 'ball_proportion_files/6N_uni_proportions.csv'
    outputDirectory = 'data/to_merge/topology/close/bridge/'
    #######
    outputBallFile = 'ball_prop_demo.csv'  # fileName for creating ball proportions from running a disease
    # set budget to 0 in this case, max_n to the time at which we want to pull out ball proportions, and num_sim to 1
    opt_method = [3, 1, 0]
    # opt_method: [1] for uniform vaccine deployment, [2] for random
    # [3, i, k] for heuristic with i = 1 for deg cent, 2 for close cent, 3 for bet cent, 4 for perc cent
    # [4, T, k] for gradient descent, T the number of iterations of the algo for each time step
    # k = 0 for pre-draw optimization, k = 1 for post-draw optimization, k = 2 so balls are allocated to every node

    ### housekeeping
    adj_matrix = importG(adjFile)
    num_nodes = len(adj_matrix[0])

    #Tlist = num_nodes * [10]
    Tlist = [sum(get_balls(ballFile)[i]) for i in range(num_nodes)]
else:
    ini_fileName = get_user_input('ini file name/directory within ini_files/ folder (use / for backslash)')
    ini_fileName = os.path.splitext(ini_fileName)[0] + '.txt'
    adjFile = 'adj_files/' + get_user_input('adj file name/directory within adj_files/ folder (use / for backslash)')
    adjFile = os.path.splitext(adjFile)[0] + '.csv'
    ballFile = 'ball_proportion_files/' + get_user_input('ball prop file name/directory within ball_prop_files/ folder '
                                                         '(use / for backslash)')
    ballFile = os.path.splitext(ballFile)[0] + '.csv'

    adj_matrix = importG(adjFile)
    num_nodes = len(adj_matrix[0])

    if get_user_input('Same amount of total balls for each urn? (y/n)') == 'y':
        Tlist = num_nodes*[int(get_user_input('Total balls per urn'))]
    else:
        print('Then taking number ball proportions ratios to be exact number of balls')
        Tlist = [sum(get_balls(ballFile)[i]) for i in range(num_nodes)]
    opt_method = []
    print('Optimization Method')
    pp = int(get_user_input('0: pre-draw optimization - 1: post-draw optimization - 2: allocate to all nodes'))
    opt = int(get_user_input('1: uniform deployment - 2: random deployment - 3: heuristic - 4: gradient descent'))
    opt_method.append(opt)
    if opt == 3:
        print('centrality measure')
        k = int(get_user_input('1: degree cent - 2: closeness cent - 3: betweenness cent - 4: percolation cent'))
        opt_method.extend([k, pp])
    elif opt == 4:
        k = int(get_user_input('number of iterations of gradient descent (should be 3 for 10 node and under)'))
        opt_method.extend([k, pp])
    else:
        opt_method.extend([0, pp])

    outputBallFile = ''
    num_sim = int(get_user_input('number of simulations to run (enter 1 to output ball proportions)'))
    if num_sim == 1:
        outputBallFile = get_user_input('output ball proportion file name')
        outputBallFile = os.path.splitext(outputBallFile)[0] + '.csv'

    outputDirectory = get_user_input('output directory (use / for backslash, end in /)')


Path(os.getcwd() + '/' + outputDirectory).mkdir(parents=True, exist_ok=True)

# Read ini file
iniList = io.ini_file_to_ini(ini_fileName)
# predraw_factor = iniList[0]
max_n = iniList[1]
m_mem = iniList[2]
budget = iniList[3]
deltaR = iniList[4]

print('Output File name')
name_choice = int(get_user_input('1: automatic file name - 2: automatic file name + user inputted suffix '
                                 '- 3: user input file name'))
if name_choice == 1:
    outputFile = io.graph_to_string(num_sim, opt_method, num_nodes, adjFile[10:-8],
                                    ini_fileName[:-4], ballFile[22:-4])
elif name_choice == 2:
    outputFile = io.graph_to_string(num_sim, opt_method, num_nodes, adjFile[10:-8],
                                    ini_fileName[:-4], ballFile[22:-4])
    outputFile += '_' + os.path.splitext(get_user_input('suffix to append to output file name'))[0] + '.csv'
else:
    outputFile = os.path.splitext(get_user_input('please enter output file name'))[0] + '.csv'


polya_sim_test(adjFile, ballFile, outputBallFile, [budget, deltaR], max_n, num_sim, m_mem, num_nodes, outputFile,
               outputDirectory, opt_method, tenacity=1)

# lmax = max(numpy.linalg.eig(adj_matrix)[0])
# print(lmax)

