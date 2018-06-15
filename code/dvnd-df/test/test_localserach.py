# -*- coding: utf-8 -*-
import sys
import os
import unittest

if os.environ.has_key('DVND_HOME'):
	sys.path.append(os.environ['DVND_HOME'])

from localsearch import *


# class LocalSearchTest(unittest.TestCase):
# 	def test_bestImprovement(self):
# 		s = Solution(10)
# 		self.assertEquals(330, s.value, "Valor inicial")
# 		self.assertEquals(285, bestImprovement(s, lambda sol, x, y: sol.swap(x, y), lambda sol, x, y: sol.swap(x, y), False)[0].value, "BestImprovement Swap")
# 		self.assertEquals(235, bestImprovement(s, lambda sol, x, y: sol.invert(x, y), lambda sol, x, y: sol.invert(x, y), False)[0].value, "BestImprovement Invert")
