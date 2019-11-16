import numpy
import networkx as nx
import matplotlib.pyplot as plt

#####
# CONSTANTS
MARKOV_MEMORY = 3

# Single Urn class, parent of SuperUrn class
class Urn:
    def __init__(self, key, R, B, M):
        self.key = key
        self.R = R  # initial number of Red balls
        self.B = B  # initial number of Black balls
        self.T = R + B  # initial Total number of balls
        self.delta = M*[0]  # ball replacement number
        self.M = M  # memory of the system
        self.Zn = M*[0]   # stoch process indicator for black or red draw at time n, only need M previous draw info
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
    def __init__(self, key, R, B, M, G):
        super().__init__(key, R, B, M)  # initialize parent urn class
        self.Graph = G  # graph the superUrn is part of
        self.Ni_key = [key] + list(nx.all_neighbors(G, key))  # list of node neighbours' keys
        # these next variables may not be set until whole network is defined
        self.Ni_list = []
        self.super_R = 0
        self.super_B = 0
        self.super_T = 0
        self.Sm = []

    def setInitialVariables(self):  # these variables are initialized after the whole network is initialized
        for i in self.Ni_key:  # parse through node neighbour keys
            self.Ni_list.append(self.Graph.nodes[i]['superUrn'])  # set list of neighbour pointers
            self.super_R += self.Graph.nodes[i]['superUrn'].R  # find initial # of red balls in super urn
            self.super_B += self.Graph.nodes[i]['superUrn'].B  # find initial # of black balls in super urn
        self.super_T = self.super_R + self.super_B  # set initial # of total balls in super urn
        self.Sm = [self.super_R/self.super_T, 0]  # set initial super urn proportion

    def drawBall(self):  # draw ball from Super Urn
        Z = numpy.random.choice([0, 1], p=[(1 - self.Sm[0]), self.Sm[0]])  # draw red or black ball
        self.Zn.pop()  # get rid of (n-M-1)th draw (since finite M memory)
        self.Zn.insert(0, Z)  # insert nth draw info

    def nextSm(self):  # calculate next draw proportion
        nominator = 0
        denominator = 0
        for urn in self.Ni_list:
            # multiply single urn red ball proportion by single urn total # of balls, for every neighbour
            nominator += urn.Um[0] * (urn.T + sum(urn.delta))
            # total # of balls for every neighbour
            denominator += urn.T + sum(urn.delta)
        self.Sm.pop()
        self.Sm.insert(0, nominator/denominator)  # update Sm


def createPolyaNetwork(n, m, R, B):  # generates graph and creates urns at every node
    G = nx.barabasi_albert_graph(n, m)  # generate random graph with n nodes, each with average of m connections
    for i in range(len(list(G.nodes))):  # set urn at every node
        G.nodes[i]['superUrn'] = SuperUrn(i, R, B, MARKOV_MEMORY, G)
    for i in range(len(list(G.nodes))):  # initialize network variables at every node
        G.nodes[i]['superUrn'].setInitialVariables()
    return G


def networkTimeStep(G, delta):  # increment time and proceed to next step in network draw process
    for i in range(len(list(G.nodes))):
        G.nodes[i]['superUrn'].drawBall()
        G.nodes[i]['superUrn'].nextDelta(delta)
        G.nodes[i]['superUrn'].nextU()
        G.nodes[i]['superUrn'].nextSm()


def printNetwork(G, t):  # print network attributes
    print('--- Time: ' + str(t) + ' --------------------')
    for i in range(len(list(G.nodes))):
        superUrn = G.nodes[i]['superUrn']
        print("|| Urn " + str(superUrn.key) + ", U_n = {:.2%}, ".format(superUrn.Sm[1]), end='')
        if superUrn.Zn[0] == 1:  # print last ball draw
            print("Draw : Red\t", end='')
        else:
            print("Draw : Black\t", end='')
    print('\n', end='')


def network_simulation(R, B, delta, M, max_n, num_nodes, num_connections):
    polya_network = createPolyaNetwork(num_nodes, num_connections, R, B)  # create network of urns
    for n in range(max_n):  # run simulation for max_n steps
        networkTimeStep(polya_network, delta)  # proceed to next step in draw process
        printNetwork(polya_network, n)  # print network attributes

    printGraph(polya_network)  # print graph for reference


def printGraph(G):  # prints a plot of the network for reference
    nx.draw(G, cmap=plt.get_cmap('viridis'), with_labels=True, font_color='white')
    plt.show()


# def polya_simulation(R, B, delta, M, max_n):
#
#     polyaUrn = Urn(1, R, B, M)
#     print("-----------------")
#     for n in range(max_n):  # run simulation for max_n total draws
#         polyaUrn.timeStep(delta)
#         polyaUrn.print_current_n()


#######################################
# PARAMETER INPUT
R = 10
B = 5
deltaB = 2
deltaR = 2
delta = [deltaB, deltaR]
M = MARKOV_MEMORY
max_n = 10
num_nodes = 7
num_connections = 3
network_simulation(R, B, delta, M, max_n, num_nodes, num_connections)



