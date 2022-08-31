"""
Working with `KnowledgeGraph` as matrix.
Integrate `scipy` and `scikit-learn` functionalities.

see license https://github.com/DerwenAI/kglab#license-and-copyright
"""

class AlgebraMixin:
    """
    Provides methods to work with graph algebra using `KnowledgeGraph` data
    """
    def to_observation_matrix(self):
        pass

    def to_adj_matrix(self):
        pass

    def to_condensed_pdist(self):
        pass
