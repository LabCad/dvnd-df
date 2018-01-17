# -*- coding: utf-8 -*-
import sys
import os


def include_dvnd():
	dvnd_home_var_name = 'DVND_HOME'
	dvnd_home_value = '/home/rodolfo/git/dvnd-df/code/dvnd-df/src'
	if os.environ.has_key(dvnd_home_var_name):
		sys.path.append(os.environ[dvnd_home_var_name])
	else:
		sys.path.append(dvnd_home_value)


def include_pydf():
	pydf_home_var_name = 'PYDF_HOME'
	pydf_home_value = '/home/rodolfo/git/dvnd-df/code/dvnd-df'
	if os.environ.has_key(pydf_home_var_name):
		sys.path.append(os.environ[pydf_home_var_name])
	else:
		sys.path.append(pydf_home_value)
