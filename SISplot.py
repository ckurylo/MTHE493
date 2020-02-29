import matplotlib.pyplot as plt
import pandas as pd
import csv


def get_balls(ballName):
    g = pd.read_csv(ballName, header=None).values.tolist()
    balls = []
    for i in range(len(g)):
        BR = g[i][0].split('\t')
        BR[0] = int(BR[0])
        BR[1] = int(BR[1])
        balls.append(BR)
    return balls


def getP(ballFile):
    node_balls = get_balls(ballFile)
    ave_p = 0
    for i in range(len(node_balls)):
        ave_p += node_balls[i][1] / sum(node_balls[i])
    ave_p /= len(node_balls)
    return ave_p


def plot_In(inputSIS, inputPolya, axis, legend, max_n, p):

    for i in range(len(inputSIS)):
        dataSIS = pd.read_csv(inputSIS[i], header=None).values.tolist()
        dataPolya = pd.read_csv(inputPolya[i], header=None).values.tolist()
        In = []
        for j in range(len(dataPolya)):
            In.append(dataPolya[j][0])
        plt.plot(range(max_n), In, label='Polya')
        plt.plot(range(max_n), dataSIS, label='SIS')
        plt.xlabel('Time (n)')
        plt.ylabel('Infection Rate $\\tilde{I}_n$')
        plt.title('10-node network '+ legend[i])
        plt.legend()
        plt.show()
    '''
        plt.plot([0, max_n], [p, p], 'r--')
        plt.axis(axis_list)
        plt.xlabel('Time (n)')
        plt.ylabel('Infection Rate $\\tilde{I}_n$')
        plt.legend(legend)
        plt.title('Curing 10-node network with Gradient Descent curing deployment')
        plt.show()
    '''

def main():
   # inputSIS = ['SIS_even_pre_10N_50sim.csv', 'SIS_rand_pre_10N_50sim.csv', 'SIS_heur_deg_pre_10N_50sim.csv',
    #    'SIS_heur_bet_pre_10N_50sim.csv','SIS_heur_close_pre_10N_50sim.csv']
   # inputPolya = ['polya_even_pre_10N_50sim.csv', 'polya_rand_pre_10N_50sim.csv', 'polya_heur_deg_pre_10N_50sim.csv',
   #     'polya_heur_bet_pre_10N_50sim.csv','polya_heur_close_pre_10N_50sim.csv']
    inputSIS = ['SIS_uniform_even_10N_50sim.csv', 'SIS_rand_even_10N_50sim.csv', 'SIS_heur_deg_even_B30_10N_50sim.csv',
    'SIS_heur_close_even_B30_10N_50sim.csv', 'SIS_heur_bet_even_B30_10N_50sim.csv']
    inputPolya = ['polya_uniform_even_10N_50sim.csv', 'polya_rand_even_10N_50sim.csv', 'polya_heur_deg_even_B30_10N_50sim.csv',
    'polya_heur_close_even_B30_10N_50sim.csv','polya_heur_bet_even_B30_10N_50sim.csv']
    max_n = 200
    axis = [0, max_n, 0, 1]
    p = getP('10node_proportions_even.csv')
    #legend = ['SIS degree centrality', 'Polya degree centrality']
    legend = ['Uniform', 'Random', 'Degree Centrality', 'Closeness Centrality','Betweeness Centrality']
    plot_In(inputSIS, inputPolya, axis, legend, max_n, p)



if __name__=='__main__':
    main()
