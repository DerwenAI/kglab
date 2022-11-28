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

    def to_zarr (self, func: str) -> "zzarr.core.Array":  # type: ignore
        """
Return value of a function in `kglab.algebra` in [Zarr format](https://pypi.org/project/zarr/).

       Args:
func str: a name of one functions in `kglab.algebra`: `to_undirect`, `to_adjacency`, `to_incidence`, `to_laplacian`

       returns:
zzarr.core.Array: values of requested `func`
        """
        self.check_attributes()  # type: ignore
        try:
            import zarr  # type: ignore
        except ImportError:
            raise ImportError("To use Zarr you need to install kglab with the required extra package: pip install kglab[with-zarr]")

        data = getattr(self, func)()
        array = zarr.create(data.shape, chunks=(10, 10))
        array[:] = data

        return array
