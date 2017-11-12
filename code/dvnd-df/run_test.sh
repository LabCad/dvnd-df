#!/usr/bin/env bash

export DVND_HOME=~/git/dvnd-df/code/dvnd-df/src
export PYDF_HOME=~/git/dvnd-df/code/

cd test
python -m unittest discover
