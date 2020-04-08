import pandas as pd
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import math

def makeHistogram(dataset, n):
    hist = [0]*n
    delta = len(dataset) / n

    for item in dataset:
        item = item*100
        bucket = math.floor(item/delta) + 1
        hist[bucket] = hist[bucket] + 1

    return hist

def plotHist(dataset, n):

    indices = []
    i = 0
    while i <= n:

        if i % 10 == 0:
            indices.append('  ' + str(i) + '%')

        if i == 100:
            indices.append('  ' + str(i) + '%')
        i = i + 1

    tix = np.linspace(0, 100, 11)
    y_pos = np.arange(n)
    plt.bar(y_pos, dataset, align='center')
    plt.xticks(tix, indices)
    plt.ylabel('Number of Nodes')
    plt.xlabel('Proportion of Disease, Un')
    plt.title('Number of Nodes with Given Infection Rate, Percolation Centrality Heuristic')

    plt.show()

def main():
    inFile = '07peripheral_curing_pre_perc_proportions_500sim'
    g = pd.read_csv('v1/' + inFile + '.csv', header=None).values.tolist()
    props = []
    for i in range(len(g)):
        BR = g[i][0].split('\t')
        BR[0] = int(float(BR[0]))
        BR[1] = int(float(BR[1]))
        #print(BR[0])
        #print(BR[1])
        props.append(BR[1]/(BR[0] + BR[1]))


    print(np.mean(props))
    buckets = 100
    hist = makeHistogram(props, buckets)
    plotHist(hist, buckets)
    saveFile = np.asarray(hist)
    np.savetxt(inFile + '_histogram.csv', saveFile, delimiter=",")

main()