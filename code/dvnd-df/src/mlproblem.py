#!/usr/bin/python
# -*- coding: utf-8 -*-
from movement import *
from copy import deepcopy
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