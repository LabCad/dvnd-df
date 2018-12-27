#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os
import os.path
import socket
import numpy
import ctypes
import sys
import include_lib
include_lib.include_simple_pycuda()
from simplepycuda import SimpleSourceModule, SimplePyCuda


array_1d_int = numpy.ctypeslib.ndpointer(dtype=ctypes.c_int, ndim=1, flags='CONTIGUOUS')
array_1d_uint = numpy.ctypeslib.ndpointer(dtype=ctypes.c_uint, ndim=1, flags='CONTIGUOUS')
array_1d_bool = numpy.ctypeslib.ndpointer(dtype=ctypes.c_bool, ndim=1, flags='CONTIGUOUS')
array_1d_short = numpy.ctypeslib.ndpointer(dtype=ctypes.c_short, ndim=1, flags='CONTIGUOUS')
array_1d_ushort = numpy.ctypeslib.ndpointer(dtype=ctypes.c_ushort, ndim=1, flags='CONTIGUOUS')


def hasparam(short_name=None, long_name=None):
	if short_name is not None:
		return "-{}".format(short_name) in sys.argv
	elif long_name is not None:
		return "--{}".format(long_name) in sys.argv
	return False


def getparam(short_name=None, long_name=None, default_value=None):
	if short_name is not None:
		short_name = "-{}".format(short_name)
	if long_name is not None:
		long_name = "--{}".format(long_name)

	if long_name is not None and long_name in sys.argv:
		return sys.argv[sys.argv.index(long_name) + 1]
	elif short_name is not None and short_name in sys.argv:
		return sys.argv[sys.argv.index(short_name) + 1]
	else:
		return default_value


def gethostcode():
	hostname = socket.gethostname()
	hostname_pattern = re.compile("\D*(\d*)")
	hostcode = int(hostname_pattern.match(hostname).group(1) or 0)
	# print "hostcode: {} hostname: {}".format(hostcode, hostname)
	return hostcode


def compilelib(files=[], localpath="", mylibname="", options=[], compiler_options=[], verbose=True):
	if not os.path.isfile(localpath + mylibname + '.so'):
		import time
		if verbose:
			print "Creating file: ", mylibname + '.so'
		cmple_start_time = time.time()
		nvccFile = 'nvcc'
		if os.path.isfile('/usr/local/cuda-8.0/bin/nvcc'):
			nvccFile = '/usr/local/cuda-8.0/bin/nvcc'
		elif os.path.isfile('/usr/local/cuda-9.2/bin/nvcc'):
			nvccFile = '/usr/local/cuda-9.2/bin/nvcc'

		SimpleSourceModule.compile_files(nvccFile, files, options, localpath + mylibname, compiler_options)
		cmple_end_time = time.time()
		if verbose:
			print "File: {}.so created in {}s".format(mylibname, cmple_end_time - cmple_start_time)
	elif verbose:
		print "Using already created file: ", mylibname + '.so'


def getLastCudaError():
	simplePycuda = SimplePyCuda("/home/rodolfo/git/simple-pycuda/")
	return simplePycuda.getLastError()


def getLastCudaErrorString():
	simplePycuda = SimplePyCuda("/home/rodolfo/git/simple-pycuda/")
	return simplePycuda.getErrorEnum(getLastCudaError())
