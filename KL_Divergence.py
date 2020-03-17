
import csv
import pandas as pd
import math
import matplotlib.pyplot as plt


def computeKLdiv(polya, sis):

    #D(polya||SIS)
    div = 0
    div_arr = []
    for i in range(len(polya)):

        div = polya[i]*math.log2(polya[i] / sis[i]) + (1-polya[i])*math.log2((1-polya[i]) / (1-sis[i]))

        div_arr.append(div)

    return div_arr

def main():

    polya_data = pd.read_csv("plot_data/CaseA_polya_finite_mem.csv", usecols=[1]).as_matrix().transpose()[0]

    SIS_data = pd.read_csv("plot_data/SIS_data.csv", nrows=1, header=None).as_matrix()[0]

    print(SIS_data)
    print(polya_data)

    KL_div = computeKLdiv(polya_data, SIS_data)

    plt.plot(KL_div)
    plt.plot(polya_data)
    plt.plot(SIS_data)
    plt.show()

if __name__=='__main__':
    main()