#!/usr/bin/python
# -*- coding: utf-8 -*-
import ctypes
import numpy
import time
from include_lib import *
include_simple_pycuda()
from simplepycuda import SimplePyCuda, SimpleSourceModule, Grid, Block


def matmul(a, n, c):
	for i in xrange(n):
		for j in xrange(n):
			a[i][j] = 2 * a[i][j] + c


def classic_example(cuda):
	n = 4
	a = numpy.random.randn(n, n)
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
	tgpu = time.time()
	func(a_gpu, len(a), 100)
	cuda.deviceSynchronize()
	tgpu2 = time.time()
	# tcpu = time.time()
	# matmul(a, len(a), 100)
	# tcpu2 = time.time()
	print a

	cuda.memcpy_dtoh(a, a_gpu)
	cuda.deviceSynchronize()
	print a
	cuda.free(a_gpu)  # this is not necessary in PyCUDA
	print "gpu: {}".format(tgpu2 - tgpu)
	# print "cpu: {}, gpu: {}, imp: {}".format(tcpu2 - tcpu, tgpu2 - tgpu, (tcpu2 - tcpu) / (tgpu2 - tgpu))
	print "Finished"


def main():
	cuda = SimplePyCuda("../simple-pycuda/")

	classic_example(cuda)
	return 0


# main()


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

	return solint


intance_path = "~/git/wamca2016/instances/"
solution_instance_file = [
	"01_berlin52.tsp", "02_kroD100.tsp",
	"03_pr226.tsp", "04_lin318.tsp",
	"05_TRP-S500-R1.tsp", "06_d657.tsp",
	"07_rat784.tsp", "08_TRP-S1000-R1.tsp"
]
solint = [x for x in xrange(10)]
print "{} - {}".format(solint, best_neighbor(intance_path + solution_instance_file[4], solint, 1))
