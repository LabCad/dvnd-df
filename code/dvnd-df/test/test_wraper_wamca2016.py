# -*- coding: utf-8 -*-
import sys
import os
import unittest
import ctypes
import numpy
from wraper_wamca2016 import merge_solutions


if os.environ.has_key('DVND_HOME'):
	sys.path.append(os.environ['DVND_HOME'])

from solution import *


class WraperWamca2016Test(unittest.TestCase):
	def test_merge_solutions(self):
		tam = 5
		sol = SolutionMovementTuple([x for x in xrange(tam)], 10, ([], [], [], []))
		sol2 = SolutionMovementTuple([x for x in xrange(tam)], 10, ([], [], [], []))

		merged_sols = merge_solutions([sol, sol2])
		self.assertEquals(2, len(merged_sols), "Tamanho incorreto")
		# self.assertEquals([i for i in xrange(tam)], sol.vector, "Solução inicial diferente do esperado")
		#
		# sol = SolutionVectorValue(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 100)
		# self.assertEquals(tam, len(sol), "Tamanho incorreto")
		# self.assertTrue((numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int) == sol.vector).all(), "Solução inicial diferente do esperado")
