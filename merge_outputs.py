import csv
import pandas as pd
import os

def get_user_input(prompt):
    print(prompt + ':', end='\t')
    return input()

def ave_metrics(inputF_list, inputDirectory, inputWeight, outputFileName, outputDirectory):
    num_sim = sum(inputWeight)
    In = []
    Sn = []
    Un = []
    Wn = []
    num_files = len(inputF_list)
    data = pd.read_csv(inputDirectory + inputF_list[0], header=None).values.tolist()
    simTime = inputWeight[0] * data[0][4]/num_sim
    max_n = len(data)
    for i in range(max_n):
        In.append(inputWeight[0] * data[i][0]/num_sim)
        Sn.append(inputWeight[0] * data[i][1]/num_sim)
        Un.append(inputWeight[0] * data[i][2]/num_sim)
        Wn.append(inputWeight[0] * data[i][3]/num_sim)

    k = 1
    for inputFile in inputF_list[1:]:
        data = pd.read_csv(inputDirectory + inputFile, header=None).values.tolist()
        simTime += inputWeight[k] * data[0][4]/num_sim
        for i in range(max_n):
            In[i] += inputWeight[k] * data[i][0]/num_sim
            Sn[i] += inputWeight[k] * data[i][1]/num_sim
            Un[i] += inputWeight[k] * data[i][2]/num_sim
            Wn[i] += inputWeight[k] * data[i][3]/num_sim
        k += 1

    new_metrics = [[In[0], Sn[0], Un[0], Wn[0], simTime]]
    for i in range(max_n)[1:]:
        new_metrics.append([In[i], Sn[i], Un[i], Wn[i]])

    with open(outputDirectory + outputFileName, "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(new_metrics)


###############################
if get_user_input('Input parameters in terminal? (y/n)') == 'y':
    inputDirectory = get_user_input('Input Directory (will merge all files in given directory, '
                                    'use / for backslash, end in /)')
    inputL = os.listdir(inputDirectory)
    inputW = []
    for i in range(len(inputL)):
        inputW.append(int(get_user_input('num_sim file ' + str(i+1))))
    outputDirectory = get_user_input('Output Directory (use / for backslash, end in /)')
    output = os.path.splitext(get_user_input('Output file name'))[0] + '.csv'
else:
    inputDirectory = 'data/to_merge/prepost/time_dilation/'
    inputL = os.listdir(inputDirectory)
    inputW = 3*[1]
    output = 'polya_pre_grad_10N_barabasi_10N_uni_proportions_100sim_prepost_time_dilation.csv'
    outputDirectory = 'PREPOST/sec_comparison/'

ave_metrics(inputL, inputDirectory, inputW, output, outputDirectory)
