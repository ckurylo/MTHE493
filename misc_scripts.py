import csv
import pandas as pd


def avg_single_metric(metric_i, fileName, fileDirectory):
    data = pd.read_csv(fileDirectory + fileName, header=None).values.tolist()
    max_n = len(data[0])
    avg = 0
    for i in range(max_n):
        avg += data[i][metric_i]
    print(avg/max_n)



fileN = 'polya_pre_grad_10N_barabasi_10N_uni_proportions_2sim_prepost_time_dilation.csv_vaccine_waste_cpu2.csv'
fileD = 'data/to_merge/prepost/vaccine_waste_time_dilation/'
avg_single_metric(3, fileN, fileD)