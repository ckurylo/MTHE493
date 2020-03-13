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


def polya_sim_test(adjFile, ballFile, delta, max_n, num_sim, m_mem, num_nodes, Tlist, outputFilePolya, outputFileSIS, opt_method, tenacity):

    sum_metrics = [4*[0] for _ in range(max_n)]
    sum_SIS = [0 for i in range(max_n)]
    node_balls = get_balls(ballFile)
    ave_p = 0
    for i in range(num_nodes):
        ave_p += node_balls[i][1] / sum(node_balls[i])
    ave_p /= num_nodes
    print(ave_p)

    total_time = 0
    for i in range(num_sim):
        print('simulation:')
        print('\r'+str(i+1), end='')
        metrics, sim_time, _, SIS = polya.network_simulation(adjFile, delta, m_mem, max_n, node_balls, 
            Tlist, opt_method, tenacity, SIS=1)
        total_time += sim_time
        for j in range(max_n):
            for k in range(4):
                sum_metrics[j][k] = sum_metrics[j][k] + metrics[j][k]
            sum_SIS[j] = sum_SIS[j] + SIS[j]
    for i in range(max_n):
        for j in range(4): sum_metrics[i][j] /= num_sim
        sum_SIS[i]= [sum_SIS[i]/ num_sim]
    sum_metrics[0].append(total_time)

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
m_mem = 5
num_sim = 200
'''
adjFile = '10N_barabasi_adj.csv'
outputFilePolya = 'polya_heur_bet_even_B30_10N_50sim.csv'
outputFileSIS = 'SIS_heur_bet_even_B30_10N_50sim.csv'
ballFile = '10node_proportions_even.csv'
'''
'''
adjFile = 'adj_files/6N_bridge_adj.csv'
outputFilePolya = 'SIS_Polya_Testing/6Nodes/polya_pre_heur_deg_6N_bridge_B20_R2_even.csv'
outputFileSIS = 'SIS_Polya_Testing/6Nodes/SIS_pre_heur_deg_6N_bridge_B20_R2_even.csv'
ballFile = 'ball_proportion_files/6N_even_proportions.csv'
'''
########
budget = 12
deltaR = 2
tenacity = 1  # weight of node's own Urn in Super Urn

# opt_method = [3,1,0]
# opt_method: [1] for uniform vaccine deployment, [2] for random
    # [3, i] for heuristic with i = 1 for deg cent, 2 for close cent, 3 for bet cent
    # [4, T, k] for gradient descent, T the number of iterations of the algo for each time step
            # k = 0 for pre-draw optimization, k = 1 for post-draw optimization

'''
# HEURISTICS FOR 6Nodes 
topology = ['bridge', 'cycle', 'star', 'stick']
initialDist = ['Conc1', 'Conc3', 'uni']
heuristic_methods = ['deg', 'close', 'bet', 'perc']

for top in topology:

    for dist in initialDist:

        adjFile = 'adj_files/6N_{top}_adj.csv'.format(top=top)
        ballFile = 'ball_proportion_files/6N_{dist}_proportions.csv'.format(dist=dist)
        adj_matrix = importG(adjFile)
        num_nodes = len(adj_matrix[0])
        Tlist = [sum(get_balls(ballFile)[i]) for i in range(num_nodes)]
        for i in range(4):
            method = heuristic_methods[i]
            opt_method = [3,i+1,0]
            outputFilePolya = 'SIS_Polya_Testing/6Nodes/polya_pre_heur_{opt}_6N_{top}_B12_R2_M5_{dist}.csv'.format(top=top, dist=dist, opt=method)
            outputFileSIS = 'SIS_Polya_Testing/6Nodes/SIS_pre_heur_{opt}_6N_{top}_B12_R2_M5_{dist}.csv'.format(top=top, dist=dist, opt=method)

            polya_sim_test(adjFile, ballFile, [budget, deltaR], max_n, num_sim, m_mem, num_nodes, Tlist,
                outputFilePolya, outputFileSIS, opt_method, tenacity)
        print("FINISHED "+ dist)

    print("FINISHED" + top)
'''


budget = 20
# HEURISTICS FOR 10 NODE DENDRIMER
initialDist = ['Conc1', 'Conc3', 'uni']
heuristic_methods = ['deg', 'close', 'bet', 'perc']

for dist in initialDist:

    adjFile = 'adj_files/10N_dendrimer_adj.csv'
    ballFile = 'ball_proportion_files/10N_{dist}_proportions.csv'.format(dist=dist)
    adj_matrix = importG(adjFile)
    num_nodes = len(adj_matrix[0])
    Tlist = [sum(get_balls(ballFile)[i]) for i in range(num_nodes)]
    for i in range(4):
        method = heuristic_methods[i]
        opt_method = [3,i+1,0]
        outputFilePolya = 'SIS_Polya_Testing/10Nodes/polya_pre_heur_{opt}_10N_dendrimer_B12_R2_M5_{dist}.csv'.format(dist=dist, opt=method)
        outputFileSIS = 'SIS_Polya_Testing/10Nodes/SIS_pre_heur_{opt}_10N_dendrimer_B12_R2_M5_{dist}.csv'.format(dist=dist, opt=method)

        polya_sim_test(adjFile, ballFile, [budget, deltaR], max_n, num_sim, m_mem, num_nodes, Tlist,
            outputFilePolya, outputFileSIS, opt_method, tenacity)



# budget as nodes*deltaR = 2----*12
# memory 5/10 use 5
# 10 balls initially-- keep starting infaction the same over all trials of distribution