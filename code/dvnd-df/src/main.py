#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import sys
from dataflow_opt import *

start_time = time.time()
solution_index = int(0 if "-in" not in sys.argv else sys.argv[sys.argv.index("-in") + 1])
# solution_in_index = None if "-sn" not in sys.argv else int(sys.argv[sys.argv.index("-sn") + 1])
file_name = None
ini_solution = None


def print_final_solution(args, counts):
	end_time = time.time()
	values_vec = [x.value for x in args]
	print "solutions: {}, counts: {}".format(values_vec, counts)
	print "Initial: {}".format(ini_solution)
	final_solution = min(args)
	elapsed_time = end_time - start_time
	ini_value = ini_solution.value
	fin_value = final_solution.value
	print "Final time: {}s - Best: {}".format(elapsed_time, final_solution)
	imp_value = None
	if abs(fin_value * 1.0) > 0.00001:
		imp_value = 1.0 * ini_value / fin_value
	print "Value - initial: {}, final: {}, improveup: {}".format(ini_value, fin_value, imp_value)
	print "data-line;i;{};f;{};t;{};c;{};fv;{};cv;{};imp;{}".format(
		ini_value, fin_value, elapsed_time, sum(counts), values_vec, counts, imp_value)


def testconflict(ini_solution = None, nmoves = 10):
	from wraper_wamca2016 import best_neighbor_moves, get_no_conflict, merge_moves, apply_moves, calculate_value
	moves0 = best_neighbor_moves(file_name, ini_solution.vector, 0, n_moves=nmoves)[2]
	moves1 = best_neighbor_moves(file_name, ini_solution.vector, 1, n_moves=nmoves)[2]
	moves2 = best_neighbor_moves(file_name, ini_solution.vector, 2, n_moves=nmoves)[2]
	moves3 = best_neighbor_moves(file_name, ini_solution.vector, 3, n_moves=nmoves)[2]
	moves4 = best_neighbor_moves(file_name, ini_solution.vector, 4, n_moves=nmoves)[2]
	moves = merge_moves(merge_moves(merge_moves(moves0, moves1), merge_moves(moves2, moves3)), moves4)
	no_conflict_moves = get_no_conflict(moves[0], moves[1], moves[2], moves[3])

	valor_antes = calculate_value(file_name, ini_solution.vector)
	print "antes  value: {} - {}".format(valor_antes, str(ini_solution.vector))
	apply_moves(file_name, ini_solution.vector, no_conflict_moves[0], no_conflict_moves[1],
		no_conflict_moves[2], no_conflict_moves[3])
	ini_solution.value = calculate_value(file_name, ini_solution.vector)
	print "depois value: {} - {}".format(ini_solution.value, str(ini_solution.vector))
	print "{}-{}={} -- {}".format(ini_solution.value, valor_antes, ini_solution.value - valor_antes, no_conflict_moves[4])
	# print "moves: ", ["{}".format(str(x)) for x in moves[2]]


goal = (sys.argv[sys.argv.index("--goal") + 1] if "--goal" in sys.argv else "min").lower() == "max"
problem_name = sys.argv[sys.argv.index("-p") + 1] if "-p" in sys.argv else "ml"
neigh_op = []
# problem_name = "tt"
if "tt" == problem_name.lower():
	from wraper_ttp import create_initial_solution, neigh_gpu, get_file_name
	file_name = get_file_name(solution_index)
	ini_solution = create_initial_solution(solution_index)

	neigh_op = [lambda ab, y=mv: neigh_gpu(ab, file_name, y) for mv in xrange(5)]
	goal = True
elif "ml" == problem_name.lower():
	from solution import SolutionVectorValue
	from wraper_wamca2016 import create_initial_solution, neigh_gpu, get_file_name, best_neighbor_moves, \
		get_no_conflict, merge_moves, copy_solution#, apply_moves, calculate_value, best_neighbor
	# import numpy
	file_name = get_file_name(solution_index)
	ini_solution = create_initial_solution(solution_index)

	neigh_op = [lambda ab, y=mv: neigh_gpu(ab, file_name, y) for mv in xrange(5)]
	# nmoves = 10
	# moves0 = best_neighbor_moves(file_name, ini_solution.vector, 0, n_moves=nmoves)[2]
	# moves1 = best_neighbor_moves(file_name, ini_solution.vector, 1, n_moves=nmoves)[2]
	# moves = merge_moves(moves0, moves1)
	# get_no_conflict(moves[0], moves[1], moves[2], moves[3])
	# print "moves: ", ["{}".format(str(x)) for x in moves[2]]
	testconflict(copy_solution(ini_solution))

print "Value - initial: {} - {}".format(ini_solution, ini_solution.value)

# TODO Versão 2 precisa do MPI enabled, bug
# mpi_enabled = True
mpi_enabled = "-mpi" in sys.argv

workers = int(sys.argv[sys.argv.index("-n") + 1] if "-n" in sys.argv else 1)
solver_param = (sys.argv[sys.argv.index("-s") + 1] if "-s" in sys.argv else "dvnd").lower()

# FIXME Remover
# solver_param="rvnd"
solver = None
if "dvnd" == solver_param:
	solver = DataFlowDVND(goal, mpi_enabled)
elif "rvnd" == solver_param:
	solver = DataFlowVND(goal, mpi_enabled, True)
elif "vnd" == solver_param:
	solver = DataFlowVND(goal, mpi_enabled)
elif "gdvnd" == solver_param:
	solver = DataFlowGDVND(goal, mpi_enabled)

print "Solver: {}".format(solver_param.upper())
start_time = time.time()
# solver.run(workers, ini_solution, neigh_op, print_final_solution)
