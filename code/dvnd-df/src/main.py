#!/usr/bin/python
# -*- coding: utf-8 -*-
from copy import deepcopy
from dataflow_opt import *
from movement import *
from solution import Solution
from solution_info import *


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


def print_final_solution(args):
	print "Fim - best: {}".format(args[0].get_best())


sol_info = SolutionInfoEuclidianPosition(
	[(0, 0), (20, 0), (10, 0), (50,  0), (100, 0), (30, 0), (40, 0), (5, 0), (110, 0), (60, 0), (-10, 0)])
ini_solution = Solution(sol_info)

solver = DataFlowOpt()
solver.run(2, ini_solution,
	[lambda x, y=mv: neigh_mov(x, y) for mv in [Movement(MovementType.SWAP), Movement(MovementType.TWO_OPT)]],
	print_final_solution)

print "solinfo->", sol_info
print "sol->", ini_solution
print "sol->", Solution(sol_info, [10, 0, 7, 2, 1, 5, 6, 3, 9, 4, 8])
