class Node:
    def __init__(self, val):
        self.val = val
        self.neighbour = []

    def print_neighbour(self):
        for element in self.neighbour:
            print(element.val)

    def def_neighbour(self, n_list):
        for element in n_list:
            self.neighbour.append(element)


node1 = Node(1)
node2 = Node(2)
node3 = Node(3)

node1.def_neighbour([node2, node3])

node1.print_neighbour()
