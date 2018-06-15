# -*- coding: utf-8 -*-
from copy import deepcopy


class SimpleMovement(object):
	def __init__(self, movtype=0, value_i=0, value_j=0, cost=0):
		self.movtype = movtype
		self.value_i = value_i
		self.value_j = value_j
		self.cost = cost

	def __hash__(self):
		return hash((self.movtype, self.value_i, self.value_j, self.cost))

	def __eq__(self, other):
		return self.movtype == other.movtype and self.value_i == other.value_i \
			and self.value_j == other.value_j and self.cost == other.cost


class MovementType(object):
	SWAP = 1
	TWO_OPT = 2
	OR_OPT_K = 3


class Movement(object):
	def __init__(self, movtype=MovementType.SWAP, x=0, y=1, k=None):
		self.movtype = movtype
		self.x = x
		self.y = y
		self.k = k

	def __str__(self):
		return "{ type: %s, x: %d, y: %d%s }" % (self.movtype, self.x, self.y, (", k: %d" % self.k) if self.k is not None else "")

	def __eq__(self, other=None):
		if isinstance(other, self.__class__):
			return self.movtype == other.movtype and self.x == other.x \
				and self.y == other.y and self.k == other.k
		return False

	def __ne__(self, other=None):
		"""Define a non-equality test"""
		return not self.__eq__(other)

	def __hash__(self):
		return hash((self.movtype, self.x, self.y, self.k))

	def conflict(self, mov=None):
		return not self.not_conflict(mov)

	def not_conflict(self, mov=None):
		if self.movtype == MovementType.SWAP:
			if mov.movtype == MovementType.SWAP:
				return abs(self.x - mov.x) > 1 and abs(self.x - mov.y) > 1 \
					and abs(self.y - mov.x) > 1 and abs(self.y - mov.y) > 1
			elif mov.movtype == MovementType.TWO_OPT:
				return ((self.x < mov.x - 1) or (self.x > mov.y - 1)) \
					and ((self.y < mov.x - 1) or (self.y > mov.y + 1))
			elif mov.movtype == MovementType.OR_OPT_K:
				return (self.y < min(mov.x, mov.y) - 1) or (self.x > min(mov.x, mov.y) + mov. k) \
					or ((self.x < min(mov.x, mov.y) - 1) and (self.y > max(mov.x, mov.y) + mov.k))
		elif self.movtype == MovementType.TWO_OPT:
			if mov.movtype == MovementType.SWAP:
				return ((mov.x < self.x - 1) or (mov.x > self.y + 1)) \
					and ((mov.y < self.x - 1) or (mov.y > self.y + 1))
			elif mov.movtype == MovementType.TWO_OPT:
				return (self.y < mov.x - 1) or (self.x > mov.y + 1) \
					or (mov.y > self.x - 1) or (mov.x > self.y + 1)
			elif mov.movtype == MovementType.OR_OPT_K:
				return (self.x > max(mov.x, mov.y) + mov.k) or (self.y < min(mov.x, mov.y) - 1)
		elif self.movtype == MovementType.OR_OPT_K:
			if mov.movtype == MovementType.SWAP:
				return (mov.y < min(self.x, self.y) - 1) or (mov.x > max(self.x, self.y) + self.k) \
					or ((mov.x < min(self.x, self.y) - 1) and (mov.y > max(self.x, self.y) + self.k))
			elif mov.movtype == MovementType.TWO_OPT:
				return (mov.y < min(self.x, self.y) - 1) or (mov.x > max(self.x, self.y) + self.k)
			elif mov.movtype == MovementType.OR_OPT_K:
				return (max(self.x, self.y) + self.k < min(mov.x, mov.y)) \
					or (min(self.x, self.y) > max(mov.x, mov.y) + mov.k)
		return True


def neigh_mov(args=[], inimov=Movement()):
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
