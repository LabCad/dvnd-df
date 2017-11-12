# -*- coding: utf-8 -*-
from random import randint


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

	@property
	def value(self):
		return sum([self.route[i] * (i + 1) for i in xrange(self.__size)]) if self.size > 0 else None

	@property
	def size(self):
		return self.__size

	def swap(self, x, y):
		self.route[x],self.route[y] = self.route[y],self.route[x]
		return self

	def invert(self, x, y):
		self.route[x], self.route[y] = self.route[y], self.route[x]
		for i in xrange(1, (y - x) // 2 + 1):
			self.route[x + i], self.route[y - i] = self.route[y - i], self.route[x + i]
		return self

	def rand(self):
		for i in xrange(self.__size):
			de = randint(self.__size)
			self.route[i], self.route[de] = self.route[de], self.route[i]
