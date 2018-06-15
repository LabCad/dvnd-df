# -*- coding: utf-8 -*-
import sys
import os
import unittest
import ctypes
import numpy


if os.environ.has_key('DVND_HOME'):
	sys.path.append(os.environ['DVND_HOME'])

from solution import *


class SolutionVectorValueTest(unittest.TestCase):
	def test_create(self):
		tam = 5
		sol = SolutionVectorValue([x for x in xrange(tam)], 10)
		self.assertEquals(tam, len(sol), "Tamanho incorreto")
		self.assertEquals([i for i in xrange(tam)], sol.vector, "Solução inicial diferente do esperado")

		sol = SolutionVectorValue(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 100)
		self.assertEquals(tam, len(sol), "Tamanho incorreto")
		self.assertTrue((numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int) == sol.vector).all(), "Solução inicial diferente do esperado")


class SolutionMovementTupleTest(unittest.TestCase):
	def test_create(self):
		tam = 5
		sol = SolutionMovementTuple([x for x in xrange(tam)], 10, ([], [], [], []))
		self.assertEquals(tam, len(sol), "Tamanho incorreto")
		self.assertEquals([i for i in xrange(tam)], sol.vector, "Solução inicial diferente do esperado")

		sol = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 100)
		self.assertEquals(tam, len(sol), "Tamanho incorreto")
		self.assertTrue((numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int) == sol.vector).all(), "Solução inicial diferente do esperado")

	def test_can_merge(self):
		tam = 5
		sol = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 100, ([], [], [], []))
		sol2 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 100, ([], [], [], []))

		self.assertTrue(sol.can_merge(sol2), "Can Merge mesma solução")

		sol2.vector[0], sol2.vector[1] = sol2.vector[1], sol2.vector[0]
		self.assertFalse(sol.can_merge(sol2), "Can Merge Mudou vetor")

		sol2.value = 15
		self.assertFalse(sol.can_merge(sol2), "Can Merge Mudou valor")
