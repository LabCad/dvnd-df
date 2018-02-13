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
	print "Size: {} - file name: {}".format(sol_info[1], sol_info[0])
	print [x.value for x in args]
	print "Initial: {}".format(ini_solution)
	final_solution = min(args)
	print "Final time: {}s - Best: {}".format(end_time - start_time, final_solution)
	imp_value = 1.0 * ini_solution.value / final_solution.value
	print "Value - initial: {}, final: {}, improveup: {}".format(ini_solution.value, final_solution.value, imp_value)


problem_name = sys.argv[sys.argv.index("-p") + 1] if "-p" in sys.argv else "ml"
neigh_op = []
if "tt" == problem_name.lower():
	from solution import SolutionTTP
	from wraper_ttp import *

	sol_info = ttp_solution_instance_file[solution_index]
	file_name = ttp_intance_path + sol_info[0]

	solint = [x for x in xrange(sol_info[1][0])]
	solbool = [False for x in xrange(sol_info[1][1])]
	ini_solution = SolutionTTP(solint, calculate_value(file_name, solint, solbool), solbool)

	neigh_op = [lambda ab, y=mv: neigh_gpu(ab, file_name, y) for mv in xrange(5)]
elif "ml" == problem_name.lower():
	from wraper_wamca2016 import *
	sol_info = wamca_solution_instance_file[solution_index]
	file_name = wamca_intance_path + sol_info[0]

	solint = [x for x in xrange(sol_info[1])]
	ini_solution = SolutionVectorValue(solint, calculate_value(file_name, solint))

	neigh_op = [lambda ab, y=mv: neigh_gpu(ab, file_name, y) for mv in xrange(5)]

mpi_enabled = "-mpi" in sys.argv
workers = int(sys.argv[sys.argv.index("-n") + 1] if "-n" in sys.argv else 1)
solver_param = sys.argv[sys.argv.index("-s") + 1] if "-s" in sys.argv else "dvnd"

solver = None
if "dvnd" == solver_param.lower():
	solver = DataFlowDVND(False, mpi_enabled)
elif "rvnd" == solver_param.lower():
	solver = DataFlowVND(False, mpi_enabled, True)
elif "vnd" == solver_param.lower():
	solver = DataFlowVND(False, mpi_enabled)

print "Solver: {}".format(solver_param.upper())
start_time = time.time()
solver.run(workers, ini_solution, neigh_op, print_final_solution)
