# -*- coding: utf-8 -*-
import sys
import os
import unittest

if os.environ.has_key('DVND_HOME'):
	sys.path.append(os.environ['DVND_HOME'])

from solution import *
from movement import *
from solution_movement import *


class SolutionMovementAccept(unittest.TestCase):
	def test_accept_swap(self):
		tam = 5
		sol = Solution(tam)
		mov = Movement(MovementType.SWAP, 0, 1)
		sol.accept(mov)
		esperado = Solution(tam, [1, 0, 2, 3, 4])
		self.assertEquals(esperado, sol, "%s - %s - %s" % (mov, esperado, sol))
		sol.accept(mov)

		mov = Movement(MovementType.SWAP, 1, 2)
		sol.accept(mov)
		esperado = Solution(tam, [0, 2, 1, 3, 4])
		self.assertEquals(esperado, sol, "%s - %s - %s" % (mov, esperado, sol))
		sol.accept(mov)

		mov = Movement(MovementType.SWAP, 1, 4)
		sol.accept(mov)
		esperado = Solution(tam, [0, 4, 2, 3, 1])
		self.assertEquals(esperado, sol, "%s - %s - %s" % (mov, esperado, sol))
		sol.accept(mov)

	def test_accept_two_opt(self):
		tam = 10
		sol = Solution(tam)
		mov = Movement(MovementType.TWO_OPT, 2, 7)
		sol.accept(mov)
		esperado = Solution(tam, [0, 1, 7, 6, 5, 4, 3, 2, 8, 9])
		self.assertEquals(esperado, sol, "%s - %s - %s" % (mov, esperado, sol))
		sol.accept(mov)

		mov = Movement(MovementType.TWO_OPT, 0, 3)
		sol.accept(mov)
		esperado = Solution(tam, [3, 2, 1, 0, 4, 5, 6, 7, 8, 9])
		self.assertEquals(esperado, sol, "%s - %s - %s" % (mov, esperado, sol))
		sol.accept(mov)


class SolutionMovementTest(unittest.TestCase):
	def test_create(self):
		tam = 5
		sol = Solution(tam)
		mov = Movement(MovementType.SWAP, 0, 1)
		solmov = SolutionMovement(sol, mov, 30)
		self.assertEquals(sol, solmov.sol, "SolutionMovement - Solução")
		self.assertEquals(mov, solmov.mov, "SolutionMovement - Movimento")
		self.assertEquals(30, solmov.imp, "SolutionMovement - Melhoria")

	def test_canMerge(self):
		tam = 5
		sol = Solution(tam)
		solmov1 = SolutionMovement(sol, Movement(MovementType.SWAP, 0, 1), 30)
		solmov2 = SolutionMovement(sol, Movement(MovementType.SWAP, 3, 4), 40)
		self.assertTrue(solmov1.can_merge(solmov2), "swap(0,1) e swap(3,4) não tem conflito")
		solmov3 = SolutionMovement(sol, Movement(MovementType.SWAP, 1, 4), 50)
		self.assertFalse(solmov1.can_merge(solmov3), "swap(0,1) e swap(1,4) tem conflito")


class SolutionMovementCollectionTest(unittest.TestCase):
	def test_create(self):
		tam = 5
		sol = Solution(tam)
		solmovs = SolutionMovementCollection(sol)
		self.assertEquals(sol.value, solmovs.value, "SolutionMovementCollection - value")

	def test_merge(self):
		tam = 5
		sol = Solution(tam)
		solmovs = SolutionMovementCollection(sol)
		solmov1 = SolutionMovement(sol, Movement(MovementType.SWAP, 0, 1), 30)
		solmov2 = SolutionMovement(sol, Movement(MovementType.SWAP, 3, 4), 40)
		solmov3 = SolutionMovement(sol, Movement(MovementType.SWAP, 1, 3), 50)

		solvalue = sol.value
		self.assertTrue(solmovs.can_merge(solmov1), "SolutionMovementCollection - canMerge")
		self.assertEquals(solvalue, solmovs.value, "SolutionMovementCollection - value")
		self.assertTrue(solmovs.can_merge(solmov2), "SolutionMovementCollection - canMerge")
		self.assertEquals(solvalue, solmovs.value, "SolutionMovementCollection - value")
		self.assertTrue(solmovs.can_merge(solmov3), "SolutionMovementCollection - canMerge")
		self.assertEquals(solvalue, solmovs.value, "SolutionMovementCollection - value")

		solmovs.merge(solmov1)
		self.assertEquals(solvalue + solmov1.imp, solmovs.value, "SolutionMovementCollection - value")
		self.assertTrue(solmovs.can_merge(solmov2), "SolutionMovementCollection - canMerge")
		self.assertFalse(solmovs.can_merge(solmov3), "SolutionMovementCollection - canMerge")

		solmovs.merge(solmov3)
		self.assertEquals(solvalue + solmov1.imp, solmovs.value, "SolutionMovementCollection - value")

		solmovs.merge(solmov2)
		self.assertEquals(solvalue + solmov1.imp + solmov2.imp, solmovs.value, "SolutionMovementCollection - value")
