from graph import Graph
from collections import deque
from itertools import combinations
import random

def get_diameter(graph: Graph) -> int:
	def bfs_longest_path(start_node):
		visited = set()
		queue = deque([(start_node, 0)])
		farthest_node, max_distance = start_node, 0

		while queue:
			node, distance = queue.popleft()
			if node not in visited:
				visited.add(node)
				if distance > max_distance:
					farthest_node, max_distance = node, distance
				for neighbor in graph.get_neighbors(node):
					if neighbor not in visited:
						queue.append((neighbor, distance + 1))
		return farthest_node, max_distance

	first_node = 0
	if graph.get_num_nodes() == 0:
		return 0

	farthest_node, _ = bfs_longest_path(first_node)
	_, diameter = bfs_longest_path(farthest_node)

	return diameter

def get_clustering_coefficient(graph: Graph, sample_size: int = 10000) -> float:
    """
    Return the approximate global clustering coefficient using sampling.
    :param graph: The input graph.
    :param sample_size: The number of nodes or edges to sample for approximation.
    :return: Approximate global clustering coefficient of the graph.
    """
    triangles = 0
    two_paths = 0

    # Precompute adjacency sets for faster lookup
    adjacency = {node: set(graph.get_neighbors(node)) for node in range(graph.get_num_nodes())}

    # Use sampling for large graphs
    nodes = list(adjacency.keys())
    sampled_nodes = random.sample(nodes, min(sample_size, len(nodes)))

    for node in sampled_nodes:
        neighbors = adjacency[node]
        num_neighbors = len(neighbors)

        # Count two-paths centered at this node
        if num_neighbors < 2:
            continue
        two_paths += num_neighbors * (num_neighbors - 1) // 2

        # Count triangles involving this node
        for u, v in combinations(neighbors, 2):
            if v in adjacency[u]:  # Check if u and v are connected
                triangles += 1

    # Avoid division by zero
    if two_paths == 0:
        return 0.0

    # Scale result to approximate global clustering coefficient
    scaling_factor = len(nodes) / len(sampled_nodes)
    return (triangles / two_paths) * scaling_factor


def get_degree_distribution(graph: Graph) -> dict[int, int]:
	degree_count = {}

	for node in range(graph.get_num_nodes()):
		degree = len(graph.get_neighbors(node))
		if degree not in degree_count:
			degree_count[degree] = 0
		degree_count[degree] += 1

	return dict(sorted(degree_count.items()))
