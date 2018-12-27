# -*- coding: utf-8 -*-
import sys
import os
import unittest

if os.environ.has_key('DVND_HOME'):
	sys.path.append(os.environ['DVND_HOME'])

if os.path.abspath(".").endswith("test"):
	from movement import *
else:
	from src.movement import *


class MovementTest(unittest.TestCase):
	def test_create(self):
		mov = Movement(MovementType.SWAP, 0, 1)

		self.assertEquals(MovementType.SWAP, mov.movtype, "Tipo do movimento")
		self.assertEquals(0, mov.x, "Inicio do movimento")
		self.assertEquals(1, mov.y, "Fim do movimento")
		self.assertIsNone(mov.k, "k não preenchido")

	def test_conflict(self):
		mov1 = Movement(MovementType.SWAP, 0, 1)
		mov2 = Movement(MovementType.SWAP, 3, 4)
		self.assertFalse(mov1.conflict(mov2), "swap(0,1) não conflita com swap(2,3)")

		mov3 = Movement(MovementType.SWAP, 1, 3)
		self.assertTrue(mov1.conflict(mov3), "swap(0,1) conflita com swap(1,3)")
