#!/bin/bash -e

for notebook_path in examples/*.ipynb; do
    [ -e "$notebook_path" ] || continue
    notebook=`basename $notebook_path`
    cp $notebook_path docs/$notebook
    jupyter nbconvert docs/$notebook --to markdown
    rm docs/$notebook
done