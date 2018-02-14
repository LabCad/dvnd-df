#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import sys
from dataflow_opt import *

start_time = time.time()
solution_index = int(0 if "-in" not in sys.argv else sys.argv[sys.argv.index("-in") + 1])
file_name = None
ini_solution = None


def print_final_solution(args):
	end_time = time.time()
	print [x.value for x in args]
	print "Initial: {}".format(ini_solution)
	final_solution = min(args)
	print "Final time: {}s - Best: {}".format(end_time - start_time, final_solution)
	imp_value = 1.0 * ini_solution.value / final_solution.value
	print "Value - initial: {}, final: {}, improveup: {}".format(ini_solution.value, final_solution.value, imp_value)


problem_name = sys.argv[sys.argv.index("-p") + 1] if "-p" in sys.argv else "ml"
neigh_op = []
if "tt" == problem_name.lower():
	from wraper_ttp import create_initial_solution, neigh_gpu
	ini_solution = create_initial_solution(solution_index)

	neigh_op = [lambda ab, y=mv: neigh_gpu(ab, file_name, y) for mv in xrange(5)]
elif "ml" == problem_name.lower():
	from wraper_wamca2016 import create_initial_solution, neigh_gpu
	ini_solution = create_initial_solution(solution_index)

	neigh_op = [lambda ab, y=mv: neigh_gpu(ab, file_name, y) for mv in xrange(5)]

mpi_enabled = "-mpi" in sys.argv
workers = int(sys.argv[sys.argv.index("-n") + 1] if "-n" in sys.argv else 1)
solver_param = sys.argv[sys.argv.index("-s") + 1] if "-s" in sys.argv else "dvnd"
goal = (sys.argv[sys.argv.index("--goal") + 1] if "--goal" in sys.argv else "min").lower() == "max"

solver = None
if "dvnd" == solver_param.lower():
	solver = DataFlowDVND(goal, mpi_enabled)
elif "rvnd" == solver_param.lower():
	solver = DataFlowVND(goal, mpi_enabled, True)
elif "vnd" == solver_param.lower():
	solver = DataFlowVND(goal, mpi_enabled)

print "Solver: {}".format(solver_param.upper())
start_time = time.time()
solver.run(workers, ini_solution, neigh_op, print_final_solution)
