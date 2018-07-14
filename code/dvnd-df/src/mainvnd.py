#!/usr/bin/python
# -*- coding: utf-8 -*-
# from dataflow_opt import *
import random
import time
import numpy
from copy import deepcopy
from wraper_wamca2016 import WamcaWraper, get_file_name
from util import hasparam, getparam

# Command line parameters
solution_index = int(getparam("in", None, 0))
solution_instance_index = int(getparam("sii", "solution_instance_index", -1))
# solution_in_index = None if "-sn" not in sys.argv else int(sys.argv[sys.argv.index("-sn") + 1])
multi_gpu = hasparam("mg", "multi_gpu")
goal = getparam(None, "goal", "min").lower() == "max"
problem_name = getparam("p", None, "ml")
number_of_moves = int(getparam(None, "number_of_moves", 10))
device_count = int(getparam("dc", "device_count", 1))
solver_param = getparam("s", "solver", "dvnd").lower()
mpi_enabled = hasparam("mpi")
workers = int(getparam("n", None, 1))

start_time = time.time()

file_name = get_file_name(solution_index)
mylib = WamcaWraper(file_name, useMultipleGpu=multi_gpu, deviceCount=device_count)
file_name = get_file_name(solution_index)
ini_solution = mylib.create_initial_solution(solution_index, solver_param, solution_instance_index)

neigh_op = [lambda ab, y=mv: mylib.neigh_gpu(ab, y) for mv in xrange(5)]
print "ns: ", neigh_op
random.shuffle(neigh_op)
print "ns: ", neigh_op
print ini_solution

start_time = time.time()
solution = deepcopy(ini_solution)
solution2 = deepcopy(solution)
k = 0
while k < len(neigh_op):
	# print "Start k=", k, " f=", solution.value,
	# for i in xrange(len(solution.vector)):
	# 	solution2.vector[i] = solution.vector[i]
	numpy.copyto(solution2.vector, solution.vector)
	solution2.value = solution.value
	# resp = best_neighbor(file_name, solution2.vector, k)
	resp = mylib.neigh_gpu(solution2, k)
	# print "out k=", k, " -> ", resp[1]
	if resp[0] < solution:
		k = 0
		numpy.copyto(solution.vector, resp[0].vector)
		# solution.vector = resp[0]
		solution.value = resp[0].value
		# solution.value = resp[1]
	else:
		k += 1

end_time = time.time()
print "finished rvnd in {}s".format(end_time - start_time)
print "initial_solution={};final_solution={};improveup={};time;{}".format(ini_solution.value, solution.value,
	1.0 * ini_solution.value / solution.value, end_time - start_time)
