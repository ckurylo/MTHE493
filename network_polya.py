import numpy
import networkx as nx
import matplotlib.pyplot as plt

#####
# CONSTANTS
MARKOV_MEMORY = 3


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

    # def timeStep(self, delta):  # execute next draw in process
    #     self.n += 1  # increment time
    #     self.nextZ()
    #     self.nextDelta(delta)
    #     self.nextU()

    # def nextZ(self):
    #     Z = numpy.random.choice([0, 1], p=[(1-self.Um[0]), self.Um[0]])  # draw red or black ball
    #     self.Zn.pop()  # get rid of (n-M-1)th draw (since finite M memory)
    #     self.Zn.insert(0, Z)  # insert nth draw info

    def nextDelta(self, delta):
        self.delta.pop()
        if self.Zn[0] == 0:
            self.delta.insert(0, delta[0])
        else:
            self.delta.insert(0, delta[1])

    def nextU(self):
        U = (self.R + numpy.dot(self.delta, self.Zn)) / (self.T + sum(self.delta))
        self.Um.pop()  # get rid of n-2 time ball proportion
        self.Um.insert(0, U)  # insert n time ball proportion

    def get_Z_m(self):
        return numpy.dot(self.delta, self.Zn)



    def print_current_n(self):  # print urn attributes for current time step
        print("Time:", self.n)  # print time
        print("Prob of drawing Red at this time : {:.2%}".format(self.Um[1]))  # print pre-draw proportion (ie prob)
        if self.Zn[0] == 1:  # print last ball draw
            print("Draw : Red")
        else:
            print("Draw : Black")
        print("-----------------------------")


class SuperUrn(Urn):
    def __init__(self, key, R, B, M, G):
        super().__init__(key, R, B, M)
        self.Graph = G
        self.Ni_key = [key] + list(nx.all_neighbors(G, key))
        self.Ni_list = []
        self.super_R = 0
        self.super_B = 0
        self.super_T = 0
        self.Sm = []

    def setInitialVariables(self):
        for i in self.Ni_key:
            self.Ni_list.append(self.Graph.nodes[i]['superUrn'])
        for urn in self.Ni_list:
            self.super_R += urn.R
            self.super_B += urn.B
        self.super_T = self.super_R + self.super_B
        self.Sm = [self.super_R/self.super_T, 0]


    def drawBall(self):
        Z = numpy.random.choice([0, 1], p=[(1 - self.Sm[0]), self.Sm[0]])  # draw red or black ball
        self.Zn.pop()  # get rid of (n-M-1)th draw (since finite M memory)
        self.Zn.insert(0, Z)  # insert nth draw info


    def nextSm(self):
        nominator = 0
        denominator = 0
        for urn in self.Ni_list:
            nominator += urn.Um[0] * (urn.T + sum(urn.delta))
            denominator += urn.T + sum(urn.delta)
        self.Sm.pop()
        self.Sm.insert(0, nominator/denominator)


def createPolyaNetwork(n, m, R, B):
    G = nx.barabasi_albert_graph(n, m)
    for i in range(len(list(G.nodes))):
        G.nodes[i]['superUrn'] = SuperUrn(i, R, B, MARKOV_MEMORY, G)
    for i in range(len(list(G.nodes))):
        G.nodes[i]['superUrn'].setInitialVariables()
    return G


def networkTimeStep(G, delta):
    for i in range(len(list(G.nodes))):
        G.nodes[i]['superUrn'].drawBall()
        G.nodes[i]['superUrn'].nextDelta(delta)
        G.nodes[i]['superUrn'].nextU()
        G.nodes[i]['superUrn'].nextSm()


def printNetwork(G, t):
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
    polya_network = createPolyaNetwork(num_nodes, num_connections, R, B)
    for n in range(max_n):
        networkTimeStep(polya_network, delta)
        printNetwork(polya_network, n)

    printGraph(polya_network)

def printGraph(G):
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



