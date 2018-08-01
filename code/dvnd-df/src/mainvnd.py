#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import time
import numpy
import threading
from copy import deepcopy
from wraper_wamca2016 import WamcaWraper, get_file_name
from cmdparam import CommandParams


class NeighborhoodThread(threading.Thread):
	def __init__(self, fun, sol):
		super(NeighborhoodThread, self).__init__()
		self.setDaemon(True)
		self.resp = None
		self.fun = fun
		self.solution = sol

	def run(self):
		self.resp = self.fun(self.solution)[0]


if __name__ == '__main__':
	# Command line parameters
	param = CommandParams(solver="dvnd", solution_index=7)

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

		# neigh_op = [lambda sol, idx, resp, funfun=ope, y=mv: negigh_dvnd(sol, idx, resp, funfun) for ope in neigh_op]
		neigh_count = len(neigh_op)
		solution = deepcopy(ini_solution)

		melhorou = True
		while melhorou:
			my_threads = [NeighborhoodThread(neigh_op[i], mylib.copy_solution(solution)) for i in xrange(neigh_count)]
			melhorou = False
			for i in xrange(neigh_count):
				counts[i] += 1
				my_threads[i].start()

			for it_tread in my_threads:
				# if it_tread.isAlive():
				it_tread.join()
				if it_tread.resp < solution:
					melhorou = True
					solution = it_tread.resp

			for ope in neigh_op:
				if melhorou:
					break
				resp = ope(solution)[0]
				if resp < solution:
					melhorou = True
					solution = it_tread.resp

	end_time = time.time()
	print "finished {} in {}s".format(param.solver.upper(), end_time - start_time)
	print "data-line;initial_solution;{};final_solution;{};time;{};counts;{};fv;{};cv;{};imp;{}".format(ini_solution.value,
		solution.value, end_time - start_time, sum(counts), [], counts, 1.0 * ini_solution.value / solution.value)

	solution2 = deepcopy(solution)
	k = 0
	counts = [0 for x in xrange(len(neigh_op))]
	start_time = time.time()
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
	end_time = time.time()
	print "finished {} in {}s".format(param.solver.upper(), end_time - start_time)
	print "data-line;initial_solution;{};final_solution;{};time;{};counts;{};fv;{};cv;{};imp;{}".format(ini_solution.value,
		solution.value, end_time - start_time, sum(counts), [], counts, 1.0 * ini_solution.value / solution.value)