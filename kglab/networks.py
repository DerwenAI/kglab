"""
Working with `SubgraphMatrix` as vectorized representation.
Additions to functionalities present in `subg.py`.
Integrate `scikit-network` functionalities.

see license https://github.com/DerwenAI/kglab#license-and-copyright
"""

import networkx as nx
from networkx.exception import NetworkXError
from scipy.spatial.distance import pdist, squareform

from .util import Mixin


class NetAnalysisMixin (Mixin):
    """
Provides methods for network analysis tools to work with `KnowledgeGraph`.
    """
    def get_distances (self, adj_mtx):
        """
Compute distances according to an adjacency matrix.

        adj_mtx:
numpy.array: square matrix of distances.
        """
        self.check_attributes()
        return squareform(pdist(adj_mtx, metric="euclidean"))


    def get_shortest_path (self, src, dst):
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


    def describe (self):
        """
Return a summary for subgraph statistics.
NOTE: we may cache these methods calls if we create something like a `GraphFrame` object.
  see kglab#273, same for adjacency and other matrices.

        return:
dict: a dictionary with stats
        """
        def msg_if_raise (f, g, r):
            """Handle error messages by adding a message key in the results"""
            try:
                return f(g)
            except NetworkXError as e:
                r[f"{str(f.__name__)}_msg"] =  str(e)
                return None

        results = {
            "n_nodes": self._get_n_nodes(),
            "n_edges": self._get_n_edges(),
        }

        return { **results, **{
            "center": msg_if_raise(nx.center, self.nx_graph, results),
            "diameter": msg_if_raise(nx.diameter, self.nx_graph, results),
            "eccentricity": msg_if_raise(nx.eccentricity, self.nx_graph, results)
        }}


    def describe_more (self):
        """
Return a summary with more graph statistics.
        """
        # density
        # triangles
        # reciprocity
        raise NotImplementedError()
