#!/usr/bin/python
# -*- coding: utf-8 -*-
from mlproblem import *
from dataflow_opt import *
from wraper_wamca2016 import *

start_time = time.time()
solution_index = int(0 if "-in" not in sys.argv else sys.argv[sys.argv.index("-in") + 1])
sol_info = wamca_solution_instance_file[solution_index]
file_name = wamca_intance_path + sol_info[0]

solint = [x for x in xrange(sol_info[1])]
ini_solution = SolutionVectorValue(solint, calculate_value(file_name, solint))


def print_final_solution(args):
	end_time = time.time()
	print [x.value for x in args]
	print "Initial: {}".format(ini_solution)
	print "Final time: {}s - Best: {}".format(end_time - start_time, min(args))


neigh_op = [lambda ab, y=mv: neigh_gpu(ab, file_name, y) for mv in xrange(5)]

mpi_enabled = "-mpi" in sys.argv
workers = int(sys.argv[sys.argv.index("-n") + 1] if "-n" in sys.argv else 1)

solver_param = sys.argv[sys.argv.index("-s") + 1] if "-s" in sys.argv else "dvnd"

solver = None
if "dvnd" == solver_param:
	print "Solver: DVND"
	solver = DataFlowDVND(False, mpi_enabled)
elif "rvnd" == solver_param:
	print "Solver: RVND"
	solver = DataFlowVND(False, mpi_enabled, True)
else:
	print "Solver: VND"
	solver = DataFlowVND(False, mpi_enabled)
start_time = time.time()
solver.run(workers, ini_solution, neigh_op, print_final_solution)
