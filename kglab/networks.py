"""
Working with `SubgraphMatrix` as vectorized representation.
Additions to functionalities present in `subg.py`.
Integrate `scikit-network` functionalities.

see license https://github.com/DerwenAI/kglab#license-and-copyright
"""

import sknetwork as skn

class NetAnalysisMixin:
    """
Provides methods for network analysis tools to work with `KnowledgeGraph`.
    """
    def get_distances(self, adj_mtx):
        """
Compute distances according to an adjacency matrix.
        """
        self.check_attributes()
        return skn.path.get_distances(adj_mtx)

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
        return skn.path.get_shortest_path(adj_matx, src, dst)


# number of nodes, number of edges
# density
# triangles
# reciprocity