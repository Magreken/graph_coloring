import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.generators.random_graphs import erdos_renyi_graph
import numpy as np
import scipy
import argparse


class Node():
    def __init__(self, colors):
        self.color = 0
        self.neighbours = []
        self.available_colors = np.copy(colors)
        self.fixed = False

    def set_color(self, c):
        self.color = c

    def get_color(self):
        return self.color

    def add_neighbour(self, n):
        self.neighbours.append(n)

    def remove_color(self, c):
        self.available_colors = [e for e in self.available_colors if e != c]

    def generate_new_color(self):
        self.color = random.Random().choice(self.available_colors)

    def set_fixed(self):
        assert self.color != 0
        self.fixed = True

    def remove_own_color(self):
        self.color = 0

    def is_fixed(self):
        return self.fixed


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="increase output verbosity")
parser.add_argument("-r", "--random", help="increase output verbosity")
args = parser.parse_args()



node_amount = 20

max_edge = [0 for _ in range(node_amount)]

gg = erdos_renyi_graph(node_amount, 0.25)

plt.figure(dpi=300)
nx.draw_networkx(gg, node_size=100, font_size=9)
plt.show()

for e in gg.edges:
    max_edge[e[0]] += 1
    max_edge[e[1]] += 1

delta = np.max(max_edge)+1

colors = [e+1 for e in range(delta)]

nodes = [Node(colors) for _ in range(node_amount)]

for e in gg.edges:
    nodes[e[0]].add_neighbour(e[1])
    nodes[e[1]].add_neighbour(e[0])

iteration = 0

while(True):
    missing = [e for e in nodes if not e.is_fixed()]
    terminate = True
    for node in nodes:
        if node.get_color() == 0:
            terminate = False
            node.generate_new_color()
        if node.get_color() == 0:
            print("WTF")
    if terminate:
        break
    for node in nodes:
        new_color = True
        for neighbour in node.neighbours:
            if node.color == nodes[neighbour].get_color():
                if nodes[neighbour].is_fixed():
                    node.remove_color(node.color)
                node.set_color(0)
                new_color = False
                break
        if new_color and node.get_color() != 0:
            node.set_fixed()
    iteration += 1
    print(f"Iteration: {iteration}\n", end='\r')

print(f"Finish in {iteration} iterations")

for edge in gg.edges:
    assert nodes[edge[0]].get_color() != nodes[edge[1]].get_color()
