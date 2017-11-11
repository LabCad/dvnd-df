# -*- coding: utf-8 -*-
from copy import *

class SolutionMovement:
	def __init__(self, sol, mov, imp):
		self.sol = copy(sol)
		self.mov = mov
		self.imp = imp

	def canMerge(self, other):
		return self.sol == other.sol and self.mov.notConflict(other.mov)

class SolutionMovementCollection:
	def __init__(self, sol):
		self.__sol = copy(sol)
		self.__movs = {}
		self.__solvalue = sol.value
		self.__value = None

	@property
	def value(self):
		return self.__solvalue + (self.__value if self.__value != None else sum([value for key, value in self.__movs.iteritems()]))

	def canMerge(self, solmov):
		if self.__sol != solmov.sol:
			return False
		if solmov.mov in self.__movs:
			return True

		for x in self.__movs:
			if x.conflict(solmov.mov):
				return False
		return True

	def merge(self, solmov):
		if self.canMerge(solmov):
			self.__movs[solmov.mov] = solmov.imp
			self.__value = None