import network_polya as polya
import pandas as pd
import numpy
import csv

'''
topologys = ['bridge', 'cycle', 'star', 'stick']
initialDist = ['Conc1', 'Conc3', 'uni']
heuristic_methods = ['deg', 'close', 'bet', 'perc']

for top in topologys:
    for method in heuristic_methods:
        initialDist = ['Conc1', 'Conc3', 'uni']
        dist1filename = 'SIS_Polya_Testing/6Nodes/polya_pre_heur_{opt}_6N_{top}_B12_R2_M5_{dist}.csv'.format(top=top, dist=initialDist[0], opt=method)
        dist2filename = 'SIS_Polya_Testing/6Nodes/polya_pre_heur_{opt}_6N_{top}_B12_R2_M5_{dist}.csv'.format(top=top, dist=initialDist[1], opt=method)
        dist3filename = 'SIS_Polya_Testing/6Nodes/polya_pre_heur_{opt}_6N_{top}_B12_R2_M5_{dist}.csv'.format(top=top, dist=initialDist[2], opt=method)
        dist1 = pd.read_csv(dist1filename, header=None).values.tolist()
        dist2 = pd.read_csv(dist2filename, header=None).values.tolist()
        dist3 = pd.read_csv(dist3filename, header=None).values.tolist()
        sum_metrics = [4*[0] for _ in range(len(dist1))]
        for i in range(len(dist1)):
            rowd1 = dist1[i]
            rowd2 = dist2[i]
            rowd3 = dist3[i]
            for j in range(4):
                sum_metrics[i][j] = (rowd1[j] + rowd2[j] + rowd3[j])/3
        print(' '+ top + ' ' + method)
        print(sum_metrics)
        sum_metrics[0].append((dist1[0][4]+dist2[0][4]+dist3[0][4])/3)
        outputFile = 'SIS_Polya_Testing/6Nodes/polya_pre_heur_{opt}_6N_{top}_B12_R2_M5_{dist}.csv'.format(top=top, dist='avg', opt=method)
        with open(outputFile, "w+") as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(sum_metrics)

'''

heuristic_methods = ['deg', 'close', 'bet', 'perc', 'eigen']
initialDist = ['Conc1', 'Conc3', 'uni']
top = 'dendrimer'
for method in heuristic_methods:
    dist1filename = 'SIS_Polya_Testing/10Nodes/polya_pre_unweighted_heur_{opt}_10N_{top}_B12_R2_M5_{dist}.csv'.format(top=top, dist=initialDist[0], opt=method)
    dist2filename = 'SIS_Polya_Testing/10Nodes/polya_pre_unweighted_heur_{opt}_10N_{top}_B12_R2_M5_{dist}.csv'.format(top=top, dist=initialDist[1], opt=method)
    dist3filename = 'SIS_Polya_Testing/10Nodes/polya_pre_unweighted_heur_{opt}_10N_{top}_B12_R2_M5_{dist}.csv'.format(top=top, dist=initialDist[2], opt=method)
    dist1 = pd.read_csv(dist1filename, header=None).values.tolist()
    dist2 = pd.read_csv(dist2filename, header=None).values.tolist()
    dist3 = pd.read_csv(dist3filename, header=None).values.tolist()
    sum_metrics = [4*[0] for _ in range(len(dist1))]
    for i in range(len(dist1)):
        rowd1 = dist1[i]
        rowd2 = dist2[i]
        rowd3 = dist3[i]
        for j in range(4):
            sum_metrics[i][j] = (rowd1[j] + rowd2[j] + rowd3[j])/3
    sum_metrics[0].append((dist1[0][4]+dist2[0][4]+dist3[0][4])/3)
    outputFile = 'SIS_Polya_Testing/10Nodes/polya_pre_unweighted_heur_{opt}_10N_{top}_B12_R2_M5_{dist}.csv'.format(top=top, dist='avg', opt=method)
    with open(outputFile, "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(sum_metrics)            