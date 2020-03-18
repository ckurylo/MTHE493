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

    for i in range(len(inputPolya)):
        #dataSIS = pd.read_csv('SIS_Polya_Testing/6Nodes/'+inputSIS[i]+'.csv', header=None).values.tolist()
        dataPolya = pd.read_csv(inputPolya[i], header=None).values.tolist()
        In = []
        for j in range(len(dataPolya)):
            In.append(dataPolya[j][0])
        plt.plot(range(max_n), In, label=legend[i])
        #plt.plot(range(max_n), dataSIS, label='SIS'+legend[i])
        plt.xlabel('Time (n)')
        plt.ylabel('Infection Rate $\\tilde{I}_n$')

    plt.title(title)
    plt.legend()
    plt.show()

def main():
    inputPolya = [
    'SIS_Polya_Testing/10Nodes/polya_post_grad_10N_dendrimer_B12_R2_M5_avg.csv',
    'SIS_Polya_Testing/10Nodes/polya_pre_heur_bet_10N_dendrimer_B12_R2_M5_avg.csv',
    'SIS_Polya_Testing/10Nodes/polya_pre_heur_close_10N_dendrimer_B12_R2_M5_avg.csv',
    'SIS_Polya_Testing/10Nodes/polya_pre_heur_deg_10N_dendrimer_B12_R2_M5_avg.csv',
    'SIS_Polya_Testing/10Nodes/polya_pre_heur_perc_10N_dendrimer_B12_R2_M5_avg.csv'
    ]
    inputSIS=[]
    for top in ['bridge', 'cycle', 'star', 'stick']:
        inputPolya = [
        'SIS_Polya_Testing/6Nodes/polya_pre_heur_bet_6N_{top}_B12_R2_M5_avg.csv'.format(top=top),
        'SIS_Polya_Testing/6Nodes/polya_pre_heur_close_6N_{top}_B12_R2_M5_avg.csv'.format(top=top),
        'SIS_Polya_Testing/6Nodes/polya_pre_heur_deg_6N_{top}_B12_R2_M5_avg.csv'.format(top=top),
        'SIS_Polya_Testing/6Nodes/polya_pre_heur_perc_6N_{top}_B12_R2_M5_avg.csv'.format(top=top)
        ]

        legend = ['betweeness', 'closeness', 'degree', 'percolation']
        title = '6N {top}'.format(top=top)

        max_n = 200
        axis = [0, max_n, 0, 1]
        #p = getP('10node_proportions_even.csv')
        #legend = ['SIS degree centrality', 'Polya degree centrality']
        #legend = ['Uniform', 'Random', 'Degree Centrality', 'Closeness Centrality','Betweeness Centrality']
        plot_In(inputSIS, inputPolya, axis, legend, max_n, title)



if __name__=='__main__':
    main()
