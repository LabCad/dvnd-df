#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from dataflow_opt import *
from wraper_wamca2016 import WamcaWraper
from cmdparam import CommandParams


# Command line parameters
param = CommandParams()


def print_final_solution(solutions=[], ini_sol=None, initial_time=0, metadata=None):
	"""
	:param solutions: Lista de soluções encontradas por cada estratégia.
	:param counts: Lista com quantidade de vizinhanças exploradas por estratégia.
	:param ini_sol: Initial solution.
	:param initial_time: Timestamp at the process begin.
	"""
	end_time = time.time()
	values_vec = [x.value for x in solutions]
	print "solutions: {}, counts: {}".format(values_vec, metadata.counts)
	print "Initial: {}".format(ini_sol)
	final_solution = min(solutions)
	elapsed_time = end_time - initial_time
	ini_value = ini_sol.value
	fin_value = final_solution.value
	print "Final time: {}s - Best: {}".format(elapsed_time, final_solution)
	imp_value = None
	if abs(fin_value * 1.0) > 0.00001:
		imp_value = 1.0 * ini_value / fin_value
	print "Value - initial: {}, final: {}, improveup: {}".format(ini_value, fin_value, imp_value)
	linha = "data-line;i;{};f;{};t;{};c;{};fv;{};cv;{};imp;{}".format(
		ini_value, fin_value, elapsed_time, sum(metadata.counts), values_vec, metadata.counts, imp_value)
	if "gdvnd" == param.solver:
		linha = "{};mergecount;{};combine_count;{};combine_count_sum;{}".format(linha, metadata.merge_count,
			metadata.combine_count, sum(metadata.combine_count))
	print linha
	if metadata is not None:
		print("\nage;{};".format(metadata.age))
		print("\nmanager_time;{};man_get_best_time;{};man_update_data_time;{}\nmanager_merge_time;{}".
			format(metadata.man_time, metadata.man_get_best_time, metadata.man_update_data_time, metadata.man_merge_time))

		print("\nneighbor_time;{};neighbor_proc_before;{};neighbor_func;{}".format(
			metadata.neighbor_time, metadata.neighbor_proc_before_time, metadata.neighbor_func_time))
		print("neighbor_func_inner_time;{};neighbor_func_numpy_alloc_time;{}".format(
			metadata.neighbor_func_inner_time, metadata.neighbor_func_numpy_alloc_time))
		print("neighbor_func_mpi_time;{};neighbor_func_numpy_resize_time;{}".format(
			metadata.neighbor_func_mpi_time, metadata.neighbor_func_numpy_resize_time))
		print("neighbor_func_rest;{}".format(
			metadata.neighbor_func_rest))

		# print("\n%;manager_time/total_time;{};neighbor_time/total_time;{}".format(100.0 * metadata.man_time / elapsed_time,
		# 	100.0 * metadata.neighbor_time / elapsed_time))
		#
		# print("%;merge/manager;{}".format(100.0 * metadata.man_merge_time / metadata.man_time))
		# print("%;process/neighbor;{};func/neighbor;{}".format(
		# 	100.0 * metadata.neighbor_proc_before_time / metadata.neighbor_time,
		# 	100.0 * metadata.neighbor_func_time / metadata.neighbor_time))
	print ""


neigh_op = []
ini_solution = None
mylib = None
if "tt" == param.problem_name:
	from wraper_ttp import create_initial_solution, neigh_gpu, get_file_name
	file_name = get_file_name(param.solution_index)
	ini_solution = create_initial_solution(param.solution_index)

	neigh_op = [lambda ab, y=mv: neigh_gpu(ab, file_name, y) for mv in xrange(5)]
	goal = True
elif "ml" == param.problem_name:
	from wraper_wamca2016 import get_file_name
	file_name = get_file_name(param.solution_index)
	mylib = WamcaWraper(file_name, useMultipleGpu=param.multi_gpu, deviceCount=param.device_count)
	ini_solution = mylib.create_initial_solution(param.solution_index, param.solver, param.solution_instance_index)

	if "gdvnd" == param.solver:
		neigh_op = [lambda ab, y=mv: mylib.neigh_gpu_moves(ab, y, param.number_of_moves) for mv in xrange(5)]
	else:
		neigh_op = [lambda ab, y=mv: mylib.neigh_gpu(ab, y) for mv in xrange(5)]

print "\nValue - initial: {} - {}".format(ini_solution, ini_solution.value)
is_use_metadata = True
solver = None
if "dvnd" == param.solver:
	solver = DataFlowDVND(goal, param.mpi_enabled, use_metadata=is_use_metadata)
elif "rvnd" == param.solver:
	solver = DataFlowVND(goal, param.mpi_enabled, True)
elif "vnd" == param.solver:
	solver = DataFlowVND(goal, param.mpi_enabled)
elif "gdvnd" == param.solver:
	assert "ml" == param.problem_name, "Merge solutions not implemented for TTP"
	print("number_of_moves: {}".format(param.number_of_moves))

	def apply_moves_to_sol_on_oper(sol):
		"""
		Apply the moves to the solution.
		:param sol: Solution
		:return: Solution with the moves applied.
		"""
		if len(sol.movtuple[0]) > 0:
			mylib.apply_moves(sol)
		return sol

	def combine_solutions(sol1, sol2):
		return mylib.merge_independent_movements(sol1, sol2)

	solver = DataFlowGDVND(param.goal, param.mpi_enabled,
		apply_moves_to_sol_on_oper,
		mylib.merge_common_movs,
		lambda sol1, sol2: combine_solutions(sol1, sol2), use_metadata=is_use_metadata)

print "Solver: {}, number of workers: {}".format(param.solver.upper(), param.workers)
start_time = time.time()
solver.run(param.workers, ini_solution, neigh_op,
	lambda args, metadata, inisol=ini_solution:
		print_final_solution(args, inisol, start_time, metadata))
