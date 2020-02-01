import numpy as np
import math
import sympy as sym
from sympy.parsing.sympy_parser import parse_expr
import csv
import matplotlib.pyplot as plt


def Sn_function(N):
    myString = ''
    with open('Sn_function_10N.csv', 'r') as csvfile:
        Sn_reader = csv.reader(csvfile, delimiter=',')
        for row in Sn_reader:
            for c in row:
                myString += c
    xN = sym.symbols('x0:%d' % (N))
    xN_dict = dict((str(x), x) for x in xN)
    f_n = parse_expr(myString, xN_dict)

    return xN, f_n


def gradient(N, T, B):
    y = [[] for i in range(T+1)]
    y[0] = [1 for i in range(N)]
    y_bar = y[:][:]
    xN, f_n = Sn_function(N)
    f_partials = sym.derive_by_array(f_n, xN)

    # f_part_def = [f_partials[i].subs([(xN[j], 1) for j in range(N)]) for i in range(N)]
    # index = np.argmin(f_part_def)

    for k in range(T):
        print('\r'+str(k+1), end='')
        #
        f_part_def = [f_partials[i].subs([(xN[j], y[k][j]) for j in range(N)]) for i in range(N)]
        index = np.argmin(f_part_def)
        #
        y_bar[k] = [0 for i in range(N)]
        y_bar[k][index] = B
        #
        alpha_list = [i/100 for i in range(1, 101)]
        f_def = [f_n.subs([(xN[j], y[k][j] + alpha_list[i] * (y_bar[k][j]-y[k][j])) for j in range(N)])
                 for i in range(100)]
        alpha = alpha_list[np.argmin(f_def)]
        #
        y[k+1] = [y[k][i] + alpha * (y_bar[k][i] - y[k][i]) for i in range(N)]

    return y, f_n, xN


# N = 10
# B = 25
# T = 100
#
# y, f_n, xN = gradient(N, T, B)
#
# f_def = [f_n.subs([(xN[j], y[i][j]) for j in range(N)]) for i in range(len(y))]
#
# with open('gradient_num_iteration_10N.csv', "w+") as my_csv:
#     csvWriter = csv.writer(my_csv, delimiter=',')
#     csvWriter.writerow(f_def)


f_def = [0 for i in range(101)]
with open('gradient_num_iteration_10N.csv', 'r') as csvfile:
    Sn_reader = csv.reader(csvfile, delimiter=',')
    for row in Sn_reader:
        for i in range(len(row)):
            f_def[i] = float(row[i])


plt.plot(range(len(f_def)), f_def, 'r.')
plt.axis([0, 10, 0.155, 0.19])
plt.xticks(np.arange(0, 11, step=1))
plt.xlabel('# of Iterations of Gradient Descent')
plt.ylabel('Expected Network Exposure $E[\\tilde{S}_n]$')
plt.title('Minimization of 10-dimensional Function with Gradient Descent')
plt.show()

