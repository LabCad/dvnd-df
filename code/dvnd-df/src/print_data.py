# -*- coding: utf-8 -*-
import time


def print_final_solution(solutions=[], ini_sol=None, initial_time=0, metadata=None, param=None):
	"""
	:param solutions: Lista de soluções encontradas por cada estratégia.
	:param counts: Lista com quantidade de vizinhanças exploradas por estratégia.
	:param ini_sol: Initial solution.
	:param initial_time: Timestamp at the process begin.
	:param metadata: Metadata information.
	:param param: Command line parameters.
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