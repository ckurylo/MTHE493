import pandas as pd
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import math

def makeHistogram(dataset, n):
    hist = [0]*n
    delta = len(dataset) / n + 1
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
            indices.append(str(i) + '%')
        else:
            indices.append('')
        i = i + 1

    y_pos = np.arange(n)
    Infection = dataset

    plt.bar(y_pos, Infection, align='center', alpha=0.5)
    plt.xticks(y_pos, indices)
    plt.ylabel('# Nodes')
    plt.xlabel('Proportion of disease')
    plt.title('Number of Nodes with Given Infection Rate Closeness Centrality Heuristic')

    plt.show()

def main():
    g = pd.read_csv('04peripheral_curing_pre_close_proportions_500sim.csv', header=None).values.tolist()
    props = []
    for i in range(len(g)):
        BR = g[i][0].split('\t')
        BR[0] = int(float(BR[0]))
        BR[1] = int(float(BR[1]))
        props.append(int(float(BR[1]))/int(float(BR[0])))

    buckets = 100
    hist = makeHistogram(props, buckets)
    plotHist(hist, buckets)
    saveFile = np.asarray(hist)
    np.savetxt("histogram .csv", saveFile, delimiter=",")

main()