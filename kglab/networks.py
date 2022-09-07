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
        """
        self.check_attributes()
        return squareform(pdist(adj_mtx, metric='euclidean'))

    def get_shortest_path(self, adj_matx, src, dst):
        """
Return shortest path from sources to destinations according to an djacency matrix.

        adj_mtx:
numpy.array: adjacency matrix for the graph.
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
        # number of nodes, number of edges
        # density
        # triangles
        # reciprocity
        raise NotImplementedError()