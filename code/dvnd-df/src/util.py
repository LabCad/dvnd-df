#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os
import os.path
import socket
import numpy
import ctypes
import include_lib
include_lib.include_simple_pycuda()
from simplepycuda import SimpleSourceModule, SimplePyCuda


array_1d_int = numpy.ctypeslib.ndpointer(dtype=ctypes.c_int, ndim=1, flags='CONTIGUOUS')
array_1d_uint = numpy.ctypeslib.ndpointer(dtype=ctypes.c_uint, ndim=1, flags='CONTIGUOUS')
array_1d_bool = numpy.ctypeslib.ndpointer(dtype=ctypes.c_bool, ndim=1, flags='CONTIGUOUS')
array_1d_short = numpy.ctypeslib.ndpointer(dtype=ctypes.c_short, ndim=1, flags='CONTIGUOUS')
array_1d_ushort = numpy.ctypeslib.ndpointer(dtype=ctypes.c_ushort, ndim=1, flags='CONTIGUOUS')


def gethostcode():
	hostname = socket.gethostname()
	hostname_pattern = re.compile("\D*(\d*)")
	hostcode = int(hostname_pattern.match(hostname).group(1) or 0)
	# print "hostcode: {} hostname: {}".format(hostcode, hostname)
	return hostcode


def compilelib(files=[], localpath="", mylibname="", options=[], compiler_options=[]):
	if not os.path.isfile(localpath + mylibname + '.so'):
		import time
		print "Creating file: ", mylibname + '.so'
		cmple_start_time = time.time()
		nvccFile = 'nvcc'
		if os.path.isfile('/usr/local/cuda-8.0/bin/nvcc'):
			nvccFile = '/usr/local/cuda-8.0/bin/nvcc'
		elif os.path.isfile('/usr/local/cuda-9.2/bin/nvcc'):
			nvccFile = '/usr/local/cuda-9.2/bin/nvcc'

		SimpleSourceModule.compile_files(nvccFile, files, options, localpath + mylibname, compiler_options)
		cmple_end_time = time.time()
		print "File: {}.so created in {}s".format(mylibname, cmple_end_time - cmple_start_time)
	else:
		print "Using already created file: ", mylibname + '.so'


def getLastCudaError():
	simplePycuda = SimplePyCuda("/home/rodolfo/git/simple-pycuda/")
	return simplePycuda.getLastError()


def getLastCudaErrorString():
	simplePycuda = SimplePyCuda("/home/rodolfo/git/simple-pycuda/")
	return simplePycuda.getErrorEnum(getLastCudaError())
