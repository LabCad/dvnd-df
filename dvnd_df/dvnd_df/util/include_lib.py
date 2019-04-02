# -*- coding: utf-8 -*-
import sys
import os
import os.path

pydf_home_uff = "/home/imcoelho/Rodolfo/dvnd-df/code/dvnd-df"
pydf_home_local = "/home/rodolfo/git/Sucuri"
simple_pycuda_home_uff = "/home/imcoelho/Rodolfo/dvnd-df/code/dvnd-df/simple-pycuda"
simple_pycuda_home_local = "/home/rodolfo/git/simple-pycuda"


pydf_home = pydf_home_local if os.path.isdir(pydf_home_local) else pydf_home_uff
simple_pycuda_home = simple_pycuda_home_local if os.path.isdir(simple_pycuda_home_local) else simple_pycuda_home_uff

print("pydf_home: {}".format(pydf_home))
print("simple_pycuda_home: {}".format(simple_pycuda_home))

os.environ['PYDF_HOME'] = pydf_home
os.environ['SIMPLE_PYCUDA_HOME'] = simple_pycuda_home


def include_dvnd():
	dvnd_home_var_name = 'DVND_HOME'
	dvnd_home_value = '/home/rodolfo/git/dvnd-df/code/dvnd-df/dvnd-df'
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
	pydf_home_value = '/home/rodolfo/git/simple-pycuda'
	if pydf_home_var_name in os.environ:
		sys.path.append(os.environ[pydf_home_var_name])
	else:
		sys.path.append(pydf_home_value)
