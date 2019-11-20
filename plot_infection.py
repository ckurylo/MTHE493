import matplotlib.pyplot as plt
import pandas as pd
import csv


def get_balls(ballName):
    g = pd.read_csv(ballName, header=None).values.tolist()
    balls = []
    for i in range(len(g)):
        RB = g[i][0].split('\t')
        RB[0] = int(RB[0])
        RB[1] = int(RB[1])
        balls.append(RB)
    return balls


def getP(ballFile):
    node_balls = get_balls(ballFile)
    ave_p = 0
    for i in range(len(node_balls)):
        ave_p += node_balls[i][0] / sum(node_balls[i])
    ave_p /= len(node_balls)
    return ave_p


def plot_In(inputF_list, case, axis_list, legend, max_n, p):


    for inputFile in inputF_list:
        data = pd.read_csv(inputFile, header=None).values.tolist()
        In = []
        for i in range(len(data)):
            In.append(data[i][0])
        plt.plot(range(max_n), In)

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
    #plt.title('Single Node Infection Diffusion into Healthy Graph, Infinite Memory')
    plt.show()


def main():
    #input = ['bigDEATH_fin_data.csv', 'lilDEATH_fin_data.csv']
    input = ['CaseA_polya_inf_mem.csv', 'CaseA_polya_finite_mem.csv']
    max_n = 1000
    axis = [0, max_n, 0.4, 1]
    p = getP('ball_proportions_100_nodes.csv')
    case = 'a'
    #legend = ['Central Node', 'Peripheral Node', 'Average $ \\rho$']
    legend = ['Infinite Memory Polya', 'Memory 50 Polya', 'SIS average',  'Average $ \\rho$']

    plot_In(input, case, axis, legend, max_n, p)



if __name__=='__main__':
    main()
