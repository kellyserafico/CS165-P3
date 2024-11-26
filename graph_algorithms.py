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

def get_clustering_coefficient_small(graph: Graph) -> float:
	triangles = 0
	two_paths = 0

	adjacency = {node: set(graph.get_neighbors(node)) for node in range(graph.get_num_nodes())}

	for node in range(graph.get_num_nodes()):
		neighbors = adjacency[node]
		num_neighbors = len(neighbors)

		if num_neighbors < 2:
			continue

		two_paths += num_neighbors * (num_neighbors - 1) // 2

		for neighbor in neighbors:
			if neighbor > node:
				shared_neighbors = neighbors.intersection(adjacency[neighbor])
				triangles += len(shared_neighbors)

	if two_paths == 0:
		return 0.0

	return triangles / two_paths


def approximate_clustering_coefficient(graph: Graph, sample_size: int = 1000) -> float:
	if graph.get_num_nodes() == 0:
		return 0.0

	nodes = list(range(graph.get_num_nodes()))
	sampled_nodes = random.sample(nodes, min(sample_size, len(nodes)))

	triangles = 0
	two_paths = 0

	adjacency = {node: set(graph.get_neighbors(node)) for node in nodes}

	for node in sampled_nodes:
		neighbors = adjacency[node]
		num_neighbors = len(neighbors)

		if num_neighbors < 2:
			continue

		two_paths += num_neighbors * (num_neighbors - 1) // 2

		for neighbor in neighbors:
			shared_neighbors = neighbors.intersection(adjacency[neighbor])
			triangles += len(shared_neighbors)

	if two_paths == 0:
		return 0.0

	return triangles / two_paths


def get_clustering_coefficient(graph: Graph) -> float:
	threshold = 10000
	if graph.get_num_nodes() > threshold:
		return approximate_clustering_coefficient(graph, sample_size=1000)
	else:
		return get_clustering_coefficient_small(graph)




def get_degree_distribution(graph: Graph) -> dict[int, int]:
	degree_count = {}

	for node in range(graph.get_num_nodes()):
		degree = len(graph.get_neighbors(node))
		if degree not in degree_count:
			degree_count[degree] = 0
		degree_count[degree] += 1

	return dict(sorted(degree_count.items()))
