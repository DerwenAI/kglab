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
        self.check_attributes()
        return skn.path.get_distances(adj_mtx)