#!/usr/bin/python
# -*- coding: utf-8 -*-
# from dataflow_opt import *
from wraper_wamca2016 import *
import random
import time
import sys
from copy import deepcopy


start_time = time.time()
solution_index = int(0 if "-in" not in sys.argv else sys.argv[sys.argv.index("-in") + 1])
sol_info = wamca_solution_instance_file[solution_index]
file_name = wamca_intance_path + sol_info[0]

solint = [x for x in xrange(sol_info[1])]
from wraper_wamca2016 import create_initial_solution, neigh_gpu, get_file_name#, best_neighbor_moves, \
	# get_no_conflict, merge_moves, apply_moves, calculate_value, best_neighbor
# import numpy
file_name = get_file_name(solution_index)
ini_solution = create_initial_solution(solution_index)
# ini_solution = SolutionVectorValue(solint, calculate_value(file_name, solint))

neigh_op = [lambda ab, y=mv: neigh_gpu(ab, file_name, y) for mv in xrange(3)]
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
	# solution2 = deepcopy(solution)
	for i in xrange(len(solution.vector)):
		solution2.vector[i] = solution.vector[i]
	solution2.value = solution.value
	resp = best_neighbor(file_name, solution2.vector, k)
	# print "out k=", k, " -> ", resp[1]
	if resp[1] < solution.value:
		k = 0
		solution.vector = resp[0]
		solution.value = resp[1]
	else:
		k += 1

end_time = time.time()
print "finished rvnd in {}s".format(end_time - start_time)
print "initial_solution={};final_solution={};improveup={};time;{}".format(ini_solution.value, solution.value,
	1.0 * ini_solution.value / solution.value, end_time - start_time)
