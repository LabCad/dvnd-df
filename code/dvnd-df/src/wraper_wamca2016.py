#!/usr/bin/python
# -*- coding: utf-8 -*-
import ctypes
import numpy
import re
import time
import os
import socket
import include_lib
include_lib.include_simple_pycuda()
from simplepycuda import SimpleSourceModule


array_1d_int = numpy.ctypeslib.ndpointer(dtype=ctypes.c_int, ndim=1, flags='CONTIGUOUS')
# os.getenv('KEY_THAT_MIGHT_EXIST', default_value)
# wamca2016path = os.getenv('WAMCA2016ABSOLUTEPATH', "/home/rodolfo/git/wamca2016/")

# wamca2016path = "/home/imcoelho/Rodolfo/wamca2016/"
wamca2016path = "/home/rodolfo/git/wamca2016/"
# localpath = "/home/imcoelho/Rodolfo/dvnd-df/code/dvnd-df/src/"
localpath = "/home/rodolfo/git/dvnd-df/code/dvnd-df/src/"

print "WAMCAPATH:" + wamca2016path


def gethostcode():
	hostname = socket.gethostname()
	hostname_pattern = re.compile("\D*(\d*)")
	hostcode = int(hostname_pattern.match(hostname).group(1) or 0)
	# print "hostcode: {} hostname: {}".format(hostcode, hostname)
	return hostcode


def create_wamca2016lib():
	mylibname = 'wamca2016lib'
	if not os.path.isfile(localpath + mylibname + '.so'):
		print "Creating file: ", mylibname + '.so'
		cmple_start_time = time.time()
		wamca_files = [wamca2016path + "source/*.cu", wamca2016path + "source/*.cpp"]
		SimpleSourceModule.compile_files('nvcc', wamca_files, [], localpath + mylibname)
		cmple_end_time = time.time()
		print "File: {}.so created in {}s".format(mylibname, cmple_end_time - cmple_start_time)
	else:
		print "Using already created file: ", mylibname + '.so'

	mylib = ctypes.cdll.LoadLibrary("{}{}.so".format(localpath, mylibname))

	# unsigned int bestNeighbor(char * file, int *solution, unsigned int solutionSize, int neighborhood,
	# 	bool justCalc = false, unsigned int hostCode = 0) {
	mylib.bestNeighbor.argtypes = [ctypes.c_void_p, array_1d_int, ctypes.c_uint, ctypes.c_int, ctypes.c_bool,
		ctypes.c_uint]
	# char * file, int *solution, unsigned int solutionSize, int neighborhood, bool justCalc = false
	# mylib.bestNeighbor.argtypes = [ctypes.c_void_p, array_1d_int, ctypes.c_uint, ctypes.c_int, ctypes.c_bool]
	mylib.bestNeighbor.restype = ctypes.c_uint
	# ctypes.POINTER(c_int)

	return mylib


wamca2016lib = create_wamca2016lib()


def calculate_value(file_name, solint):
	return best_neighbor(file_name, solint, 1, True)[1]


def best_neighbor(file, solint, neighborhood, justcalc=False):
	csolint = numpy.array(solint, dtype=ctypes.c_int)
	resp = wamca2016lib.bestNeighbor(file, csolint, len(solint), neighborhood, justcalc, gethostcode())
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
	("08_TRP-S1000-R1.tsp", 1001),
	# http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/
	# 08
	("u1060.tsp", 1060),
	("vm1084.tsp", 1084),
	("u1432.tsp", 1432),
	("vm1748.tsp", 1748),
	("u1817.tsp", 1817),
	("rl1889.tsp", 1889),
	("u2152.tsp", 2152),
	# 15
	("u2319.tsp", 2319),
	("fnl4461.tsp", 4461),
	("rl5915.tsp", 5915),
	("rl5934.tsp", 5934),
	("rl11849.tsp", 11849),
	# 20
	("usa13509.tsp", 13509),
	("d18512.tsp", 18512)
]
