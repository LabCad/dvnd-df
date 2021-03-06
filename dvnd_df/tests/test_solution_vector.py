# -*- coding: utf-8 -*-
import sys
import os
import unittest
import ctypes
from dvnd_df.wrapper.solution import *


if 'DVND_HOME' in os.environ:
	sys.path.append(os.environ['DVND_HOME'])

# if os.path.abspath(".").endswith("test"):
# 	from wrapper.solution import *
# else:
# 	from wrapper.solution import *


class SolutionVectorValueTest(unittest.TestCase):
	def test_create(self):
		tam = 5
		sol = SolutionVectorValue(numpy.arange(0, tam, dtype=ctypes.c_int), 100)
		self.assertEquals(tam, len(sol), "Tamanho incorreto")
		self.assertTrue((numpy.arange(0, tam, dtype=ctypes.c_int) == sol.vector).all(),
			"Solução inicial diferente do esperado")


class SolutionMovementTupleTest(unittest.TestCase):
	def test_create(self):
		tam = 5
		sol = SolutionMovementTuple(numpy.arange(0, tam, dtype=ctypes.c_int), 100, ([], [], [], []))
		self.assertEquals(tam, len(sol), "Tamanho incorreto")
		self.assertTrue((numpy.arange(0, tam, dtype=ctypes.c_int) == sol.vector).all(),
			"Solução inicial diferente do esperado")

	def test_can_merge(self):
		tam = 5
		sol = SolutionMovementTuple(numpy.arange(0, tam, dtype=ctypes.c_int), 100, ([], [], [], []))
		sol2 = SolutionMovementTuple(numpy.arange(0, tam, dtype=ctypes.c_int), 100, ([], [], [], []))

		self.assertTrue(sol.can_merge(sol2), "Can Merge mesma solução")

		sol2.vector[0], sol2.vector[1] = sol2.vector[1], sol2.vector[0]
		self.assertFalse(sol.can_merge(sol2), "Can Merge Mudou vetor")

		sol2.value = 15
		self.assertFalse(sol.can_merge(sol2), "Can Merge Mudou valor")
