# -*- coding: utf-8 -*-
import numpy as np
import time
import math

def read_graph_from_file(file_path):
    adjacency_list = {}
    max_node = 0
    with open(file_path, 'r', encoding='utf-8') as file:  # Specify encoding as UTF-8
        for line in file:
            node1, node2 = map(int, line.split())
            if node1 > max_node:
                max_node = node1
            if node2 > max_node:
                max_node = node2
            if node1 not in adjacency_list:
                adjacency_list[node1] = []
            if node2 not in adjacency_list:
                adjacency_list[node2] = []
            adjacency_list[node1].append(node2)

    return adjacency_list, max_node + 1


def create_and_update_matrix(n, b, edges):
    # Create an empty n*n matrix
    matrix = np.zeros((n, n), dtype=np.float64)

    # Fill the lower triangle of the symmetric matrix and mirror to the upper triangle
    for i in range(n):
        for j in range(i + 1):
            value = np.random.laplace(0, b)  # Generate random numbers from Laplace distribution
            matrix[i, j] = value
            if i != j:
                matrix[j, i] = value  # Ensure matrix symmetry

    for i in range(n):
        matrix[i, i] = 0

    # Update the matrix with the edge information in memory
    for i, j in edges:
        matrix[i, j] += 1

    return matrix


def count_triangles(adjacency_list):
    triangles = 0

    # Sort nodes by degree to minimize the intersection operation cost
    nodes = sorted(adjacency_list, key=lambda x: len(adjacency_list[x]))

    for node in nodes:
        neighbors = list(adjacency_list[node])
        # Only check for each pair of neighbors if they are also connected
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                if neighbors[j] in adjacency_list[neighbors[i]]:
                    triangles += 1

    return triangles / 3  # Since each triangle is counted three times, divide by 3


# Usage
file_path = 'your_output_file.txt'
adjacency_list, n = read_graph_from_file(file_path)

print(n)

epsilon_list = [0.1, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]

MSE1 = []
MRE1 = []
MSE2 = []
MRE2 = []

true_tri = count_triangles(adjacency_list)
print("True number of triangles:", true_tri)


def load_edges_to_memory(filepath):
    edges = []
    with open(filepath, 'r') as file:
        for line in file:
            i, j = map(int, line.strip().split())
            edges.append((i, j))
    return edges


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


# Load edge information into memory
edges = load_edges_to_memory(file_path)

start_time = time.time()  # Start timing

for eps in epsilon_list:
    print("epsilon:", eps, ":")

    list1 = []
    list2 = []
    list3 = []
    list4 = []

    for k in range(10):
        A = create_and_update_matrix(n, 1 / (0.9 * eps), edges)

        guss_tri = fast_1round(create_and_update_matrix(n, 1 / eps, edges), n)

        print("Acc-Lap1Rd-U:", guss_tri)

        list1.append(abs(guss_tri - true_tri))
        list2.append((guss_tri - true_tri) ** 2)


    se = sum(list2) / len(list2)
    re = sum(list1) / len(list1) / true_tri

    MSE1.append(se)
    MRE1.append(re)

    print("Acc-Lap1Rd-U:", 'MSE:', se, '     MRE:', re)


print(epsilon_list)
print("Acc-Lap1Rd-U:MSE:", MSE1)
print("Acc-Lap1Rd-U:MRE:", MRE1)

end_time = time.time()  # End timing
print("Total running time:", end_time - start_time, "seconds")
