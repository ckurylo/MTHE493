import csv



def ini_to_ini_file(predraw_factor, max_n, m_mem, B, deltaR, fileName):
    myStr = 'Predraw_factor: ' + str(predraw_factor) + '\n'
    myStr += 'Max_n: ' + str(max_n) + '\n'
    myStr += 'Markov Memory: ' + str(m_mem) + '\n'
    myStr += 'Budget: ' + str(B) + '\n'
    myStr += 'deltaR: ' + str(deltaR) + '\n'

    with open(fileName, "w+") as my_file:
        writer = open(my_file)
        writer.writelines(myStr)





def graph_to_string(num_sim, opt_method, num_nodes, graph_type, ini):
    myStr = ''
    if opt_method[2] == 0:
        myStr += 'pre_'
    if opt_method[2] == 1:
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
    myStr += str(num_nodes) + 'N_' + str(graph_type) + '_' + str(num_sim) + '_' + str(ini) + '.csv'
    return myStr



