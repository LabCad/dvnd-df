#!/usr/bin/env bash
git submodule update --remote --init --recursive
sudo apt install python-mpi4py
sudo apt install mpich

# installation for anaconda2: https://www.anaconda.com/download/
#pip install --user virtualenv
#virtualenv -p /usr/bin/python2.7 venv

#source venv/bin/activate
#pip install -r requirements.txt
#deactivate
