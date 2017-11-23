#!/usr/bin/env bash

export DVND_HOME=`cd src && pwd`
export PYDF_HOME=`cd .. && pwd`

cd test
python2 -m unittest discover
