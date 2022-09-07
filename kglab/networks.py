"""
Working with `SubgraphMatrix` as vectorized representation.
Additions to functionalities present in `subg.py`.
Integrate `scikit-network` functionalities.

see license https://github.com/DerwenAI/kglab#license-and-copyright
"""

import networkx as nx
from scipy.spatial.distance import pdist, squareform

class NetAnalysisMixin:
    """
Provides methods for network analysis tools to work with `KnowledgeGraph`.
    """
    def get_distances(self, adj_mtx):
        """
Compute distances according to an adjacency matrix.

        adj_mtx:
numpy.array: square matrix of distances.
        """
        self.check_attributes()
        return squareform(pdist(adj_mtx, metric='euclidean'))

    def get_shortest_path(self, src, dst):
        """
Return shortest path from sources to destinations.

        src:
int or iterable: indices of source nodes
        dst:
int or iterable: indices of destination nodes

        returns:
list of int: a path of indices
        """
        self.check_attributes()
        return nx.shortest_path(self.nx_graph, source=src, target=dst)

    def describe(self):
        """
Return a summary for subgraph statistics.

        return:
dict: a dictionary with stats
        """

        return {
            "n_nodes": self._get_n_nodes(),
            "n_edges": self._get_n_edges()
        # <https://networkx.org/documentation/stable/reference/algorithms/distance_measures.html>
        # center
        # diameter
        # eccentricity
        }

    def describe_more(self):
        # density
        # triangles
        # reciprocity
        raise NotImplementedError()