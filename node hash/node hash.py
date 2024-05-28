# -*- coding: utf-8 -*-
def remap_nodes_and_save(input_file, output_file):
    import os

    # Read the file and extract edges
    with open(input_file, 'r') as file:
        edges = [line.strip().split() for line in file.readlines()]

    # Map original nodes to new node IDs
    node_map = {}
    new_node_id = 0

    def get_node_id(node):
        nonlocal new_node_id
        if node not in node_map:
            node_map[node] = new_node_id
            new_node_id += 1
        return node_map[node]

    # Create new edge connections
    new_edges = [(get_node_id(edge[0]), get_node_id(edge[1])) for edge in edges]

    # Save new edges to the output file
    with open(output_file, 'w') as file:
        for edge in new_edges:
            file.write(f"{edge[0]} {edge[1]}\n")


# Usage example
remap_nodes_and_save('input_file.txt', 'output_file.txt')
