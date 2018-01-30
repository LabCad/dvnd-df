#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
# os.environ['PYDF_HOME'] = "/home/imcoelho/Rodolfo/dvnd-df/code/dvnd-df"
os.environ['PYDF_HOME'] = "/home/rodolfo/git/dvnd-df/code/dvnd-df"
# os.environ['SIMPLE_PYCUDA_HOME'] = "/home/imcoelho/Rodolfo/dvnd-df/code/dvnd-df/simple-pycuda"
os.environ['SIMPLE_PYCUDA_HOME'] = "/home/rodolfo/git/dvnd-df/code/dvnd-df/simple-pycuda"

from copy import deepcopy
from dataflow_opt import *
from movement import *
from solution import Solution
from solution_info import *
from wraper_wamca2016 import *


class SolutionVectorValue:
	def __init__(self, vector, value):
		self.vector = vector
		self.value = value

	def __lt__(self, other):
		return self.value < other.value

	def __len__(self):
		return len(self.vector)

	def __str__(self):
		return "{}-{}".format(self.value, self.vector)


def neigh_mov(args, inimov):
	atual = args[0]
	# antes = atual[oper_idx]
	# str_antes = "oper{} - sv: {}".format(oper_idx, solvalue)

	# movs = {0: MovementType.SWAP, 1: MovementType.TWO_OPT, 2: MovementType.OR_OPT_K}
	# movtype = movs[oper_idx]
	movsinv = {MovementType.SWAP: 0, MovementType.TWO_OPT: 1, MovementType.OR_OPT_K: 2}
	oper_idx = movsinv[inimov.movtype]
	atual.source = oper_idx
	sol = atual[oper_idx]
	best_val = sol.value
	best_sol = deepcopy(sol)
	sol_copy = deepcopy(sol)
	mov = inimov
	for i in xrange(len(sol)):
		for j in xrange(i + 1, len(sol)):
			mov.x, mov.y = i, j
			# TODO Melhorar implementação com desfazer movimento
			sol_copy.set_route(sol.get_route)
			sol_copy.accept(mov)
			sol_val = sol_copy.value
			if sol_val < best_val:
				best_val = sol_val
				best_sol.set_route(sol_copy.get_route)

	atual[oper_idx] = best_sol
	# print "{}:{}-{}".format(oper_idx, sol, best_sol)

	return atual


def neigh_gpu(solution, file, inimov):
	resp = best_neighbor(file, solution.vector, inimov)
	return SolutionVectorValue(resp[0], resp[1])


def print_final_solution(args):
	print [x.value for x in args]
	print "Fim - best: {}".format(min(args))


solution_index = int(0 if "-in" not in sys.argv else sys.argv[sys.argv.index("-in") + 1])
sol_info = wamca_solution_instance_file[solution_index]
solint = [x for x in xrange(sol_info[1])]
#147511
# solint = [0, 43, 33, 36, 47, 23, 4, 5, 14, 37, 39, 38, 35, 34, 48, 31, 21, 17, 30, 22, 19, 49, 15, 28, 29, 1, 6, 41, 20, 16, 2, 44, 18, 40, 7, 8, 9, 42, 3, 45, 24, 11, 27, 26, 25, 46, 13, 12, 50, 32, 10, 51]
solint = [0, 21, 31, 48, 35, 34, 33, 43, 45, 47, 23, 5, 14, 4, 37, 39, 36, 38, 44, 18, 40, 7, 8, 9, 42, 3, 24, 27, 26, 25, 12, 13, 46, 15, 49, 19, 22, 30, 17, 2, 16, 6, 1, 41, 20, 29, 28, 11, 32, 50, 10, 51]

file_name = wamca_intance_path + sol_info[0]
resp = best_neighbor(file_name, solint, 1, True)
ini_solution = SolutionVectorValue(solint, resp[1])

# ini_solution.vector = list(reversed(ini_solution.vector))
# resp2 = neigh_gpu([{0: ini_solution}], file_name, 0)
# print "resp2: {}".format(resp2[0])
neigh_op = [lambda ab, y=mv: neigh_gpu(ab, file_name, y) for mv in xrange(2)]
# neigh_op = [lambda ab, y=mv: neigh_mov(ab, y) for mv in [Movement(MovementType.SWAP), Movement(MovementType.TWO_OPT)]]

print "Início: {}".format(ini_solution)

mpi_enabled = "-mpi" in sys.argv
workers = int(sys.argv[sys.argv.index("-n") + 1] if "-n" in sys.argv else 4)

solver = DataFlowOpt(False, mpi_enabled)
solver.run(workers, ini_solution, neigh_op, print_final_solution)

# print "solinfo->", sol_info
# print "sol->", ini_solution
# print "sol->", Solution(sol_info, [10, 0, 7, 2, 1, 5, 6, 3, 9, 4, 8])

# resp = best_neighbor(wamca_intance_path + sol_info[0], solint, 1)
# print "oi {} - {}".format(resp[1], resp[0])
