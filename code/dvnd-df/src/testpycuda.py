#!/usr/bin/python
# -*- coding: utf-8 -*-
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


main()
