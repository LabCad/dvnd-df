# -*- coding: utf-8 -*-
from random import randint
from movement import *


class Solution(object):
	def __init__(self, size, route=None):
		self.__size = size
		if route is None:
			self.__route = [x for x in xrange(size)]
		else:
			self.__route = [x for x in route]

	def __eq__(self, other):
		"""Define an equality test"""
		if isinstance(other, self.__class__):
			return self.__size == other.__size and self.__route == other.__route
		return False

	def __ne__(self, other):
		"""Define a non-equality test"""
		return not self.__eq__(other)

	def __lt__(self, other):
		return self.value < other.value

	def __str__(self):
		return "{ size: %d, value: %s, route: %s }" % (self.__size, self.value, self.__route)

	def __copy__(self):
		return Solution(self.__size, self.__route)

	def __len__(self):
		return self.__size

	@property
	def value(self):
		return sum([self.__route[i] * (i + 1) for i in xrange(self.__size)]) if self.__size > 0 else None

	@property
	def get_route(self):
		return [x for x in self.__route]

	def swap(self, x, y):
		self.__route[x], self.__route[y] = self.__route[y], self.__route[x]
		return self

	def two_opt(self, x, y):
		for i in xrange((y - x) / 2 + 1):
			self.__route[x + i], self.__route[y - i] = self.__route[y - i], self.__route[x + i]
		return self

	def oropt_k(self, x, y, k):
		if k < y - x:
			temp = []
			for i in xrange(x, min(self.__size, x + k)):
				temp.append(self.__route[i])
			for i in xrange(x, y):
				self.__route[i] = self.__route[i + k]
			for i in xrange(y, min(self.__size, y + len(temp))):
				self.__route[i] = temp[i - y]
		return self

	def invert(self, x, y):
		self.__route[x], self.__route[y] = self.__route[y], self.__route[x]
		for i in xrange(1, (y - x) // 2 + 1):
			self.__route[x + i], self.__route[y - i] = self.__route[y - i], self.__route[x + i]
		return self

	def rand(self):
		for i in xrange(self.__size):
			de = randint(0, self.__size - 1)
			self.__route[i], self.__route[de] = self.__route[de], self.__route[i]
		return self

	def accept(self, mov):
		if mov.movtype == MovementType.SWAP:
			self.swap(mov.x, mov.y)
		elif mov.movtype == MovementType.TWO_OPT:
			self.two_opt(mov.x, mov.y)
		elif mov.movtype == MovementType.OR_OPT_K:
			self.oropt_k(mov.x, mov.y, mov.k)
		return self
