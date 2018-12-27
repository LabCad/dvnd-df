#!/usr/bin/python
# -*- coding: utf-8 -*-
# import time
from dataflow_opt import *
from wraper_wamca2016 import WamcaWraper
from cmdparam import CommandParams
import traceback


def sig_handler(signum, frame):
	print("---\n")
	print("---\n")
	print("---\nsignal: " + str(signum))
	traceback.print_stack(frame)
	print("local vars")
	for key, value in frame.f_locals.iteritems():
		print("{0}:{1}".format(key, value))
	print("---\n")
	print("---\n")
	print("---\n")
	raise Exception('signal: ' + str(signum))
	# sys.exit(signum)


if __name__ == '__main__':
	# signal.signal(signal.SIGSEGV, sig_handler)

	# Command line parameters
	param = CommandParams(solver="dvnd", solution_index=0, single_output_gate=True, number_of_moves=12)
	print "param: {}".format(param)

	def print_final_solution(solutions=[], ini_sol=None, initial_time=0, metadata=None):
		"""
		:param solutions: Lista de soluções encontradas por cada estratégia.
		:param counts: Lista com quantidade de vizinhanças exploradas por estratégia.
		:param ini_sol: Initial solution.
		:param initial_time: Timestamp at the process begin.
		"""
		end_time = time.time()
		values_vec = [x.value for x in solutions]
		# print "solutions: {}, counts: {}".format(values_vec, metadata.counts)
		print "Initial: {}".format(ini_sol)
		final_solution = min(solutions)
		elapsed_time = end_time - initial_time
		ini_value = ini_sol.value
		fin_value = final_solution.value
		print "Final time: {}s - Best: {}".format(elapsed_time, final_solution)
		imp_value = None
		if abs(fin_value * 1.0) > 1e-5:
			imp_value = 1.0 * ini_value / fin_value
		print "Value - initial: {}, final: {}, improveup: {}".format(ini_value, fin_value, imp_value)
		# linha = "data-line;i;{};f;{};t;{};c;{};fv;{};cv;{};imp;{}".format(
		# ini_value, fin_value, elapsed_time, sum(metadata.counts), values_vec, metadata.counts, imp_value)
		linha = "data-line;i;{};f;{};t;{};c;{};fv;{};cv;{};imp;{}".format(
			ini_value, fin_value, elapsed_time, sum(metadata.counts), values_vec, metadata.counts, imp_value)
		# if "gdvnd" == param.solver:
		# 	linha = "{};mergecount;{};combine_count;{};combine_count_sum;{}".format(linha, metadata.merge_count,
		# 		metadata.combine_count, sum(metadata.combine_count))
		linha = "{};type;{};inum;{};w;{}".format(linha, param.solver, param.solution_index, param.workers)
		if "gdvnd" == param.solver:
			linha = "{};man_time;{}".format(linha, metadata.man_time)
		print ""
		print "solver: {}".format(param.solver.upper())
		print linha
		print ""
		print "time;{};man_time;{};neigh_time;{}".format(elapsed_time, metadata.man_time, metadata.neigh_time)
		print "man_time;{};man_merge_sol;{};man_best_sol;{};man_combine_sol;{}".format(
			metadata.man_time, metadata.man_merge_sol_time, metadata.man_best_sol_time, metadata.man_combine_sol_time)
		print ""


	neigh_op = []
	ini_solution = None
	mylib = None
	if "tt" == param.problem_name:
		from wraper_ttp import create_initial_solution, neigh_gpu, get_file_name
		file_name = get_file_name(param.solution_index)
		if not param.only_compile:
			ini_solution = create_initial_solution(param.solution_index)

			neigh_op = [lambda ab, y=mv: neigh_gpu(ab, file_name, y) for mv in xrange(5)]
		goal = True
	elif "ml" == param.problem_name:
		from wraper_wamca2016 import get_file_name

		file_name = get_file_name(param.solution_index)
		mylib = WamcaWraper(file_name, useMultipleGpu=param.multi_gpu, deviceCount=param.device_count)
		if not param.only_compile:
			ini_solution = mylib.create_initial_solution(param.solution_index, param.solver, param.solution_instance_index)

			if "gdvnd" == param.solver:
				neigh_op = [lambda ab, y=mv: mylib.neigh_gpu_moves(ab, y, param.number_of_moves)
					for mv in xrange(param.number_of_moves)]
			else:
				neigh_op = [lambda ab, y=mv: mylib.neigh_gpu(ab, y) for mv in xrange(param.number_of_moves)]

	if not param.only_compile:
		print "\nValue - initial: {} - {}".format(ini_solution, ini_solution.value)
	is_use_metadata = True

	solver = None
	if param.solver.endswith("_no_df"):
		if "rvnd_no_df" == param.solver or "vnd_no_df" == param.solver:
			solver = VND("rvnd_no_df" == param.solver)
		elif "dvnd_no_df" == param.solver:
			solver = DVND()
	elif "dvnd" == param.solver:
		solver = DataFlowDVND(param.goal, param.mpi_enabled, use_metadata=is_use_metadata,
			use_multiple_output=not param.single_output_gate)
	elif "rvnd" == param.solver:
		solver = DataFlowVND(param.goal, param.mpi_enabled, True)
	elif "vnd" == param.solver:
		solver = DataFlowVND(param.goal, param.mpi_enabled)
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
				lambda sol1, sol2: combine_solutions(sol1, sol2), use_metadata=is_use_metadata,
				use_multiple_output=not param.single_output_gate)

	if not param.only_compile:
		print "Solver: {}, number of workers: {}".format(param.solver.upper(), param.workers)
		start_time = time.time()
		solver.run(param.workers, ini_solution, neigh_op,
			lambda args, metadata, inisol=ini_solution:
				print_final_solution(args, inisol, start_time, metadata))
