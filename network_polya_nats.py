import numpy
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib import animation
from matplotlib.animation import FuncAnimation
from celluloid import Camera
import matplotlib
import OptimizationMethods as opt
#matplotlib.use('Agg')


#####
# CONSTANTS
def defConstants(m, b, d, tenacity):
    global MARKOV_MEMORY
    MARKOV_MEMORY = m
    global BUDGET
    BUDGET = b
    global DELTA_R
    DELTA_R = d
    global TENACITY
    TENACITY = tenacity

# Single Urn class, parent of SuperUrn class
class Urn:
    def __init__(self, key, R, B):
        self.key = key
        self.R = R  # initial number of Red balls
        self.B = B  # initial number of Black balls
        self.T = R + B  # initial Total number of balls
        self.delta = MARKOV_MEMORY*[0]  # ball replacement number
#        self.M = MARKOV_MEMORY  # memory of the system
        self.Zn = MARKOV_MEMORY*[0]   # stoch process indicator for black or red draw at time n, only need M previous draw info
        self.Um = [R/(R+B), 0]  # red ball proportion in the urn, only ever need the value before and after each draw
        self.n = 0  # time

    # THIS METHOD FROM SINGLE URN SIMULATIONS, DON'T USE
    # def timeStep(self, delta):  # execute next draw in process
    #     self.n += 1  # increment time
    #     self.nextZ()
    #     self.nextDelta(delta)
    #     self.nextU()
    # THIS METHOD FROM SINGLE URN SIMULATIONS, DON'T USE
    # def nextZ(self):
    #     Z = numpy.random.choice([0, 1], p=[(1-self.Um[0]), self.Um[0]])  # draw red or black ball
    #     self.Zn.pop()  # get rid of (n-M-1)th draw (since finite M memory)
    #     self.Zn.insert(0, Z)  # insert nth draw info

    def nextDelta(self, delta):  # updates the list of last M delta, based on last draw
        self.delta.pop()
        if self.Zn[0] == 0:
            self.delta.insert(0, delta[0])
        else:
            self.delta.insert(0, delta[1])

    def nextU(self):  # calculates next (single) urn proportion based on last draw
        U = (self.R + numpy.dot(self.delta, self.Zn)) / (self.T + sum(self.delta))
        self.Um.pop()  # get rid of n-2 time ball proportion
        self.Um.insert(0, U)  # insert n time ball proportion

    def get_Z_m(self):  # return the number of red balls added to urn in last M draws
        return numpy.dot(self.delta, self.Zn)

    # THIS METHOD FROM SINGLE URN SIMULATIONS, DON'T USE
    # def print_current_n(self):  # print urn attributes for current time step
    #     print("Time:", self.n)  # print time
    #     print("Prob of drawing Red at this time : {:.2%}".format(self.Um[1]))  # print pre-draw proportion (ie prob)
    #     if self.Zn[0] == 1:  # print last ball draw
    #         print("Draw : Red")
    #     else:
    #         print("Draw : Black")
    #     print("-----------------------------")

# SuperUrn class, child class of Urn
class SuperUrn(Urn):
    def __init__(self, key, R, B, G):
        super().__init__(key, R, B)  # initialize parent urn class
        self.Graph = G  # graph the superUrn is part of
        self.Ni_key = list(nx.all_neighbors(G, key))  # list of node neighbours' keys
        # these next variables may not be set until whole network is defined
        self.Ni_list = []
        self.Ni_weight = [TENACITY] + [G.adj[key][i]['weight'] for i in self.Ni_key]
        self.Ni_key.insert(0, key)
        self.super_R = 0
        self.super_B = 0
        self.super_T = 0
        self.Sm = []

    def setInitialVariables(self):  # these variables are initialized after the whole network is initialized
        k = 0
        for i in self.Ni_key:  # parse through node neighbour keys
            self.Ni_list.append(self.Graph.nodes[i]['superUrn'])  # set list of neighbour pointers
            self.super_R += self.Ni_weight[k] * self.Graph.nodes[i]['superUrn'].R  # find initial # of red balls in super urn
            self.super_B += self.Ni_weight[k] * self.Graph.nodes[i]['superUrn'].B  # find initial # of black balls in super urn
            k += 1
        self.super_T = self.super_R + self.super_B  # set initial # of total balls in super urn
        self.Sm = [self.super_R/self.super_T, 0]  # set initial super urn proportion

    def drawBall(self):  # draw ball from Super Urn
        Z = numpy.random.choice([0, 1], p=[(1 - self.Sm[0]), self.Sm[0]])  # draw red or black ball
        self.Zn.pop()  # get rid of (n-M-1)th draw (since finite M memory)
        self.Zn.insert(0, Z)  # insert nth draw info

    def nextSm(self):  # calculate next draw proportion
        nominator = 0
        denominator = 0
        for i in range(len(self.Ni_list)):
            # multiply single urn red ball proportion by single urn total # of balls, for every neighbour, with weight
            nominator += self.Ni_weight[i] * self.Ni_list[i].Um[0] * (self.Ni_list[i].T + sum(self.Ni_list[i].delta))
            # total # of balls for every neighbour
            denominator += self.Ni_weight[i] * ( self.Ni_list[i].T + sum(self.Ni_list[i].delta) )
        self.Sm.pop()
        self.Sm.insert(0, nominator/denominator)  # update Sm


def createPolyaNetwork(adjFile, node_balls):  # generates graph and creates urns at every node
    G = importGraph(adjFile)

    for i in range(len(list(G.nodes))):  # set urn at every node
        B = node_balls[i][0]
        R = node_balls[i][1]
        G.nodes[i]['superUrn'] = SuperUrn(i, R, B, G)
    for i in range(len(list(G.nodes))):  # initialize network variables at every node
        G.nodes[i]['superUrn'].setInitialVariables()

    return G


def getDelta(G, deployment_method):
    if deployment_method[0] == 1:
        deltaB = opt.evenDistribution(G.number_of_nodes(), BUDGET)
    elif deployment_method[0] == 2:
        deltaB = opt.randomDistribution(G.number_of_nodes(), BUDGET)
    elif deployment_method[0] == 3:
        S = []
        N = numNeighbors(G)
        C = centralityCalculation(G, deployment_method[1])
        for i in G.nodes:
            S.append(G.nodes[i]['superUrn'].Sm[0])
        deltaB = opt.heuristic(G.number_of_nodes(), BUDGET, N, C, S)
    elif deployment_method[0] == 4:
        deltaB = opt.gradient(G, deployment_method[1], deployment_method[2], BUDGET, DELTA_R)
    deltaR = G.number_of_nodes()*[DELTA_R]
    return [deltaB, deltaR]


def networkTimeStep(G, opt_method):  # increment time and proceed to next step in network draw process
    state_vector = []
    if opt_method[0] != 4 or opt_method[2] == 0:  # get vaccine deployment if pre-draw optimization
        delta = getDelta(G, opt_method)
    for i in G.nodes:
        G.nodes[i]['superUrn'].drawBall()
    if opt_method[0] == 4 and opt_method[2] == 1:  # get vaccine deployment if post-draw optimization
        delta = getDelta(G, opt_method)
    for i in G.nodes:
        G.nodes[i]['superUrn'].nextDelta([delta[0][i], delta[1][i]])
        G.nodes[i]['superUrn'].nextU()
        G.nodes[i]['superUrn'].nextSm()
        state_vector.append(G.nodes[i]['superUrn'].Zn)
    return state_vector


def diseaseMetrics(G, state_vector):
    N = len(list(G.nodes))
    # average of all red balls pulled  = infection rate
    state_sum = sum(row[0] for row in state_vector)
    I_n = (1/N)*state_sum

    r_tot_Sn = 0
    for i in G.nodes:
        r_tot_Sn = r_tot_Sn + G.nodes[i]['superUrn'].Sm[0]

    # average red balls in network
    S_n = (1/N)*r_tot_Sn

    rho_tot = 0
    for i in G.nodes:
        rho_tot = rho_tot + G.nodes[i]['superUrn'].Um[0]

    # average of proportion of infection across network
    U_n = (1/N)*rho_tot
    metrics = [I_n, S_n, U_n]
    return metrics


def printNetwork(G, t,v,m):  # print network attributes
    print('--- Time: ' + str(t) + ' --------------------')
    for i in G.nodes:
        superUrn = G.nodes[i]['superUrn']
        print("|| Urn " + str(superUrn.key) + ", U_n = {:.2%}, ".format(superUrn.Sm[0]), end='')
        if superUrn.Zn[0] == 1:  # print last ball draw
            print("Draw : Red\t", end='')
        else:
            print("Draw : Black\t", end='')
    print('\n', end='')
    print("Network infection rate: {:.2%}".format(m[0]), end='\n')
    print("Avg Network Infection: {:.2%}".format(m[1]), end='\n')
    print("Network Susceptibility: {:.2%}".format(m[2]), end='\n')


def network_simulation(adjFile, delta, M, max_n, node_balls, opt_method, tenacity):
    defConstants(M, delta[0], delta[1], tenacity)

    polya_network = createPolyaNetwork(adjFile, node_balls)  # create network of urns
    #infection_data = {}
    disease_metrics = []
    print('\npolya time:')
    for n in range(max_n):  # run simulation for max_n steps
        print('\r'+str(n+1), end='')
        v = networkTimeStep(polya_network, opt_method)  # proceed to next step in draw process
        m = diseaseMetrics(polya_network, v)
        disease_metrics.append(m)
        #infection_data[n] = {}
        #for node in polya_network.nodes:
            #infection_data[n][node] = polya_network.nodes[node]['superUrn'].Um[1]
        # printNetwork(polya_network, n,v,m)  # print network attributes
    #update_graph(polya_network, infection_data)

    return disease_metrics

#    colour = recolourGraph
#   printGraph(polya_network, colour)  # print graph for reference

def update_graph(G, data):
    fig = plt.figure()
    camera = Camera(fig)
    layout = nx.spring_layout(G)
    colour_map = {}
    print(data)
    for n in data:
        colour_map[n] = []
        for i in data[n]:
            if data[n][i] > 0.8:
                colour_map[n].append('red')
            elif 0.6 < data[n][i] <= 0.8:
                colour_map[n].append('orange')
            elif 0.4 < data[n][i] <= 0.6:
                colour_map[n].append('yellow')
            elif 0.2 < data[n][i] <= 0.4:
                colour_map[n].append('green')
            else:
                colour_map[n].append('green')

        nx.draw(G, node_color=colour_map[n], pos=layout, node_size=30, width=0.25)
        plt.draw()
        camera.snap()

    new = camera.animate()
    new.save('animation_1.html')
    print('i made it')

#def printGraph(G, c):  # prints a plot of the network for reference

#
# def polya_simulation(R, B, delta, M, max_n):
#
#     polyaUrn = Urn(1, R, B, M)
#     print("-----------------")
#     for n in range(max_n):  # run simulation for max_n total draws
#         polyaUrn.timeStep(delta)
#         polyaUrn.print_current_n()

def centralityCalculation(G, cent_mes):

    deg_centrality = nx.degree_centrality(G)
    deg_cent = [k for k in deg_centrality.values()]
    close_centrality = nx.closeness_centrality(G)
    perc_cent = percolation(G)
    close_cent = [k for k in close_centrality.values()]
    #print(deg_centrality)
    bet_centrality = nx.betweenness_centrality(G, normalized = True, endpoints = False)
    bet_cent = [k for k in bet_centrality.values()]
    #print(deg_centrality)
    if cent_mes == 1:
        return deg_cent
    elif cent_mes == 2:
        return close_cent
    elif cent_mes == 3:
        return perc_cent
    else:
        return bet_cent

def percolation(G):
    balldict = {}

    for node in G.nodes:
        balldict[node] = G.nodes[node]['superUrn'].Um[0]

    centrality = nx.percolation_centrality(G, states = balldict)

    return centrality

def numNeighbors(G):
    neighbors = [len(list(G.neighbors(n))) for n in G]
    return neighbors

def importGraph(adjFile):
    bigG = nx.from_numpy_matrix(pd.read_csv(adjFile, header=None).as_matrix())
    return bigG
#######################################
# PARAMETER INPUT


def get_balls(ballName):
    g = pd.read_csv(ballName, header=None).values.tolist()
    balls = []
    for i in range(len(g)):
        BR = g[i][0].split('\t')
        BR[0] = int(BR[0])
        BR[1] = int(BR[1])
        balls.append(BR)

    return balls


def main():

    M = 5
    budget = 25
    deltaR = 2
    delta = [budget, deltaR]
    max_n = 50
    tenacity_factor = 1  # weight of node's own Urn in Super Urn
    adjFile = '6node.csv'
    defConstants(M, delta[0], delta[1], tenacity_factor)

    opt_method = [3, 4, 0]
    #opt_method = [2]
    network_simulation(adjFile, delta, M, max_n, get_balls('6node_proportions.csv'), opt_method, tenacity_factor)
    # opt_method: [1] for uniform vaccine deployment, [2] for random
    # [3, i] for heuristic with i = 1 for deg cent, 2 for close cent, 3 for bet cent
    # [4, T, k] for gradient descent, T the number of iterations of the algo for each time step
            # k = 0 for pre-draw optimization, k = 1 for post-draw optimization
    """
    G, cent = centralityCalculation('100_node_adj.csv')
    neigh = numNeighbors(G)
    deltaB1 = opt.evenDistribution(100, 800)
    print(deltaB1)
    deltaB2 = opt.randomDistribution(100, 800)
    print(deltaB2)
    #opt.heuristic(100, 800, N, cent, S)
    """

if __name__=='__main__':
    main()