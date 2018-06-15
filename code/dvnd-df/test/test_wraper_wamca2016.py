# -*- coding: utf-8 -*-
import sys
import os
import unittest
import ctypes
# import numpy
from wraper_wamca2016 import merge_solutions


if os.environ.has_key('DVND_HOME'):
	sys.path.append(os.environ['DVND_HOME'])

from solution import *


class WraperWamca2016Test(unittest.TestCase):
	def test_merge_distinct_solutions(self):
		tam = 5
		sol0 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10, ([], [], [], []))
		sol1 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10, ([], [], [], []))
		sol1.vector[0], sol1.vector[1] = sol1.vector[1], sol1.vector[0]
		sols = [sol0, sol1]

		merged_sols = merge_solutions(sols)
		self.assertEquals(2, len(merged_sols), "Tamanho incorreto")
		for i in xrange(len(merged_sols)):
			self.assertEquals(merged_sols[i], sols[i], "Solução {} diferente do esperado".format(i))
			self.assertEquals(0, len(merged_sols[i].movtuple[0]), "Solução {} Quantidade de movimentos restantes".format(i))

	def test_merge_solutions_no_moves(self):
		tam = 5
		sol0 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10, ([], [], [], []))
		sol1 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10, ([], [], [], []))
		sols = [sol0, sol1]

		merged_sols = merge_solutions(sols)
		self.assertEquals(2, len(merged_sols), "Tamanho incorreto")
		for i in xrange(len(merged_sols)):
			self.assertEquals(merged_sols[i], sols[i], "Solução {} diferente do esperado".format(i))
			self.assertEquals(0, len(merged_sols[i].movtuple[0]), "Solução {} Quantidade de movimentos restantes".format(i))

	def test_merge_solutions_one_move(self):
		tam = 5
		sol0 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10, ([0], [0], [1], [2]))
		sol1 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10, ([0], [0], [1], [2]))
		sols = [sol0, sol1]

		merged_sols = merge_solutions(sols)
		self.assertEquals(2, len(merged_sols), "Tamanho incorreto")
		for i in xrange(len(merged_sols)):
			self.assertEquals(merged_sols[i], sols[i], "Solução {} diferente do esperado".format(i))
			self.assertEquals(0, len(merged_sols[i].movtuple[0]), "Solução {} Quantidade de movimentos restantes".format(i))

		sol1.movtuple = [1], [0], [1], [2]

		merged_sols = merge_solutions(sols)
		self.assertEquals(2, len(merged_sols), "Tamanho incorreto")
		for i in xrange(len(merged_sols)):
			self.assertEquals(merged_sols[i], sols[i], "Solução {} diferente do esperado".format(i))
			self.assertEquals(1, len(merged_sols[i].movtuple[0]), "Solução {} Quantidade de movimentos restantes".format(i))

		sol1.movtuple = [1, 0], [0, 0], [1, 1], [2, 2]
		merged_sols = merge_solutions(sols)
		self.assertEquals(0, len(merged_sols[0].movtuple[0]), "Solução {} Quantidade de movimentos restantes".format(0))
		self.assertEquals(1, len(merged_sols[1].movtuple[0]), "Solução {} Quantidade de movimentos restantes".format(1))

		sol0.movtuple = [1, 2, 3, 0], [3, 4, 0, 0], [4, 5, 1, 1], [7, 9, 2, 2]
		merged_sols = merge_solutions(sols)
		self.assertEquals(3, len(merged_sols[0].movtuple[0]), "Solução {} Quantidade de movimentos restantes".format(0))
		self.assertEquals(1, len(merged_sols[1].movtuple[0]), "Solução {} Quantidade de movimentos restantes".format(1))