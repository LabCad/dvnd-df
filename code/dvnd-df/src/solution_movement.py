# -*- coding: utf-8 -*-
from copy import *


class SolutionMovement:
	def __init__(self, sol, mov, imp):
		self.sol = copy(sol)
		self.mov = mov
		self.imp = imp

	def can_merge(self, other):
		return self.sol == other.sol and self.mov.not_conflict(other.mov)


class SolutionMovementCollection:
	def __init__(self, sol):
		self.__sol = copy(sol)
		self.__movs = {}
		self.__solvalue = sol.value
		self.__value = None

	@property
	def value(self):
		return self.__solvalue + (self.__value if self.__value is not None else sum([value for key, value in self.__movs.iteritems()]))

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
			self.__value = None