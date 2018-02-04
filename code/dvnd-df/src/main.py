#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from mlproblem import *

# os.environ['PYDF_HOME'] = "/home/imcoelho/Rodolfo/dvnd-df/code/dvnd-df"
os.environ['PYDF_HOME'] = "/home/rodolfo/git/dvnd-df/code/dvnd-df"
# os.environ['SIMPLE_PYCUDA_HOME'] = "/home/imcoelho/Rodolfo/dvnd-df/code/dvnd-df/simple-pycuda"
os.environ['SIMPLE_PYCUDA_HOME'] = "/home/rodolfo/git/dvnd-df/code/dvnd-df/simple-pycuda"

from dataflow_opt import *
from wraper_wamca2016 import *


start_time = time.time()


def print_final_solution(args):
	end_time = time.time()
	print [x.value for x in args]
	print "Fim time: {}s - best: {}".format(end_time - start_time, min(args))


solution_index = int(0 if "-in" not in sys.argv else sys.argv[sys.argv.index("-in") + 1])
sol_info = wamca_solution_instance_file[solution_index]
file_name = wamca_intance_path + sol_info[0]

solint = [x for x in xrange(sol_info[1])]
resp = best_neighbor(file_name, solint, 1, True)
ini_solution = SolutionVectorValue(solint, resp[1])

neigh_op = [lambda ab, y=mv: neigh_gpu(ab, file_name, y) for mv in xrange(5)]

print "Início: {}".format(ini_solution)

mpi_enabled = "-mpi" in sys.argv
workers = int(sys.argv[sys.argv.index("-n") + 1] if "-n" in sys.argv else 1)

solver_param = sys.argv[sys.argv.index("-s") + 1] if "-s" in sys.argv else "rvnd"

solver = None
if "dvnd" == solver_param:
	solver = DataFlowDVND(False, mpi_enabled)
elif "rvnd" == solver_param:
	solver = DataFlowVND(False, mpi_enabled, True)
else:
	solver = DataFlowVND(False, mpi_enabled)
start_time = time.time()
solver.run(workers, ini_solution, neigh_op, print_final_solution)
