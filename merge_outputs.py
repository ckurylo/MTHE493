import csv
import pandas as pd


def ave_metrics(inputF_list, inputDirectory, outputFileName, outputDirectory):
    In = []
    Sn = []
    Un = []
    Wn = []
    num_files = len(inputF_list)
    data = pd.read_csv(inputDirectory + inputF_list[0], header=None).values.tolist()
    simTime = data[0][4]/num_files
    max_n = len(data)
    for i in range(max_n):
        In.append(data[i][0]/num_files)
        Sn.append(data[i][1]/num_files)
        Un.append(data[i][2]/num_files)
        Wn.append(data[i][3]/num_files)

    for inputFile in inputF_list[1:]:
        data = pd.read_csv(inputDirectory + inputFile, header=None).values.tolist()
        simTime += data[0][4]/num_files
        for i in range(max_n):
            In[i] += data[i][0]/num_files
            Sn[i] += data[i][1]/num_files
            Un[i] += data[i][2]/num_files
            Wn[i] += data[i][3]/num_files

    new_metrics = [[In[0], Sn[0], Un[0], Wn[0], simTime]]
    for i in range(max_n)[1:]:
        new_metrics.append([In[i], Sn[i], Un[i], Wn[i]])

    with open(outputDirectory + outputFileName, "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(new_metrics)


inputDirectory = 'demo_files/'
inputL = ['polya_pre_uni_6N_bridge_6node_proportion_1sim_ini3_demo.csv',
          'polya_pre_uni_6N_bridge_ball_prop_demo_2sim_ini3_demo.csv']
output = 'merge_demo_output.csv'
outputDirectory = 'demo_files/'
ave_metrics(inputL, inputDirectory, output, outputDirectory)