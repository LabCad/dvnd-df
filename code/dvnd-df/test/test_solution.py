# -*- coding: utf-8 -*-
import sys
import os
import unittest

if 'DVND_HOME' in os.environ:
	sys.path.append(os.environ['DVND_HOME'])

# from solution import *


# class SolutionTest(unittest.TestCase):
# 	def test_create(self):
# 		tam = 5
# 		sol = Solution(tam)
# 		self.assertEquals(tam, len(sol), "Tamanho incorreto")
# 		self.assertEquals([i for i in xrange(tam)], sol.get_route, "Solução inicial diferente do esperado")
#
# 	def test_value(self):
# 		tam = 5
# 		sol = Solution(tam)
# 		valor = 0
# 		for i in xrange(tam):
# 			valor += i * (i + 1)
# 		self.assertEquals(valor, sol.value, "Valor calculado errado")
#
# 	def test_swap(self):
# 		sol = Solution(5)
# 		self.assertEquals([1, 0, 2, 3, 4], sol.swap(0, 1).get_route, "Swap não coincide")
#
# 		sol = Solution(10, [0, 4, 6, 1, 9, 7, 3, 2, 8, 5])
# 		self.assertEquals([0, 7, 6, 1, 9, 4, 3, 2, 8, 5], sol.swap(1, 5).get_route, "swap(1,5) não coincide")
#
# 		sol = Solution(10)
# 		self.assertEquals([0, 5, 2, 3, 4, 1, 6, 7, 8, 9], sol.swap(1, 5).get_route, "swap(1,5) não coincide")
#
# 	def test_2_opt(self):
# 		sol = Solution(10, [0, 4, 6, 1, 9, 7, 3, 2, 8, 5])
# 		self.assertEquals([0, 7, 9, 1, 6, 4, 3, 2, 8, 5], sol.two_opt(1, 5).get_route, "2-opt(1,5) não coincide")
#
# 		sol = Solution(10)
# 		self.assertEquals([0, 5, 4, 3, 2, 1, 6, 7, 8, 9], sol.two_opt(1, 5).get_route, "2-opt(1,5) não coincide")
#
# 	def test_oropt_2t(self):
# 		sol = Solution(10, [0, 4, 6, 1, 9, 7, 3, 2, 8, 5])
# 		self.assertEquals([0, 1, 9, 7, 3, 4, 6, 2, 8, 5], sol.oropt_k(1, 5, 2).get_route, "oropt-2(1,5) não coincide")
#
# 		sol = Solution(10)
# 		self.assertEquals([0, 3, 4, 5, 6, 1, 2, 7, 8, 9], sol.oropt_k(1, 5, 2).get_route, "oropt-2(1,5) não coincide")
#
# 		sol = Solution(10)
# 		self.assertEquals([0, 2, 3, 4, 5, 6, 7, 8, 9, 1], sol.oropt_k(1, 9, 1).get_route, "oropt-1(1,9) não coincide")
#
# 		sol = Solution(10)
# 		self.assertEquals([0, 2, 3, 4, 5, 6, 7, 8, 1, 9], sol.oropt_k(1, 8, 1).get_route, "oropt-1(1,8) não coincide")
#
# 	def test_invert(self):
# 		sol = Solution(5)
# 		sol.invert(0, 3)
# 		esperado = [3, 2, 1, 0, 4]
# 		self.assertEquals(esperado, sol.get_route, ("Invert não coincide %s - %s" % (esperado, sol.get_route)))
