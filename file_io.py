def ini_to_ini_file(predraw_factor, max_n, m_mem, B, deltaR, fileName):
    myStr = 'Predraw_factor:\t' + str(predraw_factor) + '\n'
    myStr += 'Max_n:\t' + str(max_n) + '\n'
    myStr += 'Markov Memory:\t' + str(m_mem) + '\n'
    myStr += 'Budget:\t' + str(B) + '\n'
    myStr += 'deltaR:\t' + str(deltaR) + '\n'
    writer = open(fileName, 'w+')
    writer.writelines(myStr)


def ini_file_to_ini(fileName):
    with open(fileName, 'r') as my_file:
        iniStr = my_file.readlines()
    iniList = []
    for myStr in iniStr:
        iniList.append(int(myStr.split('\t')[1].strip('\n')))
    return iniList



def graph_to_string(num_sim, opt_method, num_nodes, graph_type, ini, ballProp):
    myStr = 'polya_'
    if opt_method[2] == 0:
        myStr += 'pre_'
    else:
        myStr += 'post_'

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
    myStr += str(num_nodes) + 'N_' + str(graph_type) + '_' + ballProp + '_' + str(num_sim) + 'sim_' + str(ini) + '.csv'
    return myStr


# predraw_factor = 1
# max_n = 1000
# m_mem = 10
# B = 50
# deltaR = 3
# fileName = 'lul_xd.txt'
#
# ini_to_ini_file(predraw_factor, max_n, m_mem, B, deltaR, fileName)
# print(ini_file_to_ini(fileName))
#
# num_sim = 50
# opt_method = [3,2,1]
# num_nodes = 10
# graph_type = 'stick'
# ini = 'ini1'
#
# print(graph_to_string(num_sim, opt_method, num_nodes, graph_type, ini))
