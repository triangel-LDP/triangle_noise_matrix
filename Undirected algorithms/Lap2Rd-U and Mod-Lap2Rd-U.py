# -*- coding: utf-8 -*-
# The input for this program is all undirected edges
import numpy as np
import time

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
            adjacency_list[node2].append(node1)

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
        if i != j:
            matrix[j, i] += 1  # Also update the symmetric element

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
        A = create_and_update_matrix(n, 1 / (0.9 * eps), edges)

        total = 0

        for i in range(n):
            d_i = len(adjacency_list[i])
            for j in adjacency_list[i]:
                total += A[j, :] @ A[:, i]
            laplace_noise = np.random.laplace(0, d_i / (0.1 * eps))
            total += laplace_noise

        guss_tri = total / 6

        print("Mod-Lap2Rd-U:", guss_tri)

        list1.append(abs(guss_tri - true_tri))
        list2.append((guss_tri - true_tri) ** 2)

        ################################################################################################################

        total_sum = 0

        for node in range(0, n):
            neighbors = adjacency_list[node]
            # Record the neighbors of node

            for i in range(len(neighbors) - 1):
                for j in range(i + 1, len(neighbors)):  # Note that this is from i+1 to n, undirected graph pairs (i, j) are enumerated once
                    total_sum += A[neighbors[i], neighbors[j]]
            # Add the edges between the neighbors of node to the total sum. For example, if node 1 has neighbors 2, 3, 4, 5, add the values corresponding to these nodes in pairs in M
            total_sum += np.random.laplace(0, len(adjacency_list[node]) / (0.1 * eps))

        guss_tri2 = total_sum / 3
        print("Lap2Rd-U:", guss_tri2)
        list3.append(abs(guss_tri2 - true_tri))
        list4.append((guss_tri2 - true_tri) ** 2)

    se = sum(list2) / len(list2)
    re = sum(list1) / len(list1) / true_tri

    MSE1.append(se)
    MRE1.append(re)

    print("Mod-Lap2Rd-U:", 'MSE:', se, '     MRE:', re)

    se = sum(list4) / len(list4)
    re = sum(list3) / len(list3) / true_tri

    print("Lap2Rd-U:", 'MSE:', se, '     MRE:', re)

    MSE2.append(se)
    MRE2.append(re)
    print('\n')


print(epsilon_list)
print("Lap2Rd-U:MSE:", MSE2)
print("Lap2Rd-U:MRE:", MRE2)
print("Mod-Lap2Rd-U:MSE:", MSE1)
print("Mod-Lap2Rd-U:MRE:", MRE1)

end_time = time.time()  # End timing
print("Total running time:", end_time - start_time, "seconds")
