#########################
#### File Input/Ouput Module
# Run main to create ini.txt File
#########################

import os

def ini_to_ini_file(predraw_factor, max_n, m_mem, B, deltaR, fileName):
    myStr = 'Predraw_factor:\t' + str(predraw_factor) + '\n'
    myStr += 'Max_n:\t' + str(max_n) + '\n'
    myStr += 'Markov Memory:\t' + str(m_mem) + '\n'
    myStr += 'Budget:\t' + str(B) + '\n'
    myStr += 'deltaR:\t' + str(deltaR) + '\n'
    writer = open('ini_files/'+fileName, 'w+')
    writer.writelines(myStr)


def ini_file_to_ini(fileName):
    with open('ini_files/'+fileName, 'r') as my_file:
        iniStr = my_file.readlines()
    iniList = []
    for myStr in iniStr:
        iniList.append(int(myStr.split('\t')[1].strip('\n')))
    return iniList



def graph_to_string(num_sim, opt_method, num_nodes, graph_type, ini, ballProp):
    myStr = 'polya_'
    if opt_method[2] == 0:
        myStr += 'pre_'
    elif opt_method[2] == 1:
        myStr += 'post_'
    else:
        myStr += 'optimist_'
    if opt_method[0] == 1:
        myStr += 'uni_'
    elif opt_method[0] == 2:
        myStr += 'random_'
    elif opt_method[0] == 3:
        if opt_method[1] == 1:
            myStr += 'deg_cent_'
        elif opt_method[1] == 2:
            myStr += 'close_cent_'
        elif opt_method[1] == 3:
            myStr += 'bet_cent_'
        elif opt_method[1] == 4:
            myStr += 'perc_cent_'
    else:
        myStr += 'grad_'
    myStr += str(graph_type) + '_' + ballProp + '_' + str(num_sim) + 'sim_' + str(ini) + '.csv'
    return myStr


def main():
    # PARAMETER INPUT
    iniNameList = ['Predraw Factor (for pre to post conversion)', 'Max_n', 'Markov Memory', 'Budget', 'deltaR']
    print("--------------------------------------------------------\nCREATE INI FILE\n------------------------------------"
          "--------------------\n")
    iniList = []
    for tag in iniNameList:
        while True:
            print(tag + ':', end='\t')
            A = input()
            try:
                A = int(A)
                iniList.append(A)
                break
            except ValueError:
                print("\n--Please input an integer--\n")
    while True:
        print("Please name your ini file:", end='\t')
        B = input()
        try:
            ini_fileName = str(B)
            break
        except ValueError:
            print("\n--Please input a string--\n")
    print("\n--------------------------------------------------------\n")
    ini_fileName = os.path.splitext(ini_fileName)[0] + '.txt'
    #########################################
    # Create ini file
    ini_to_ini_file(iniList[0], iniList[1], iniList[2], iniList[3], iniList[4], ini_fileName)
    print('ini file created successfully')

if __name__ == '__main__':
    main()
