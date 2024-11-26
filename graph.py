from collections.abc import Iterable
from collections import defaultdict
import random

class Graph:
	def __init__(self, num_nodes: int, edges: Iterable[tuple[int, int]] = ()):
		self.num_nodes = num_nodes
		self.edges = list(edges)
		self.adjacency_list = defaultdict(set)

		for u, v in self.edges:
			self.adjacency_list[u].add(v)
			self.adjacency_list[v].add(u)

	def get_num_nodes(self) -> int:
		return self.num_nodes

	def get_num_edges(self) -> int:
		return len(self.edges)

	def get_neighbors(self, node: int) -> Iterable[int]:
		return self.adjacency_list[node]

	@classmethod
	def generate_barabasi_albert(cls, num_nodes: int, d: int) -> 'Graph':

		edges = []
		adjacency_list = defaultdict(set)

		for u in range(d + 1):
			for v in range(u + 1, d + 1):
				edges.append((u, v))
				adjacency_list[u].add(v)
				adjacency_list[v].add(u)

		for new_node in range(d + 1, num_nodes):
			nodes_with_repetition = [
				node for node, neighbors in adjacency_list.items() for _ in range(len(neighbors))
			]
			target_nodes = random.sample(nodes_with_repetition, d)

			for target in target_nodes:
				edges.append((new_node, target))
				adjacency_list[new_node].add(target)
				adjacency_list[target].add(new_node)

		return cls(num_nodes, edges)
