#!/bin/bash -e

## debugging the uploaded README:
# pandoc README.md --from markdown --to rst -s -o README.rst

rm -rf dist build kglab.egg-info
python setup.py sdist bdist_wheel -v
twine upload --verbose dist/*
