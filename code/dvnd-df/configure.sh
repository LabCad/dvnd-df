#!/usr/bin/env bash

sudo apt install python-mpi4py
sudo apt install mpich

# installation for anaconda2: https://www.anaconda.com/download/
pip install virtualenv
virtualenv -p /usr/bin/python2.7 venv

source venv/bin/activate
pip install -r requirements.txt
deactivate
