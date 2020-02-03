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


def plot_In(inputF_list, case, axis_list, legend, max_n, p, plot_SIS):


    for inputFile in inputF_list:
        data = pd.read_csv(inputFile, header=None).values.tolist()
        In = []
        for i in range(len(data)):
            In.append(data[i][0])
        plt.plot(range(max_n), In)

    if plot_SIS:
        SIS = pd.read_csv('SIS_data.csv', header=None).values.tolist()
        if case == 'a':
            plt.plot(range(len(SIS[0])), SIS[0], 'k')
        elif case == 'b':
            plt.plot(range(len(SIS[1])), SIS[1], 'k')
        elif case == 'c':
            plt.plot(range(len(SIS[2])), SIS[2], 'k')


    plt.plot([0, max_n], [p, p], 'r--')
    plt.axis(axis_list)
    plt.xlabel('Time (n)')
    plt.ylabel('Infection Rate $\\tilde{I}_n$')
    plt.legend(legend)
    plt.title('Curing 10-node network with Gradient Descent curing deployment')
    plt.show()


def main():
    #input = ['bigDEATH_fin_data.csv', 'lilDEATH_fin_data.csv']
    #input = ['10node_case3_degCent.csv', '10node_case3_closeCent.csv', '10node_case3_betCent.csv']
    #input = ['10node_case1.csv', '10node_case2.csv']
    input = ['10node_T1_postdraw.csv', '10node_T10_predraw.csv']
    input = ['demo.csv', 'pre_grad_10N_50sim.csv']
    max_n = 200
    axis = [0, max_n, 0, 1]
    p = getP('10node_proportions.csv')
    case = 'a'
    #legend = ['Central Node', 'Peripheral Node', 'Average $ \\rho$']
    legend = ['degree centrality', 'closeness centrality', 'betweenness centrality',  'Average $ \\rho$']
    legend = ['post draw opt', 'pre draw opt', 'Average $ \\rho$']
    #legend = []
    #legend = ['uniform distribution', 'random distribution', 'Average $ \\rho$']
    plot_In(input, case, axis, legend, max_n, p, plot_SIS = False)



if __name__=='__main__':
    main()
