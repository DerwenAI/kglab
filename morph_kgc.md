# Currently the `morph-kgc` package is pinned to use `rdflib <7.3.0` due to unit
tests breaking with later versions: https://github.com/morph-kgc/morph-kgc/issues/345

# The following code has been temporarily removed from the `kglab/serde.py` module:

import morph_kgc

    def materialize (
        self,
        config: str,
        ) -> "KnowledgeGraph": # type: ignore
        """
Binding to the [Morph-KGC](https://github.com/oeg-upm/morph-kgc) `materialize()` method.

    config:
morph-kgc configuration, it can be the path to the config file, or a string with the config; see <https://morph-kgc.readthedocs.io/en/latest/documentation/#library>

    returns:
this `KnowledgeGraph` object – used for method chaining
        """
        if len(self._g) == 0: # type: ignore
            # generate the triples and load them to an RDFlib graph
            self._g = morph_kgc.materialize(config)
        else:
            # merge
            # for caveats about merging this way:
            # <https://rdflib.readthedocs.io/en/stable/merging.html>
            self._g.parse(morph_kgc.materialize(config)) # type: ignore

        return self


