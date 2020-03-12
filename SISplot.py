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


def plot_In(inputSIS, inputPolya, axis, legend, max_n, title):

    for i in range(len(inputSIS)):
        dataSIS = pd.read_csv('SIS_Polya_Testing/6Nodes/'+inputSIS[i]+'.csv', header=None).values.tolist()
        dataPolya = pd.read_csv('SIS_Polya_Testing/6Nodes/'+inputPolya[i]+'.csv', header=None).values.tolist()
        In = []
        for j in range(len(dataPolya)):
            In.append(dataPolya[j][0])
        plt.plot(range(max_n), In, label='Polya'+legend[i])
        plt.plot(range(max_n), dataSIS, label='SIS'+legend[i])
        plt.xlabel('Time (n)')
        plt.ylabel('Infection Rate $\\tilde{I}_n$')
        plt.title(title)
        plt.legend()
        #plt.show()
    '''
        plt.plot([0, max_n], [p, p], 'r--')
        plt.axis(axis_list)
        plt.xlabel('Time (n)')
        plt.ylabel('Infection Rate $\\tilde{I}_n$')
        plt.legend(legend)
        plt.title('Curing 10-node network with Gradient Descent curing deployment')
        plt.show()
    '''
    plt.show()

def main():
   # inputSIS = ['SIS_even_pre_10N_50sim.csv', 'SIS_rand_pre_10N_50sim.csv', 'SIS_heur_deg_pre_10N_50sim.csv',
    #    'SIS_heur_bet_pre_10N_50sim.csv','SIS_heur_close_pre_10N_50sim.csv']
   # inputPolya = ['polya_even_pre_10N_50sim.csv', 'polya_rand_pre_10N_50sim.csv', 'polya_heur_deg_pre_10N_50sim.csv',
   #     'polya_heur_bet_pre_10N_50sim.csv','polya_heur_close_pre_10N_50sim.csv']
    inputSIS = ['SIS_uniform_even_10N_50sim.csv', 'SIS_rand_even_10N_50sim.csv', 'SIS_heur_deg_even_B30_10N_50sim.csv',
    'SIS_heur_close_even_B30_10N_50sim.csv', 'SIS_heur_bet_even_B30_10N_50sim.csv']
    inputPolya = ['polya_uniform_even_10N_50sim.csv', 'polya_rand_even_10N_50sim.csv', 'polya_heur_deg_even_B30_10N_50sim.csv',
    'polya_heur_close_even_B30_10N_50sim.csv','polya_heur_bet_even_B30_10N_50sim.csv']
    
    inputPolya = [
    'polya_pre_heur_deg_6N_bridge_B20_R2_C1',
    'polya_pre_heur_deg_6N_bridge_B20_R2_C3',
    'polya_pre_heur_deg_6N_bridge_B20_R2_uni'
    ]

    inputSIS = [
    'SIS_pre_heur_deg_even_6N_bridge_B20_R2_C1',
    'SIS_pre_heur_deg_6N_bridge_B20_R2_C3',
    'SIS_pre_heur_deg_even_6N_bridge_B20_R2_uni'
    ]

    legend = ['C1', 'C3', 'uni']
    title = '6N Bridge Deg'
    '''
    inputPolya = [
    'Polya_pre_heur_perc_6N_bridge_B20_R2_uni',
    'Polya_pre_heur_perc_6N_bridge_B20_R2_even',
    'Polya_pre_heur_perc_6N_bridge_B20_R2_C1',
    'Polya_pre_heur_perc_6N_bridge_B20_R2_C3'
    ]
    inputSIS = [
    'SIS_pre_heur_perc_6N_bridge_B20_R2_uni',
    'SIS_pre_heur_perc_6N_bridge_B20_R2_even',
    'SIS_pre_heur_perc_6N_bridge_B20_R2_C1',
    'SIS_pre_heur_perc_6N_bridge_B20_R2_C3'
    ]
    legend = ['uni', 'even', 'C1', 'C3']
    title = '6N Bridge Perc'
    '''
    max_n = 200
    axis = [0, max_n, 0, 1]
    #p = getP('10node_proportions_even.csv')
    #legend = ['SIS degree centrality', 'Polya degree centrality']
    #legend = ['Uniform', 'Random', 'Degree Centrality', 'Closeness Centrality','Betweeness Centrality']
    plot_In(inputSIS, inputPolya, axis, legend, max_n, title)



if __name__=='__main__':
    main()
