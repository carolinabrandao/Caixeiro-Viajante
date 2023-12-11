import tsplib95 
import math
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import tracemalloc
import time

class TwiceAroundtheTree:
    def __init__(self, instance):
        self.instance = instance
        self.graph = self.create_graph()
        self.time = 0
        self.bytes = 0
        self.weight = 0
        self.path = []

    def euclidean_distance(self, coord1, coord2):
        return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(coord1, coord2)))
    
    def create_graph(self):
        G = nx.Graph()
        for node1 in self.instance.get_nodes():
            for node2 in self.instance.get_nodes():
                if node1 != node2:
                    coord1 = self.instance.node_coords[node1]
                    coord2 = self.instance.node_coords[node2]
                    distance = self.euclidean_distance(coord1, coord2)
                    G.add_edge(node1, node2, weight=distance)
        return G
    
    def findPathWeight(self, A, path):
        weight = 0
        for i in range(len(path) - 1):
            weight += A[path[i]][path[i + 1]]['weight']
        return weight
    
    def twiceAroundTheTreeTSP(self):
        tracemalloc.start()
        tempo_inicial = time.time()

        MST = nx.minimum_spanning_tree(self.graph)
        first_node = list(self.graph.nodes)[0]
        path = list(nx.dfs_preorder_nodes(MST, first_node))
        path.append(path[0])
        self.weight = self.findPathWeight(self.graph, path)
        self.path = path

        tempo_final = time.time()
        self.time = tempo_final - tempo_inicial
        self.bytes, _ = tracemalloc.get_traced_memory()
        
        return self.weight, self.time, self.bytes
    

    

