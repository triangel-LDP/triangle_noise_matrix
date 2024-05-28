# -*- coding: utf-8 -*-
import numpy as np
import time
import math

def read_graph_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # First read all lines to determine the maximum node number
        lines = file.readlines()
        max_node = 0
        for line in lines:
            node1, node2 = map(int, line.split())
            if node1 > max_node:
                max_node = node1
            if node2 > max_node:
                max_node = node2

    # Create a sufficiently large adjacency list array
    adjacency_list = [[] for _ in range(max_node + 1)]
    in_list = [[] for _ in range(max_node + 1)]

    # Traverse all lines again to construct the adjacency list
    for line in lines:
        node1, node2 = map(int, line.split())
        adjacency_list[node1].append(node2)
        in_list[node2].append(node1)

    return adjacency_list, in_list, max_node + 1


def create_and_update_matrix(n, b, edges):
    # Create an empty n*n matrix
    matrix = np.zeros((n, n), dtype=np.float64)

    for i in range(n):
        for j in range(n):
            matrix[i, j] = np.random.laplace(0, b)

    for i in range(n):
        matrix[i, i] = 0

    # Update the matrix with the edge information in memory
    for i, j in edges:
        matrix[i, j] += 1

    return matrix


def count_triangles(adjacency_list, in_list):
    triangles = 0
    # Sort each node by the length of its adjacency list
    nodes = sorted(range(len(adjacency_list)), key=lambda x: len(adjacency_list[x]))

    for node in nodes:
        outs = adjacency_list[node]
        ins = in_list[node]
        # Only check if each pair of neighbors are also connected to each other
        for i in range(len(outs)):
            for j in range(len(ins)):
                if outs[i] != ins[j]:
                    if ins[j] in adjacency_list[outs[i]]:
                        triangles += 1

    return triangles // 3  # Since each triangle is counted three times, divide by 3


def fast_1round(A, n):
    M = math.ceil(4 * math.log(n) * math.log(n))
    # M is the number of Monte Carlo samples

    T = []
    # To store the values obtained after each sampling

    for i in range(M):
        x = np.random.randn(n)
        y = A @ x
        s = (y.T) @ A @ y / 6
        # This is the algorithm step, x is a generated n-dimensional standard normal random vector. First, multiply it by matrix A to get vector y, then calculate the transpose of y multiplied by A and y, thus using n^2 time complexity to calculate the trace of the matrix. Since we want to count the number of triangles, divide by 6 at the end
        T.append(s)

    ans = sum(T) / len(T)
    # Take the average of the sampled data
    return ans


# Usage
file_path = 'your_output_file.txt'
adjacency_list, in_list, n = read_graph_from_file(file_path)

print(n)

epsilon_list = [0.1, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]

MSE1 = []
MRE1 = []
MSE2 = []
MRE2 = []

true_tri = count_triangles(adjacency_list, in_list)
print("True number of triangles:", true_tri)


def load_edges_to_memory(filepath):
    edges = []
    with open(filepath, 'r') as file:
        for line in file:
            i, j = map(int, line.strip().split())
            edges.append((i, j))
    return edges


# Load edge information into memory
edges = load_edges_to_memory(file_path)

start_time = time.time()  # Start timing

for eps in epsilon_list:
    print("epsilon:", eps, ":")

    list1 = []
    list2 = []
    list3 = []
    list4 = []

    for k in range(20):
        A = create_and_update_matrix(n, 1 / eps, edges)

        guss_tri = np.trace(np.linalg.matrix_power(A, 3)) / 3

        print("Lap1Rd-D:", guss_tri)

        list1.append(abs(guss_tri - true_tri))
        list2.append((guss_tri - true_tri) ** 2)

        ################################################################################################################

    se = sum(list2) / len(list2)
    re = sum(list1) / len(list1) / true_tri

    MSE1.append(se)
    MRE1.append(re)

    print("Lap1Rd-D:", 'MSE:', se, '     MRE:', re)
    print('\n')


print(epsilon_list)
print("Lap1Rd-D:MSE:", MSE1)
print("Lap1Rd-D:MRE:", MRE1)

end_time = time.time()  # End timing
print("Total running time:", end_time - start_time, "seconds")
