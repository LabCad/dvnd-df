#!/usr/bin/python
# -*- coding: utf-8 -*-
import ctypes
import numpy
from include_lib import *
include_simple_pycuda()
from simplepycuda import SimplePyCuda, SimpleSourceModule, grid, block


def classicExample(cuda):
	a = numpy.random.randn(4, 4)
	a = a.astype(numpy.float32)
	print a
	a_gpu = cuda.mem_alloc(a.nbytes)
	cuda.memcpy_htod(a_gpu, a)
	mod = SimpleSourceModule("""
		#include<stdio.h>
		__global__ void doublify (float* a, int n, int c)
		{
			int idx = threadIdx.x + threadIdx.y*n;
			a[idx] = 2 * a[idx] + c;
		}
	""")
	func = mod.get_function("doublify", False)
	# TODO: this next line will be made automatically in get_function method... just need a few more time :)
	func.set_arguments([ctypes.c_void_p, ctypes.c_int, ctypes.c_int])
	# func.set_arguments([ctypes.c_void_p])
	func(a_gpu, len(a), 100)
	cuda.memcpy_dtoh(a, a_gpu)
	cuda.deviceSynchronize()
	print a
	cuda.free(a_gpu)  # this is not necessary in PyCUDA
	print "Finished"


def main():
	cuda = SimplePyCuda("../simple-pycuda/")

	classicExample(cuda)
	return 0

main()