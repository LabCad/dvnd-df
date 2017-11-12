# -*- coding: utf-8 -*-
from random import randint
from movement import *


class Solution(object):
	def __init__(self, size, route=None):
		self.__size = size
		if route is None:
			self.route = [x for x in xrange(size)]
		else:
			self.route = [x for x in route]

	def __eq__(self, other):
		"""Define an equality test"""
		if isinstance(other, self.__class__):
			return self.__size == other.__size and self.route == other.route
		return False

	def __ne__(self, other):
		"""Define a non-equality test"""
		return not self.__eq__(other)

	def __lt__(self, other):
		return self.value < other.value

	def __str__(self):
		return "{ size: %d, value: %s, route: %s }" % (self.__size, self.value, self.route)

	def __copy__(self):
		return Solution(self.__size, self.route)

	def __len__(self):
		return self.__size

	@property
	def value(self):
		return sum([self.route[i] * (i + 1) for i in xrange(self.__size)]) if self.__size > 0 else None

	def swap(self, x, y):
		self.route[x], self.route[y] = self.route[y], self.route[x]
		return self

	def tow_opt(self, x, y):
		for i in xrange((y - x) / 2 + 1):
			self.route[x + i], self.route[y - i] = self.route[y - i], self.route[x + i]

	def or_opt_k(self, x, y, k):
		pass

	def invert(self, x, y):
		self.route[x], self.route[y] = self.route[y], self.route[x]
		for i in xrange(1, (y - x) // 2 + 1):
			self.route[x + i], self.route[y - i] = self.route[y - i], self.route[x + i]
		return self

	def rand(self):
		for i in xrange(self.__size):
			de = randint(0, self.__size - 1)
			self.route[i], self.route[de] = self.route[de], self.route[i]
		return self

	def accept(self, mov):
		if mov.movtype == MovementType.SWAP:
			self.swap(mov.x, mov.y)
		elif mov.movtype == MovementType.TWO_OPT:
			self.tow_opt(mov.x, mov.y)
		elif mov.movtype == MovementType.OR_OPT_K:
			self.or_opt_k(mov.x, mov.y, mov.k)
		return self
