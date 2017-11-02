# -*- coding: utf-8 -*-
from random import randint

class Solution(object):
	def __init__(self, size, route = None):
		self.size = size
		if route == None:
			self.route = [x for x in xrange(size)]
		else:
			self.route = [x for x in route]

	def __str__(self):
		return ("{ size: %d, value: %d, route: %s }" % (self.size, self.value, self.route))

	@property
	def value(self):
		return sum([self.route[i] * (i + 1) for i in xrange(self.size)])

	def swap(self, x, y):
		self.route[x],self.route[y] = self.route[y],self.route[x]
		return self

	def invert(self, x, y):
		self.route[x], self.route[y] = self.route[y], self.route[x]
		for i in xrange(1, (y - x) // 2 + 1):
			self.route[x + i], self.route[y - i] = self.route[y - i], self.route[x + i]
		return self

	def rand(self, other):
		for i in xrange(self.size):
			de = randint(self.size)
			self.route[i], self.route[de] = self.route[de], self.route[i]
