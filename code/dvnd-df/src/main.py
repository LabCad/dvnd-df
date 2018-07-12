#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from util import hasparam, getparam
from dataflow_opt import *
from wraper_wamca2016 import WamcaWraper


# Command line parameters
solution_index = int(getparam("in", None, 0))
solution_instance_index = int(getparam("sii", "solution_instance_index", -1))
# solution_in_index = None if "-sn" not in sys.argv else int(sys.argv[sys.argv.index("-sn") + 1])
multi_gpu = hasparam("mg", "multi_gpu")
goal = getparam(None, "goal", "min").lower() == "max"
problem_name = getparam("p", None, "ml")
number_of_moves = int(getparam(None, "number_of_moves", 10))
device_count = int(getparam("dc", "device_count", 1))
solver_param = getparam("s", "solver", "gdvnd").lower()
# TODO Versão 2 precisa do MPI enabled, bug
# mpi_enabled = True
mpi_enabled = hasparam("mpi")
workers = int(getparam("n", None, 1))


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
	if "gdvnd" == solver_param:
		linha = "{};mergecount;{};combine_count;{};combine_count_sum;{}".format(linha, metadata.merge_count,
			metadata.combine_count, sum(metadata.combine_count))
	print linha
	if metadata is not None:
		print("\nage;{};".format(metadata.age))
		print("\nmanager_time;{};manager_merge_time;{}".format(metadata.man_time, metadata.man_merge_time))

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
if "tt" == problem_name.lower():
	from wraper_ttp import create_initial_solution, neigh_gpu, get_file_name
	file_name = get_file_name(solution_index)
	ini_solution = create_initial_solution(solution_index)

	neigh_op = [lambda ab, y=mv: neigh_gpu(ab, file_name, y) for mv in xrange(5)]
	goal = True
elif "ml" == problem_name.lower():
	from wraper_wamca2016 import get_file_name
	file_name = get_file_name(solution_index)
	mylib = WamcaWraper(file_name, useMultipleGpu=multi_gpu, deviceCount=device_count)
	ini_solution = mylib.create_initial_solution(solution_index, solver_param, solution_instance_index)

	if "gdvnd" == solver_param:
		neigh_op = [lambda ab, y=mv: mylib.neigh_gpu_moves(ab, y, number_of_moves) for mv in xrange(5)]
	else:
		neigh_op = [lambda ab, y=mv: mylib.neigh_gpu(ab, y) for mv in xrange(5)]

print "\nValue - initial: {} - {}".format(ini_solution, ini_solution.value)
is_use_metadata = True
solver = None
if "dvnd" == solver_param:
	solver = DataFlowDVND(goal, mpi_enabled, use_metadata=is_use_metadata)
elif "rvnd" == solver_param:
	solver = DataFlowVND(goal, mpi_enabled, True)
elif "vnd" == solver_param:
	solver = DataFlowVND(goal, mpi_enabled)
elif "gdvnd" == solver_param:
	assert "ml" == problem_name.lower(), "Merge solutions not implemented for TTP"
	print("number_of_moves: {}".format(number_of_moves))

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

	solver = DataFlowGDVND(goal, mpi_enabled,
		lambda sol: apply_moves_to_sol_on_oper(sol),
		lambda sols: mylib.merge_common_movs(sols),
		lambda sol1, sol2: combine_solutions(sol1, sol2), use_metadata=is_use_metadata)

print "Solver: {}, number of workers: {}".format(solver_param.upper(), workers)
start_time = time.time()
solver.run(workers, ini_solution, neigh_op,
	lambda args, metadata, inisol=ini_solution:
		print_final_solution(args, inisol, start_time, metadata))
