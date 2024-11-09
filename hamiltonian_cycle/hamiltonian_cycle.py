import networkx as nx
import numpy as np

"""
Given a graph G = (V, E)


Variables: 
    x_i - i-th node in the path # current_path in the code
    
Domain x:
    x_0 = {0} - Start node
    x_1 = {neighbors of x_0}
    x_2 = {neighbors of x_1}
    ...


Constraints:
1. All nodes must be visited once
    allDifferent(x_0, x_1, ..., x_{n-1})
    If node is visited, it can't be visited again. That's granted by the visited array in the code.

2. For all i in {0, 1, ..., n-1}: (x_i, x_{i+1}) in E
    That's granted by iterating over the neighbors of the current node.
"""


def find_hamiltonian_cycles():

    def hamiltonian_cycle(G, node, visited, current_path):
        visited[node] = True
        current_path.append(node) 

        if len(current_path) == len(G): # If all nodes are visited check that we can return to the start node. 
            if 0 in G[node]:
                # I'm appending a 0 just to make the cycle complete.
                current_path.append(0)
                cycles.append(current_path.copy())
                 # Remove the start and last nodes to continue searching for other cycles. 
                 # Basically look if we can find a way to the start node from other then the previous to the last node
                current_path.pop() 
        else:
            # Walk through all the neighbors of node. "try all values in the domain"
            for neighbor in G[node]:
                if not visited[neighbor]: # if visited, move to the next neighbor. 
                    hamiltonian_cycle(G, neighbor, visited, current_path)

        # Backtrack: Remove the current node from the path and mark it as not visited. Path is invalid or already tried
        current_path.pop()
        visited[node] = False # We can visit this node again in another path


    cycles = []

    G = {
        0: [1, 2, 4],
        1: [0, 3, 4],
        2: [0, 3],
        3: [1, 2],
        4: [0, 1]
        }

    print("Graph:")
    for node, neighbors in G.items():
        print(f"{node}: {neighbors}")

    nodes = list(G.keys())

    # log visited nodes. i-th element is True if i-th node is visited
    visited = np.full(len(G), False)

    current_path = []
    hamiltonian_cycle(G, nodes[0], visited, current_path)
    return cycles


if __name__ == '__main__':
    cycles = find_hamiltonian_cycles()

    if len(cycles) == 0:
        print("No Hamiltonian cycle found")
    else:
        print(f"Found {len(cycles)} Hamiltonian cycles")
        for cycle in cycles:
            print(cycle)