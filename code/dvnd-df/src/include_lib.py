# -*- coding: utf-8 -*-
import sys
import os


def include_dvnd():
	dvnd_home_var_name = 'DVND_HOME'
	dvnd_home_value = '/home/rodolfo/git/dvnd-df/code/dvnd-df/src'
	if dvnd_home_var_name in os.environ:
		sys.path.append(os.environ[dvnd_home_var_name])
	else:
		sys.path.append(dvnd_home_value)


def include_pydf():
	pydf_home_var_name = 'PYDF_HOME'
	pydf_home_value = '/home/rodolfo/git/dvnd-df/code/dvnd-df'
	if pydf_home_var_name in os.environ:
		sys.path.append(os.environ[pydf_home_var_name])
	else:
		sys.path.append(pydf_home_value)


def include_simple_pycuda():
	pydf_home_var_name = 'SIMPLE_PYCUDA_HOME'
	pydf_home_value = '/home/rodolfo/git/dvnd-df/code/dvnd-df/simple-pycuda'
	if pydf_home_var_name in os.environ:
		sys.path.append(os.environ[pydf_home_var_name])
	else:
		sys.path.append(pydf_home_value)
