#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import sys
from dataflow_opt import *

start_time = time.time()
solution_index = int(0 if "-in" not in sys.argv else sys.argv[sys.argv.index("-in") + 1])
# solution_index = 3
# solution_in_index = None if "-sn" not in sys.argv else int(sys.argv[sys.argv.index("-sn") + 1])


def print_final_solution(args=[], counts=[], ini_sol=None):
	"""
	:param args: Lista de soluções encontradas por cada estratégia.
	:param counts: Lista com quantidade de vizinhanças exploradas por estratégia.
	"""
	end_time = time.time()
	values_vec = [x.value for x in args]
	print "solutions: {}, counts: {}".format(values_vec, counts)
	print "Initial: {}".format(ini_sol)
	final_solution = min(args)
	elapsed_time = end_time - start_time
	ini_value = ini_sol.value
	fin_value = final_solution.value
	print "Final time: {}s - Best: {}".format(elapsed_time, final_solution)
	imp_value = None
	if abs(fin_value * 1.0) > 0.00001:
		imp_value = 1.0 * ini_value / fin_value
	print "Value - initial: {}, final: {}, improveup: {}".format(ini_value, fin_value, imp_value)
	print "data-line;i;{};f;{};t;{};c;{};fv;{};cv;{};imp;{}".format(
		ini_value, fin_value, elapsed_time, sum(counts), values_vec, counts, imp_value)


goal = (sys.argv[sys.argv.index("--goal") + 1] if "--goal" in sys.argv else "min").lower() == "max"
problem_name = sys.argv[sys.argv.index("-p") + 1] if "-p" in sys.argv else "ml"
number_of_moves = int(sys.argv[sys.argv.index("--number_of_moves") + 1]) if "--number_of_moves" in sys.argv else 10
solver_param = (sys.argv[sys.argv.index("-s") + 1] if "-s" in sys.argv else "dvnd").lower()

# FIXME Remover
solver_param = "gdvnd"
neigh_op = []
ini_solution = None
# problem_name = "tt"
if "tt" == problem_name.lower():
	from wraper_ttp import create_initial_solution, neigh_gpu, get_file_name
	file_name = get_file_name(solution_index)
	ini_solution = create_initial_solution(solution_index)

	neigh_op = [lambda ab, y=mv: neigh_gpu(ab, file_name, y) for mv in xrange(5)]
	goal = True
elif "ml" == problem_name.lower():
	# from solution import SolutionVectorValue
	from wraper_wamca2016 import create_initial_solution, neigh_gpu, get_file_name, neigh_gpu_moves
	# import numpy
	file_name = get_file_name(solution_index)
	ini_solution = create_initial_solution(solution_index, solver_param)

	if "gdvnd" == solver_param:
		neigh_op = [lambda ab, y=mv: neigh_gpu_moves(ab, file_name, y, number_of_moves) for mv in xrange(5)]
	else:
		neigh_op = [lambda ab, y=mv: neigh_gpu(ab, file_name, y) for mv in xrange(5)]
	# nmoves = 10
	# moves0 = best_neighbor_moves(file_name, ini_solution.vector, 0, n_moves=nmoves)[2]
	# moves1 = best_neighbor_moves(file_name, ini_solution.vector, 1, n_moves=nmoves)[2]
	# moves = merge_moves(moves0, moves1)
	# get_no_conflict(moves[0], moves[1], moves[2], moves[3])
	# print "moves: ", ["{}".format(str(x)) for x in moves[2]]
	# testconflict(copy_solution(ini_solution))

print "\nValue - initial: {} - {}".format(ini_solution, ini_solution.value)

# TODO Versão 2 precisa do MPI enabled, bug
# mpi_enabled = True
mpi_enabled = "-mpi" in sys.argv

workers = int(sys.argv[sys.argv.index("-n") + 1] if "-n" in sys.argv else 1)

solver = None
if "dvnd" == solver_param:
	solver = DataFlowDVND(goal, mpi_enabled)
elif "rvnd" == solver_param:
	solver = DataFlowVND(goal, mpi_enabled, True)
elif "vnd" == solver_param:
	solver = DataFlowVND(goal, mpi_enabled)
elif "gdvnd" == solver_param:
	assert "ml" == problem_name.lower(), "Merge solutions not implemented for TTP"
	print("number_of_moves: {}".format(number_of_moves))
	from wraper_wamca2016 import merge_solutions, apply_moves_tuple, calculate_value

	def apply_moves_to_sol_on_oper(sol):
		"""
		Apply the moves to the solution.
		:param sol: Solution
		:return: Solution with the moves applied.
		"""
		if len(sol.movtuple[0]) > 0:
			apply_moves_tuple(file_name, sol.vector, sol.movtuple)
			sol.value = calculate_value(file_name, sol.vector)
		return sol

	solver = DataFlowGDVND(goal, mpi_enabled,
		lambda sol: apply_moves_to_sol_on_oper(sol),
		lambda sols, file=file_name: merge_solutions(sols, file)[0])

print "Solver: {}, number of workers: {}".format(solver_param.upper(), workers)
start_time = time.time()
# ini_solution = None
# print_final_solution(args=[], counts=[], ini_solution=None)
solver.run(workers, ini_solution, neigh_op,
	lambda args, counts, inisol=ini_solution: print_final_solution(args, counts, inisol))



