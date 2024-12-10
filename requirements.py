# Import each one of your sorting algorithms below as follows:
# Feel free to comment out these lines before your algorithms are implemented.
from graph import Graph # type: ignore
from graph_algorithms import get_diameter # type: ignore
from graph_algorithms import get_clustering_coefficient # type: ignore
from graph_algorithms import get_degree_distribution # type: ignore

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Details about Gradescope submission:

# - The graph class should be stored in separate files from the three graph algorithms.
# - No file should include anything outside of standard Python libraries.
# - Functions should be tested using Python 3.6+ on a Linux environment.
# - The submission should either be the files themselves, or a zip file not containing any directories.


# Explanations for Graph public member functions
#
# init(): initialize the graph a given number of nodes and given edges.
#         edges are represented as tuples (u, v), where each edge is between node with index u and
#         node with index v.
#         the autograder will never add duplicate edges to the graph.
# get_num_nodes(): returns the number of nodes in the graph.
# get_num_edges(): returns the number of edges in the graph.
# get_neighbors(): given a node index, return an iterable type over the collection of its neighbors.
#                  the iterable type can be a list, set, generator, etc.
#                  each neighbor should appear exactly once.

# Explanations for graph algorithm functions
#
# get_diameter(): return the approximate graph diameter using a heuristic function.
# get_clustering_coefficient(): return the graph's global clustering coefficient.
# get_degree_distribution(): returns a dictionary representing the degree distribution of the graph.
#                            the keys are the degree, and the values is the number of nodes with that
#                            degree.


def analyze_barabasi_albert_graphs(sizes, d=5, num_runs=5):
    diameters = []
    clustering_coeffs = []

    for n in sizes:
        avg_diameter = 0
        avg_clustering = 0

        for _ in range(num_runs):
            graph = Graph.generate_barabasi_albert(num_nodes=n, d=d)
            avg_diameter += get_diameter(graph)
            avg_clustering += get_clustering_coefficient(graph)

        diameters.append(avg_diameter / num_runs)
        clustering_coeffs.append(avg_clustering / num_runs)

    return diameters, clustering_coeffs


# Plot diameters and clustering coefficients
def plot_metrics(sizes, diameters, clustering_coeffs):
    log_sizes = np.log(sizes)

    # Plot Diameter
    plt.figure(figsize=(10, 6))
    plt.plot(log_sizes, diameters, 'o-', label="Diameter")
    slope, intercept, r_value, _, _ = linregress(log_sizes, diameters)
    plt.plot(
        log_sizes,
        slope * log_sizes + intercept,
        '--',
        label=f"Linear Fit (Slope={slope:.2f}, R²={r_value**2:.4f})"
    )
    plt.title("Graph Diameter vs log(n)")
    plt.xlabel("log(n)")
    plt.ylabel("Diameter")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot Clustering Coefficient
    plt.figure(figsize=(10, 6))
    plt.plot(log_sizes, clustering_coeffs, 'o-', label="Clustering Coefficient")
    slope, intercept, r_value, _, _ = linregress(log_sizes, clustering_coeffs)
    plt.plot(
        log_sizes,
        slope * log_sizes + intercept,
        '--',
        label=f"Linear Fit (Slope={slope:.2f}, R²={r_value**2:.4f})"
    )
    plt.title("Clustering Coefficient vs log(n)")
    plt.xlabel("log(n)")
    plt.ylabel("Clustering Coefficient")
    plt.legend()
    plt.grid(True)
    plt.show()


# Plot Degree Distribution
def plot_degree_distribution(graph, title="Degree Distribution", log_scale=False):
    degree_dist = get_degree_distribution(graph)
    degrees, counts = zip(*degree_dist.items())

    plt.figure(figsize=(10, 6))
    plt.plot(degrees, counts, 'o-', label="Degree Distribution")
    if log_scale:
        plt.xscale("log")
        plt.yscale("log")
        plt.title(f"{title} (Log-Log Scale)")
    else:
        plt.title(f"{title} (Linear Scale)")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True, which="both", linestyle="--")
    plt.show()


# Main Function
if __name__ == "__main__":
    # sizes = [1000, 5000, 10000, 20000, 50000]
    sizes = [100, 200, 300, 400, 500]
    d = 5
    num_runs = 5

    # Analyze Barabási-Albert Graphs
    diameters, clustering_coeffs = analyze_barabasi_albert_graphs(sizes, d, num_runs)

    # Plot Diameters and Clustering Coefficients
    plot_metrics(sizes, diameters, clustering_coeffs)

    # Degree Distribution for specific sizes
    small_graph = Graph.generate_barabasi_albert(num_nodes=1000, d=d)
    medium_graph = Graph.generate_barabasi_albert(num_nodes=10000, d=d)
    large_graph = Graph.generate_barabasi_albert(num_nodes=100000, d=d)

    plot_degree_distribution(small_graph, title="Degree Distribution (Small Graph)")
    plot_degree_distribution(medium_graph, title="Degree Distribution (Medium Graph)")
    plot_degree_distribution(large_graph, title="Degree Distribution (Large Graph)")
    plot_degree_distribution(large_graph, title="Degree Distribution (Log-Log)", log_scale=True)