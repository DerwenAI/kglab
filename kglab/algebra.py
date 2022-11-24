"""
Working with `SubgraphMatrix` as vectorized representation.
Additions to functionalities present in `subg.py`.
Integrate `scipy` and `scikit-learn` functionalities.

see license https://github.com/DerwenAI/kglab#license-and-copyright
"""

import typing

import networkx as nx

from .util import Mixin


class AlgebraMixin (Mixin):
    """
Provides methods to work with graph algebra using `SubgraphMatrix` data.

NOTE: provide optional Oxigraph support for fast in-memory computation
    """
    nx_graph: typing.Optional[nx.DiGraph] = None


    def to_undirected (self):
        """
Return the undirected adjancency matrix of the directed graph.

        returns:
`numpy.array`: the array representation in `numpy` standard
        """
        return nx.to_numpy_array(self.nx_graph.to_undirected())


    def to_adjacency (self):
        """
Return adjacency (dense) matrix for the KG.
[Relevant NetworkX interface](https://networkx.org/documentation/stable/reference/convert.html#id2)

        returns:
`numpy.array`: the array representation in `numpy` standard
        """
        self.check_attributes()
        return nx.to_numpy_array(self.nx_graph)


    def to_incidence (self):
        """
Return incidence (dense) matrix for the KG.
[Relevant scipy docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html)

        returns:
`numpy.array`: the array representation in `numpy` standard
        """
        self.check_attributes()
        return nx.incidence_matrix(self.nx_graph).toarray()


    def to_laplacian (self):
        """
Return Laplacian matrix for the KG. Graph is turned into undirected.
[docs](https://networkx.org/documentation/stable/reference/generated/networkx.linalg.laplacianmatrix.laplacian_matrix.html).
Lapliacian is also known as vertices degrees matrix.

        returns:
`numpy.array`: the array representation in `numpy` standard
        """
        self.check_attributes()
        return nx.laplacian_matrix(self.nx_graph.to_undirected()).toarray()


    def to_scipy_sparse (self):
        """
Return graph in CSR format (optimized for matrix-matrix operations).

        returns:
SciPy sparse matrix: Graph adjacency matrix.
        """
        self.check_attributes()
        return nx.to_scipy_sparse_array(self.nx_graph)
