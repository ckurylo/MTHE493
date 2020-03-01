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


def plot_In(inputPre, inputPost, axis, legend, max_n, p):

    for i in range(len(inputPre)):
        dataPre = pd.read_csv(inputPre[i], header=None).values.tolist()
        dataPost = pd.read_csv(inputPost[i], header=None).values.tolist()
        InPre = []
        InPost = []
        for j in range(len(dataPost)):
            InPre.append(dataPre[j][0])
            InPost.append(dataPost[j][0])
        plt.plot(range(max_n), InPre, label='Pre')
        plt.plot(range(max_n), InPost, label='Post')
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

    inputPre = ['polya_ppheur_deg_pre_10N_50sim.csv', 'polya_ppheur_close_pre_10N_50sim.csv', 'polya_ppheur_close_pre_10N_50sim.csv',
        'polya_ppuni_pre_10N_50sim.csv','polya_pprand_pre_10N_50sim.csv']
    inputPost = ['polya_ppheur_deg_post_10N_50sim.csv', 'polya_ppheur_close_post_10N_50sim.csv', 'polya_ppheur_close_post_10N_50sim.csv',
        'polya_ppuni_post_10N_50sim.csv','polya_pprand_post_10N_50sim.csv']
    max_n = 200
    axis = [0, max_n, 0, 1]
    p = getP('10node_proportions.csv')
    #legend = ['SIS degree centrality', 'Polya degree centrality']
    legend = ['Degree Centrality', 'Betweenness Centrality', 'Closeness Centrality', 'Uniform', 'Random']
    plot_In(inputPre, inputPost, axis, legend, max_n, p)



if __name__=='__main__':
    main()
