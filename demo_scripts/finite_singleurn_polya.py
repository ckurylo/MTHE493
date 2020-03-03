import numpy


class Urn:
    def __init__(self, R, B, delta, M):
        self.R = R  # initial number of Red balls
        self.B = B  # initial number of Black balls
        self.T = R + B  # initial Total number of balls
        self.delta = delta  # ball replacement number
        self.M = M  # memory of the system
        self.Zn = M*[0]   # stoch process indicator for black or red draw at time n, only need M previous draw info
        self.Um = [R/(R+B), 0]  # red ball proportion in the urn, only ever need the value before and after each draw
        self.n = 0  # time

    def timeStep(self):  # execute next draw in process
        self.n += 1  # increment time
        self.nextZ()
        self.nextU()

    def nextZ(self):
        Z = numpy.random.choice([0, 1], p=[(1-self.Um[0]), self.Um[0]])  # draw red or black ball
        self.Zn.pop()  # get rid of (n-M-1)th draw (since finite M memory)
        self.Zn.insert(0, Z)  # insert nth draw info


    def nextU(self):
        if self.n < self.M:  # for draws for time less than M, have n memory for computing ball proportion
            U = (self.R + self.delta * sum(self.Zn)) / (self.T + self.n * self.delta)
        else:  # past n = M, have M memory for computing ball proportion
            U = (self.R + self.delta * sum(self.Zn)) / (self.T + self.M * self.delta)
        self.Um.pop()  # get rid of n-2 time ball proportion
        self.Um.insert(0, U)  # insert n time ball proportion

    def print_current_n(self):  # print urn attributes for current time step
        print("Time:", self.n)  # print time
        print("Prob of drawing Red at this time : {:.2%}".format(self.Um[1]))  # print pre-draw proportion (ie prob)
        if self.Zn[0] == 1:  # print last ball draw
            print("Draw : Red")
        else:
            print("Draw : Black")
        print("-----------------------------")


def polya_simulation(R, B, delta, M, max_n):

    polyaUrn = Urn(R, B, delta, M)
    print("-----------------")
    for n in range(max_n):  # run simulation for max_n total draws
        polyaUrn.timeStep()
        polyaUrn.print_current_n()


#######################################
# PARAMETER INPUT
R = 10
B = 5
delta = 2
M = 3
max_n = 15
polya_simulation(R, B, delta, M, max_n)

