# -*- coding: utf-8 -*-
from copy import *


class SolutionMovement(object):
	def __init__(self, sol, mov, imp):
		self.sol = copy(sol)
		self.mov = mov
		self.imp = imp

	def __str__(self):
		return "{ mov: %s, imp: %s}" % (self.mov, self.imp)

	def can_merge(self, other):
		return self.sol == other.sol and self.mov.not_conflict(other.mov)


class SolutionMovementCollection(object):
	def __init__(self, sol):
		self.__sol = copy(sol)
		self.__movs = {}
		self.__solvalue = sol.value
		self.__value = 0

	def __lt__(self, other):
		return self.value < other.value

	def __str__(self):
		return "{ solution: %s, movs(%d): %s, value: %d%+d=%d }" % \
			(self.__sol, len(self.__movs), ", ".join(["%s" % x for x in list(self.__movs.keys())]), self.__solvalue or 0, self.__value, self.value or 0)

	def __len__(self):
		return len(self.__sol)

	@property
	def value(self):
		return (self.__solvalue + self.__value) if self.__solvalue is not None else None

	def can_merge(self, solmov):
		if self.__sol != solmov.sol:
			return False
		if solmov.mov in self.__movs:
			return True

		for x in self.__movs:
			if x.conflict(solmov.mov):
				return False
		return True

	def merge(self, solmov):
		if self.can_merge(solmov):
			self.__movs[solmov.mov] = solmov.imp
			self.__value += solmov.imp

	def ini_solution_value(self):
		return self.__sol.value

	def ini_solution(self):
		return copy(self.__sol)

	def gen_solution(self):
		sol = copy(self.__sol)
		for x in self.__movs:
			sol.accept(x)
		return sol
