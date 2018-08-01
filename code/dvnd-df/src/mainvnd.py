#!/usr/bin/python
# -*- coding: utf-8 -*-
# from dataflow_opt import *
import random
import time
import numpy
from multiprocessing.pool import ThreadPool
import threading
from copy import deepcopy
from wraper_wamca2016 import WamcaWraper, get_file_name
from cmdparam import CommandParams

# Command line parameters
param = CommandParams(solver="dvnd")

start_time = time.time()

file_name = get_file_name(param.solution_index)
mylib = WamcaWraper(file_name, useMultipleGpu=param.multi_gpu, deviceCount=param.device_count)
ini_solution = mylib.create_initial_solution(param.solution_index, param.solver, param.solution_instance_index)

neigh_op = [lambda ab, y=mv: mylib.neigh_gpu(ab, y) for mv in xrange(5)]
print "ns: ", neigh_op
random.shuffle(neigh_op)
print "ns: ", neigh_op
print ini_solution

start_time = time.time()
counts = [0 for x in xrange(len(neigh_op))]
if "rvnd" == param.solver:
	solution = deepcopy(ini_solution)
	solution2 = deepcopy(solution)
	k = 0
	while k < len(neigh_op):
		counts[k] += 1
		numpy.copyto(solution2.vector, solution.vector)
		solution2.value = solution.value
		resp = mylib.neigh_gpu(solution2, k)
		if resp[0] < solution:
			k = 0
			numpy.copyto(solution.vector, resp[0].vector)
			solution.value = resp[0].value
		else:
			k += 1
elif "dvnd" == param.solver:
	def negigh_dvnd(solution, idx, resp, funfun):
		resp[idx] = funfun(solution)[0]
		return resp[idx]

	neigh_op = [lambda sol, idx, resp, funfun=ope, y=mv: negigh_dvnd(sol, idx, resp, funfun) for ope in neigh_op]
	neigh_count = len(neigh_op)
	solution = deepcopy(ini_solution)
	# pool = ThreadPool(processes=neigh_count)

	melhorou = True
	respostas = [None for x in xrange(neigh_count)]
	while melhorou:
		# my_threads = [pool.apply_async(ope, (mylib.copy_solution(solution), )) for ope in neigh_op]
		my_threads = []
		melhorou = False
		for i in xrange(neigh_count):
			counts[i] += 1
			it_tread = threading.Thread(target=neigh_op[i], args=(mylib.copy_solution(solution), i, respostas))
			it_tread.setDaemon(True)
			it_tread.start()
			my_threads.append(it_tread)

		for i in xrange(neigh_count):
			it_tread = my_threads[i]
			if it_tread.isAlive():
				it_tread.join()
			sol = respostas[i]
			if sol < solution:
				melhorou = True
				solution = sol


end_time = time.time()
print "finished {} in {}s".format(param.solver.upper(), end_time - start_time)
print "data-line;initial_solution;{};final_solution;{};time;{};counts;{};fv;{};cv;{};imp;{}".format(ini_solution.value,
	solution.value, end_time - start_time, sum(counts), [], counts, 1.0 * ini_solution.value / solution.value)
