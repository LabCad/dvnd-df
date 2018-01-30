#!/usr/bin/python
# -*- coding: utf-8 -*-
import ctypes
import numpy
import os
from include_lib import *
include_simple_pycuda()
from simplepycuda import SimplePyCuda, SimpleSourceModule, Grid, Block


# os.getenv('KEY_THAT_MIGHT_EXIST', default_value)
# wamca2016path = "/home/rodolfo/git/wamca2016/"
wamca2016path = os.getenv('WAMCA2016ABSOLUTEPATH', "/home/rodolfo/git/wamca2016/")
print "WAMCAPATH:"+wamca2016path


def calculate_value(file, solint):
	# TODO Implementar
	pass


def best_neighbor(file, solint, neighborhood, justcalc=False):
	mylibname = 'wamca2016lib'
	if not os.path.isfile(mylibname + '.so'):
		print "Creating file: ", mylibname + '.so'
		SimpleSourceModule.compile_files('nvcc',
			[wamca2016path + "source/*.cu", wamca2016path + "source/*.cpp"], [], mylibname)
		print "Creating file: ", mylibname + '.so', " created"

	mylib = ctypes.cdll.LoadLibrary(mylibname + '.so')
	array_1d_int = numpy.ctypeslib.ndpointer(dtype=ctypes.c_int, ndim=1, flags='CONTIGUOUS')
	mylib.bestNeighbor.argtypes = [ctypes.c_void_p, array_1d_int, ctypes.c_uint, ctypes.c_int, ctypes.c_bool]
	# ctypes.POINTER(c_int)
	mylib.bestNeighbor.restype = ctypes.c_uint
	csolint = numpy.array(solint, dtype=ctypes.c_int)
	resp = mylib.bestNeighbor(file, csolint, len(solint), neighborhood, justcalc)
	solint = list(csolint)
	# solint = list(numpy.ctypeslib.as_array(csolint, shape=(len(solint),)))

	return solint, resp


wamca_intance_path = wamca2016path + "instances/"
wamca_solution_instance_file = [
	("01_berlin52.tsp", 52),
	("02_kroD100.tsp", 100),
	("03_pr226.tsp", 226),
	("04_lin318.tsp", 318),
	("05_TRP-S500-R1.tsp", 501),
	("06_d657.tsp", 657),
	("07_rat784.tsp", 783),
	("08_TRP-S1000-R1.tsp", 1001)
]
