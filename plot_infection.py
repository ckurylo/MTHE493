import matplotlib.pyplot as plt
import pandas as pd
import csv
import os
import numpy as np


def get_balls(ballName):
    g = pd.read_csv('ball_proportion_files/' + ballName, header=None).values.tolist()
    balls = []
    for i in range(len(g)):
        BR = g[i][0].split('\t')
        BR[0] = int(float(BR[0]))
        BR[1] = int(float(BR[1]))
        balls.append(BR)
    return balls


def getP(ballFile):
    node_balls = get_balls(ballFile)
    ave_p = 0
    for i in range(len(node_balls)):
        ave_p += node_balls[i][1] / sum(node_balls[i])
    ave_p /= len(node_balls)
    return ave_p


def dilation_input():
    if get_user_input('input manually? (y/n)') == 'y':
        inputDirectory = get_user_input('input directory (use / for backslash, end in /)')
        pre_file = os.path.splitext(get_user_input('pre draw fileName to shorten and plot'))[0] + '.csv'
        post_file = os.path.splitext(get_user_input('post draw fileName for plot reference'))[0] + '.csv'
    else:
        inputDirectory = 'SIS_Polya_Testing/sim_outputs/'
        pre_file = 'pre_grad_6N_center_20sim_ini2.csv'
        post_file = 'post_grad_6N_center_50sim_ini2.csv'
    title = get_user_input('Figure title:')

    metric_i = int(get_user_input('Metric to plot (In: 0, Sn: 1, Un: 2, Wn: 3, other: 4)'))
    xlabel = 'Time (n)'
    if metric_i == 0:
        ylabel = 'Infection Rate $\\tilde{I}_n$'
    elif metric_i == 1:
        ylabel = 'Super Urn Proportion $\\tilde{S}_n$'
    elif metric_i == 2:
        ylabel = 'Urn Proportion $\\tilde{U}_n$'
    elif metric_i == 3:
        ylabel = 'Vaccine Waste $\\tilde{W}_n$'
    else:
        metric_i = 0
        xlabel = get_user_input('xlabel')
        ylabel = get_user_input('ylabel')
    label = [xlabel, ylabel]

    # user input axis or hard code in
    if get_user_input('Input axis bounds? (y/n)') == 'y':
        x1 = int(get_user_input('x axis lower bound'))
        x2 = int(get_user_input('x axis upper bound'))
        y1 = int(get_user_input('y axis lower bound'))
        y2 = int(get_user_input('y axis upper bound'))
        axis = [x1, x2, y1, y2]
    else:
        axis = [0, 10, 0, 1]  # hard code in

    legend = []
    if get_user_input('Input legend? (y/n)') == 'y':
        for i in range(2): legend.append(get_user_input('entry ' + str(i + 1)))
    else:  # hard code in
        legend = []

    p = 0
    plot_p = get_user_input('Plot average initial infection? (y/n)')
    if plot_p == 'y':
        legend.append('Average $ \\rho$')

        read_input = get_user_input('read ball prop files from directory? (y/n)')
        if read_input == 'y':
            while True:
                try:
                    ballDirectory = get_user_input('Enter ball prop directory within ball_proportion_files '
                                                   '(use / for backslash, and end with /)')
                    ballPropL = os.listdir('ball_proportion_files/' + ballDirectory)
                    break
                except FileNotFoundError:
                    print('folder not found')
        else:  # hard code in
            ballPropL = ['6N_uni_proportions.csv']

        for ballFile in ballPropL:
            try:
                p += getP(ballDirectory + ballFile)
            except FileNotFoundError:
                print('something went wrong')
                plot_p = False
                break
        p /= len(ballPropL)

    try:
       plot_dilation(inputDirectory, pre_file, post_file, metric_i, title, label, axis, legend, p, plot_p)
    except FileNotFoundError:
        print('something went wrong')


def plot_dilation(inputDirectory, pre_file, post_file, metric_i, title, label, axis_list, legend, p, plot_p):
    pre_data = pd.read_csv(inputDirectory + pre_file, header=None).values.tolist()
    post_data = pd.read_csv(inputDirectory + post_file, header=None).values.tolist()

    pre_In = []
    pre_max_n = len(pre_data)
    post_In = []
    post_max_n = len(post_data)

    for i in range(pre_max_n):
        pre_In.append(pre_data[i][metric_i])
    plt.plot(np.linspace(0, post_max_n, num=pre_max_n, endpoint=False).tolist(), pre_In)
    for i in range(post_max_n):
        post_In.append(post_data[i][metric_i])
    plt.plot(range(post_max_n), post_In)

    if plot_p == 'y': plt.plot([0, post_max_n], [p, p], 'r--')

    plt.axis(axis_list)
    plt.xlabel(label[0])
    plt.ylabel(label[1])
    plt.legend(legend)
    plt.title(title)
    plt.show()

def plot_In(inputF_list, inputDirectory, metric_i, case, title, label, axis_list, legend, p, plot_p, plot_SIS):


    for inputFile in inputF_list:
        data = pd.read_csv(inputDirectory + inputFile, header=None).values.tolist()
        In = []
        max_n = len(data)
        for i in range(max_n):
            In.append(data[i][metric_i])
        plt.plot(range(max_n), In)

    if plot_SIS:
        SIS = pd.read_csv('SIS_data.csv', header=None).values.tolist()
        if case == 'a':
            plt.plot(range(len(SIS[0])), SIS[0], 'k')
        elif case == 'b':
            plt.plot(range(len(SIS[1])), SIS[1], 'k')
        elif case == 'c':
            plt.plot(range(len(SIS[2])), SIS[2], 'k')

    if plot_p == 'y': plt.plot([0, max_n], [p, p], 'r--')

    plt.axis(axis_list)
    plt.xlabel(label[0])
    plt.ylabel(label[1])
    plt.legend(legend)
    plt.title(title)
    plt.show()


def get_user_input(prompt):
    print(prompt + ':', end='\t')
    return input()

def main():

    if get_user_input('doing any time dilation stuff? (y/n)') == 'y':
        dilation_input()
    #  Either read all files in a directory or hard code in your inputFile list (under else)
    read_input = get_user_input('Plot all files in a given directory? (y/n)')
    if read_input == 'y':
        while True:
            try:
                inputDirectory = get_user_input('Enter input folder directory (use / for backslash, and end with /)')
                inputL = os.listdir(inputDirectory)
                break
            except FileNotFoundError:
                print('folder not found')
    else:
        inputL = ['democrat.csv']

    case = 'a'
    if get_user_input('Plot SIS too? (y/n)') == 'y':
        plot_SIS = True
    else: plot_SIS = False

    title = get_user_input('Figure title:')

    metric_i = int(get_user_input('Metric to plot (In: 0, Sn: 1, Un: 2, Wn: 3, other: 4)'))
    xlabel = 'Time (n)'
    if metric_i == 0:
        ylabel = 'Infection Rate $\\tilde{I}_n$'
    elif metric_i == 1:
        ylabel = 'Super Urn Proportion $\\tilde{S}_n$'
    elif metric_i == 2:
        ylabel = 'Urn Proportion $\\tilde{U}_n$'
    elif metric_i == 3:
        ylabel = 'Vaccine Waste $\\tilde{W}_n$'
    else:
        metric_i = 0
        xlabel = get_user_input('xlabel')
        ylabel = get_user_input('ylabel')
    label = [xlabel, ylabel]

    # user input axis or hard code in
    if get_user_input('Input axis bounds? (y/n)') == 'y':
        x1 = int(get_user_input('x axis lower bound'))
        x2 = int(get_user_input('x axis upper bound'))
        y1 = int(get_user_input('y axis lower bound'))
        y2 = int(get_user_input('y axis upper bound'))
        axis = [x1, x2, y1, y2]
    else: axis = [0, 10, 0, 1]  # hard code in

    legend = []
    if get_user_input('Input legend? (y/n)') == 'y':
        for i in range(len(inputL)): legend.append(get_user_input('entry ' + str(i+1)))
    else: # hard code in
        legend = []

    p = 0
    plot_p = get_user_input('Plot average initial infection? (y/n)')
    if plot_p == 'y':
        legend.append('Average $ \\rho$')

        read_input = get_user_input('read ball prop files from directory? (y/n)')
        if read_input == 'y':
            while True:
                try:
                    ballDirectory = get_user_input('Enter ball prop directory within ball_proportion_files '
                                               '(use / for backslash, and end with /)')
                    ballPropL = os.listdir('ball_proportion_files/' + ballDirectory)
                    break
                except FileNotFoundError:
                    print('folder not found')
        else:  # hard code in
            ballPropL = ['6N_uni_proportions.csv']

        for ballFile in ballPropL:
            try:
                p += getP(ballDirectory + ballFile)
            except FileNotFoundError:
                print('something went wrong')
                plot_p = False
                break
        p /= len(ballPropL)

    try:
        plot_In(inputL, inputDirectory, metric_i, case, title, label, axis, legend, p, plot_p, plot_SIS)
    except FileNotFoundError:
        print('something went wrong')


if __name__=='__main__':
    main()
