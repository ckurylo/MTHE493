import numpy


class Urn:
    def __init__(self, R, B, delta):
        self.R = R  # initial number of Red balls
        self.B = B  # initial number of Black balls
        self.T = R + B  # initial Total number of balls
        self.delta = delta  # ball replacement number
        self.Zn = []  # stoch process indicator for black or red draw at time n
        self.Um = [R/(R+B), 0]  # red ball proportion in the urn, only ever need the value before and after each draw

    def timeStep(self):  # execute next draw in process
        self.nextZ()
        self.nextU()

    def nextZ(self):
        Z = numpy.random.choice([0, 1], p=[(1-self.Um[0]), self.Um[0]])  # draw red or black ball
        self.Zn.append(Z)  # add ball draw to indicator process Zn

    def nextU(self):
        U = (self.R + self.delta * sum(self.Zn)) / (self.T + len(self.Zn) * self.delta)  # new proportion of balls
        self.Um.pop()  # get rid of proportion for time n-2
        self.Um.insert(0, U)  # insert proportion for time n

    def print_current_n(self):  # print urn attributes for current time step
        print("Time:", len(self.Zn))  # print time
        print("Prob of drawing Red at this time : {:.2%}".format(self.Um[1]))  # print pre-draw proportion (ie prob)
        if self.Zn[-1] == 1:  # print last ball draw
            print("Draw : Red")
        else:
            print("Draw : Black")
        print("-----------------------------")


def polya_simulation(R, B, delta, max_n):

    polyaUrn = Urn(R, B, delta)
    print("-----------------")
    for n in range(max_n):  # run simulations for max_n total draws
        polyaUrn.timeStep()
        polyaUrn.print_current_n()


#######################################
# PARAMETER INPUT
R = 5
B = 5
delta = 2
max_n = 100
polya_simulation(R, B, delta, max_n)
