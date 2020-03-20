import csv
import pandas as pd


def avg_single_metric(metric_i, fileName, fileDirectory):
    data = pd.read_csv(fileDirectory + fileName, header=None).values.tolist()
    max_n = len(data[0])
    avg = 0
    for i in range(max_n):
        avg += data[metric_i][i]
    print(avg/max_n)


