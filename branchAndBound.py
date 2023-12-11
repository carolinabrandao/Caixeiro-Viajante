import numpy as np
import networkx as nx
import math
import tracemalloc
import time 
import tsplib95



class Node:
    def __init__(self, bound, boundEdges, cost, solution):
        self.bound = bound
        self.boundEdges = boundEdges
        self.cost = cost
        self.solution = solution
    
    def __lt__(self, other):
        if len(self.solution) == len(other.solution):
            return self.bound < other.bound
        elif len(self.solution) > len(other.solution):
            return True
        else:
            return False
    


def findTwoMinimalEdges(list):
    min1 = np.inf
    min2 = np.inf
    for j in list:
        if list[j]['weight'] < min1:
            min2 = min1
            min1 = list[j]['weight']
        elif list[j]['weight'] < min2:
            min2 = list[j]['weight']
    return min1, min2

def findInitialBound(A):
    bound = 0
    initialBoundEdges = np.zeros((A.number_of_nodes(), 2), dtype=list)
    for i in range(A.number_of_nodes()):
        min1, min2 = findTwoMinimalEdges(A[i])
        initialBoundEdges[i][0] = min1
        initialBoundEdges[i][1] = min2
        bound += min1 + min2
    return bound / 2, initialBoundEdges

def findBound(A, solution, boundEdges, bound):
    changedEdges = np.zeros(A.number_of_nodes(), dtype=int)
    newEdges = np.array(boundEdges)
    edgeWeight = A[solution[-2]][solution[-1]]['weight']
    sum = bound * 2
    if newEdges[solution[-2]][0] != edgeWeight:
        if changedEdges[solution[-2]] == 0:
            sum -= newEdges[solution[-2]][1]
            sum += edgeWeight
        else:
            sum -= newEdges[solution[-2]][0]
            sum += edgeWeight
        changedEdges[solution[-2]] += 1
    if newEdges[solution[-1]][0] != edgeWeight:
        if changedEdges[solution[-1]] == 0:
            sum -= newEdges[solution[-1]][1]
            sum += edgeWeight
        else:
            sum -= newEdges[solution[-1]][0]
            sum += edgeWeight
        changedEdges[solution[-1]] += 1
    return sum / 2, newEdges 
from heapq import heappush, heappop

def branchAndBoundTSP(A):

    initialBound, initialBoundEdges = findInitialBound(A)
    root = Node(initialBound, initialBoundEdges, 0, [0])
    heap = []
    heappush(heap, root)
    best = np.inf
    solution = []
    nodeCount = 0
    while heap:
        node = heappop(heap)
        nodeCount += 1
        level = len(node.solution)
        if level > A.number_of_nodes():
            if best > node.cost:
                best = node.cost
                solution = node.solution
        else:
            if node.bound < best:
                if level < A.number_of_nodes() - 2:
                    for k in range(1, A.number_of_nodes()):
                        if k == node.solution[-1] or k == 0:
                            continue
                        edgeWeight = A[node.solution[-1]][k]['weight']
                        newBound, newEdges = findBound(A, node.solution + [k], node.boundEdges, node.bound) 
                        if k not in node.solution and newBound < best:
                            newNode = Node(newBound, newEdges, node.cost + edgeWeight, node.solution + [k])
                            if k == 2:
                                if 1 not in node.solution:  
                                    continue 
                            heappush(heap, newNode)
                else:
                    for k in range(1, A.number_of_nodes()):
                        if k == node.solution[-1] or k == 0:
                            continue
                        lastNode = 0
                        for i in range(1, A.number_of_nodes()):
                            if i not in node.solution + [k] and k != i:
                                lastNode = i
                                break
                        edgeWeight = A[node.solution[-1]][k]['weight']
                        nextEdgeWeight = A[k][lastNode]['weight']
                        lastEdgeWeight = A[lastNode][0]['weight']
                        cost = node.cost + edgeWeight + nextEdgeWeight + lastEdgeWeight
                        if k not in node.solution and cost < best:
                            newNode = Node(cost, [], cost, node.solution + [k, lastNode, 0])
                            heappush(heap, newNode)
    #add 1 to each element in solution
    solution = [x + 1 for x in solution]
    return best, solution

def euclidean_distance(coord1, coord2):
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(coord1, coord2)))


def create_graph(problem):
    G = nx.Graph()
    for node1 in problem.get_nodes():
        for node2 in problem.get_nodes():
            if node1 != node2:
                # Ajustando os índices dos nós para começar de 0
                coord1 = problem.node_coords[node1]
                coord2 = problem.node_coords[node2]
                distance = euclidean_distance(coord1, coord2)
                G.add_edge(node1 - 1, node2 - 1, weight=distance)
    return G

def branch_and_bound(problem):

        tempo_inicial = time.time()
        tracemalloc.start()

        graph = create_graph(problem)
        weight, path = branchAndBoundTSP(graph)
        tempo_final = time.time()
        tempo = tempo_final - tempo_inicial
        bytes, _ = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print("Problema:", problem.name)
        print("Tempo de execução:", tempo)
        print("Uso de memória:", bytes)
        

nos10 = tsplib95.load("testesBNB/test10.tsp")
nos15 = tsplib95.load("testesBNB/test15.tsp")
nos20 = tsplib95.load("testesBNB/test20.tsp")
nos30 = tsplib95.load("testesBNB/test30.tsp")

branch_and_bound(nos10)
branch_and_bound(nos15)
branch_and_bound(nos20)
branch_and_bound(nos30)

