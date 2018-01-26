#!/usr/bin/python
# -*- coding: utf-8 -*-

import ctypes
import numpy
from include_lib import *
include_simple_pycuda()
from simplepycuda import SimplePyCuda, SimpleSourceModule, Grid, Block


def best_neighbor(file, solint, neighborhood):
	mylibname = 'wamca2016lib'
	if not os.path.isfile(mylibname + '.so'):
		SimpleSourceModule.compile_files('nvcc',
			["~/git/wamca2016/source/*.cu", "~/git/wamca2016/source/*.cpp"], [], mylibname)

	mylib = ctypes.cdll.LoadLibrary(mylibname + '.so')
	array_1d_int = numpy.ctypeslib.ndpointer(dtype=ctypes.c_int, ndim=1, flags='CONTIGUOUS')
	mylib.bestNeighbor.argtypes = [ctypes.c_void_p, array_1d_int, ctypes.c_uint, ctypes.c_int]
	# ctypes.POINTER(c_int)
	mylib.bestNeighbor.restype = ctypes.c_voidp
	csolint = numpy.array(solint, dtype=ctypes.c_int)
	mylib.bestNeighbor(file, csolint, len(solint), neighborhood)
	solint = list(csolint)
	# solint = list(numpy.ctypeslib.as_array(csolint, shape=(len(solint),)))

	return solint#, resp
