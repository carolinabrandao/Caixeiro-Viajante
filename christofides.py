import math
import networkx as nx
import tracemalloc
import time

class Christofides:
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
    
    def findShortcutPath(self, MSTMultiGraph):
        path = list(nx.eulerian_circuit(MSTMultiGraph, source=list(MSTMultiGraph.nodes)[0]))
        path = [x[0] for x in path]
        shortcutPath = list(dict.fromkeys(path))
        return shortcutPath + [shortcutPath[0]]

    def findPathWeight(self):
        weight = 0
        for i in range(len(self.path) - 1):
            weight += self.graph[self.path[i]][self.path[i + 1]]['weight']
        return weight
    

    # Algoritmo de Christofides
    def christofidesTSP(self):
        tracemalloc.start()
        tempo_inicial = time.time()

        
        MST = nx.minimum_spanning_tree(self.graph)
        degrees = dict(nx.degree(MST))
        oddNodes = [node for node, degree in degrees.items() if degree % 2 == 1]
        oddNodesSubgraph = self.graph.subgraph(oddNodes)
        matching = list(nx.min_weight_matching(oddNodesSubgraph, maxcardinality=True))

        MSTMultiGraph = nx.MultiGraph(MST)
        for node1, node2 in matching:
            MSTMultiGraph.add_edge(node1, node2, weight=self.graph[node1][node2]['weight'])

        self.path = self.findShortcutPath(MSTMultiGraph)
        self.weight = self.findPathWeight()

        tempo_final = time.time()
        self.time = tempo_final - tempo_inicial
        self.bytes, _ = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return self.weight, self.time, self.bytes
