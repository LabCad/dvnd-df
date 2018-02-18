#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os
import socket
import numpy
import ctypes
import include_lib
include_lib.include_simple_pycuda()
from simplepycuda import SimpleSourceModule


array_1d_int = numpy.ctypeslib.ndpointer(dtype=ctypes.c_int, ndim=1, flags='CONTIGUOUS')
array_1d_bool = numpy.ctypeslib.ndpointer(dtype=ctypes.c_bool, ndim=1, flags='CONTIGUOUS')


def gethostcode():
	hostname = socket.gethostname()
	hostname_pattern = re.compile("\D*(\d*)")
	hostcode = int(hostname_pattern.match(hostname).group(1) or 0)
	# print "hostcode: {} hostname: {}".format(hostcode, hostname)
	return hostcode


def compilelib(files, localpath, mylibname, options=[]):
	if not os.path.isfile(localpath + mylibname + '.so'):
		import time
		print "Creating file: ", mylibname + '.so'
		cmple_start_time = time.time()
		SimpleSourceModule.compile_files('nvcc', files, options, localpath + mylibname)
		cmple_end_time = time.time()
		print "File: {}.so created in {}s".format(mylibname, cmple_end_time - cmple_start_time)
	else:
		print "Using already created file: ", mylibname + '.so'
