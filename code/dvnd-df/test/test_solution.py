# -*- coding: utf-8 -*-
import sys, os
import unittest

if os.environ.has_key('DVND_HOME'):
	sys.path.append(os.environ['DVND_HOME'])

from solution import *


class SolutionTest(unittest.TestCase):
	def test_create(self):
		tam = 5
		sol = Solution(tam)
		self.assertEquals(tam, len(sol), "Tamanho incorreto")
		self.assertEquals([i for i in xrange(tam)], sol.route, "Solução inicial diferente do esperado")

	def test_value(self):
		tam = 5
		sol = Solution(tam)
		valor = 0
		for i in xrange(tam):
			valor += i * (i + 1)
		self.assertEquals(valor, sol.value, "Valor calculado errado")

	def test_swap(self):
		sol = Solution(5)
		self.assertEquals([1, 0, 2, 3, 4], sol.swap(0, 1).route, "Swap não coincide")

	def test_invert(self):
		sol = Solution(5)
		sol.invert(0, 3)
		esperado = [3, 2, 1, 0, 4]
		self.assertEquals(esperado, sol.route, ("Invert não coincide %s - %s" % (esperado, sol.route)))
