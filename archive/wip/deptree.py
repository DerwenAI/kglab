#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
See <https://stackoverflow.com/a/55007852/1698443>
"""

import pipdeptree  # type: ignore # pylint: disable=E0401
import json
#import sys

pkgs = pipdeptree.get_installed_distributions()

tree = pipdeptree.PackageDAG.from_pkgs(pkgs)
print(pipdeptree.render_json_tree(tree, indent=2))

json_tree = json.loads(pipdeptree.render_json_tree(tree, indent=0))
print([package["package_name"] for package in json_tree])
