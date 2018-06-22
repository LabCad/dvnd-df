# -*- coding: utf-8 -*-
import sys
import os
import unittest
import ctypes
# import numpy
from wraper_wamca2016 import merge_solutions, get_file_name, wamca_solution_instance_file, \
	apply_moves_tuple, from_list_to_tuple, get_no_conflict, no_conflict


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

		merged_sols = merge_solutions(sols)[0]
		self.assertEquals(2, len(merged_sols), "Tamanho incorreto")
		for i in xrange(len(merged_sols)):
			self.assertEquals(merged_sols[i], sols[i], "Solução {} diferente do esperado".format(i))
			self.assertEquals(0, len(merged_sols[i].movtuple[0]), "Solução {} Quantidade de movimentos restantes".format(i))

	def test_merge_solutions_no_moves(self):
		tam = 5
		sol0 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10, ([], [], [], []))
		sol1 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10, ([], [], [], []))
		sols = [sol0, sol1]

		merged_sols = merge_solutions(sols)[0]
		self.assertEquals(2, len(merged_sols), "Tamanho incorreto")
		for i in xrange(len(merged_sols)):
			self.assertEquals(merged_sols[i], sols[i], "Solução {} diferente do esperado".format(i))
			self.assertEquals(0, len(merged_sols[i].movtuple[0]), "Solução {} Quantidade de movimentos restantes".format(i))

	def test_merge_solutions_one_move(self):
		solution_index = 0
		sol_info = wamca_solution_instance_file[solution_index]
		tam = sol_info[1]
		file_name = get_file_name(solution_index)

		sol0 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10, ([0], [1], [2], [2]))
		sol1 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10, ([0], [1], [2], [2]))
		sols = [sol0, sol1]

		merged_sols = merge_solutions(sols, file_name)[0]
		self.assertEquals(2, len(merged_sols), "Tamanho incorreto")
		for i in xrange(len(merged_sols)):
			sols[i].vector[1], sols[i].vector[2] = sols[i].vector[2], sols[i].vector[1]
			self.assertTrue((merged_sols[i].vector == sols[i].vector).all(), "Solução {} diferente do esperado".format(i))
			self.assertEquals(0, len(merged_sols[i].movtuple[0]), "Solução {} Quantidade de movimentos restantes".format(i))

		sol1.movtuple = [1], [1], [2], [2]

		merged_sols = merge_solutions(sols, file_name)[0]
		self.assertEquals(2, len(merged_sols), "Tamanho incorreto")
		for i in xrange(len(merged_sols)):
			self.assertEquals(1, len(merged_sols[i].movtuple[0]), "Solução {} Quantidade de movimentos restantes".format(i))

		sol1.movtuple = [1, 0], [1, 1], [2, 2], [2, 2]
		merged_sols = merge_solutions(sols, file_name)[0]
		self.assertEquals(0, len(merged_sols[0].movtuple[0]), "Solução {} Quantidade de movimentos restantes".format(0))
		self.assertEquals(1, len(merged_sols[1].movtuple[0]), "Solução {} Quantidade de movimentos restantes".format(1))

		sol0.movtuple = [1, 2, 3, 0], [3, 4, 1, 1], [4, 5, 2, 2], [7, 9, 2, 2]
		merged_sols = merge_solutions(sols, file_name)[0]
		self.assertEquals(3, len(merged_sols[0].movtuple[0]), "Solução {} Quantidade de movimentos restantes".format(0))
		self.assertEquals(1, len(merged_sols[1].movtuple[0]), "Solução {} Quantidade de movimentos restantes".format(1))

	def test_apply_moves(self):
		# apply_moves(file="", solint=[], cids=None, ciis=None, cjjs=None, ccosts=None):
		solution_index = 0
		sol_info = wamca_solution_instance_file[solution_index]
		tam = sol_info[1]
		sol_vector = numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int)
		sol_vector_copy = numpy.copy(sol_vector)
		file_name = get_file_name(solution_index)
		apply_moves_tuple(file_name, sol_vector, from_list_to_tuple([], [], [], []))

		self.assertTrue((sol_vector_copy == sol_vector).all(), "Todos iguais quando não há movimento")

		# Swap
		apply_moves_tuple(file_name, sol_vector, from_list_to_tuple([0], [1], [2], [0]))
		sol_vector_copy[2], sol_vector_copy[1] = sol_vector_copy[1], sol_vector_copy[2]
		self.assertTrue((sol_vector_copy == sol_vector).all(), "Swap 1-2")

		sol_vector = numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int)
		sol_vector_copy = numpy.copy(sol_vector)
		apply_moves_tuple(file_name, sol_vector, from_list_to_tuple([0, 0], [4, 2], [5, 3], [0, 0]))
		sol_vector_copy[4], sol_vector_copy[5] = sol_vector_copy[5], sol_vector_copy[4]
		sol_vector_copy[2], sol_vector_copy[3] = sol_vector_copy[3], sol_vector_copy[2]
		self.assertTrue((sol_vector_copy == sol_vector).all(), "Swap 4-5, Swap 2-3")

	def test_merge_SolutionMovementTuple(self):
		solution_index = 0
		sol_info = wamca_solution_instance_file[solution_index]
		tam = sol_info[1]
		file_name = get_file_name(solution_index)

		# No moves
		sol0 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10,
			from_list_to_tuple([], [], [], []))
		sol1 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10,
			from_list_to_tuple([], [], [], []))
		bkp_vector = numpy.copy(sol0.vector)

		quest = [sol0, sol1]
		resp = merge_solutions(quest, file_name)
		self.assertEqual(len(quest), len(resp[0]), "Mesma quantidade de soluções")
		self.assertTrue((resp[0][0].vector == resp[0][1].vector).all(), "Solution 0 equals to solution 1")
		self.assertTrue((resp[0][0].vector == bkp_vector).all(), "Solution 0 is as expected")

		# Swap 4-5, Swap 2-3
		sol0 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10,
			from_list_to_tuple([0], [4], [5], [0]))
		sol1 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10,
			from_list_to_tuple([0], [4], [5], [0]))
		bkp_vector = numpy.copy(sol0.vector)

		quest = [sol0, sol1]
		resp = merge_solutions(quest, file_name)
		self.assertEqual(len(quest), len(resp[0]), "Mesma quantidade de soluções")
		self.assertEqual(1, len(resp[1]), "Mesma quantidade de movimentos")
		self.assertEqual(0, len(resp[0][0].movtuple[0]), "Solution 0 - all moviments are equal")
		self.assertEqual(0, len(resp[0][1].movtuple[0]), "Solution 1 - all moviments are equal")
		self.assertTrue((resp[0][0].vector == resp[0][1].vector).all(), "Solution 0 equals to solution 1")
		bkp_vector[4], bkp_vector[5] = bkp_vector[5], bkp_vector[4]
		self.assertTrue((resp[0][0].vector == bkp_vector).all(), "Solution 0 is as expected")

		# Swap 4-5, Swap 2-3
		sol0 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10,
			from_list_to_tuple([0, 0], [4, 2], [5, 3], [0, 0]))
		sol1 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10,
			from_list_to_tuple([0, 0], [4, 2], [5, 3], [0, 0]))
		bkp_vector = numpy.copy(sol0.vector)
		quest = [sol0, sol1]
		resp = merge_solutions(quest, file_name)
		self.assertEqual(len(quest), len(resp[0]), "Mesma quantidade de soluções")
		self.assertEqual(2, len(resp[1]), "Mesma quantidade de movimentos")
		self.assertEqual(0, len(resp[0][0].movtuple[0]), "Solution 0 - all moviments are equal")
		self.assertEqual(0, len(resp[0][1].movtuple[0]), "Solution 1 - all moviments are equal")
		self.assertTrue((resp[0][0].vector == resp[0][1].vector).all(), "Solution 0 equals to solution 1")
		bkp_vector[4], bkp_vector[5] = bkp_vector[5], bkp_vector[4]
		bkp_vector[2], bkp_vector[3] = bkp_vector[3], bkp_vector[2]
		self.assertTrue((resp[0][0].vector == bkp_vector).all(), "Solution 0 is as expected")

		# Sol0 has more moves
		sol0 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10,
			from_list_to_tuple([0, 0, 0], [6, 2, 4], [7, 3, 5], [0, 0, 0]))
		sol1 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10,
			from_list_to_tuple([0, 0], [6, 2], [7, 3], [0, 0]))
		bkp_vector = numpy.copy(sol0.vector)
		quest = [sol0, sol1]
		resp = merge_solutions(quest, file_name)
		self.assertEqual(len(quest), len(resp[0]), "Mesma quantidade de soluções")
		self.assertEqual(2, len(resp[1]), "Mesma quantidade de movimentos")
		self.assertEqual(1, len(resp[0][0].movtuple[0]), "Solution 0 - all moviments are equal")
		self.assertEqual(0, len(resp[0][1].movtuple[0]), "Solution 1 - all moviments are equal")
		self.assertTrue((resp[0][0].vector == resp[0][1].vector).all(), "Solution 0 equals to solution 1")
		bkp_vector[6], bkp_vector[7] = bkp_vector[7], bkp_vector[6]
		bkp_vector[2], bkp_vector[3] = bkp_vector[3], bkp_vector[2]
		self.assertTrue((resp[0][0].vector == bkp_vector).all(), "Solution 0 is as expected")

		# Two common moviments
		sol0 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10,
			from_list_to_tuple([0, 0, 0], [8, 2, 4], [9, 3, 5], [0, 0, 0]))
		sol1 = SolutionMovementTuple(numpy.array([x for x in xrange(tam)], dtype=ctypes.c_int), 10,
			from_list_to_tuple([0, 0, 0], [8, 6, 2], [9, 7, 3], [0, 0, 0]))
		bkp_vector = numpy.copy(sol0.vector)
		quest = [sol0, sol1]
		resp = merge_solutions(quest, file_name)
		self.assertEqual(len(quest), len(resp[0]), "Mesma quantidade de soluções")
		self.assertEqual(2, len(resp[1]), "Mesma quantidade de movimentos")
		self.assertEqual(1, len(resp[0][0].movtuple[0]), "Solution 0 - all moviments are equal")
		self.assertEqual(1, len(resp[0][1].movtuple[0]), "Solution 1 - all moviments are equal")
		self.assertTrue((resp[0][0].vector == resp[0][1].vector).all(), "Solution 0 equals to solution 1")
		bkp_vector[8], bkp_vector[9] = bkp_vector[9], bkp_vector[8]
		bkp_vector[2], bkp_vector[3] = bkp_vector[3], bkp_vector[2]
		self.assertTrue((resp[0][0].vector == bkp_vector).all(), "Solution 0 is as expected")

	def test_no_conflict(self):
		# Swap x Swap
		self.assertTrue(no_conflict(0, 4, 5, 0, 7, 8), "(0, 4, 5), (0, 7, 8) Sem conflito")
		self.assertFalse(no_conflict(0, 8, 5, 0, 7, 8), "(0, 8, 5), (0, 7, 8) conflito")
		self.assertFalse(no_conflict(0, 8, 5, 0, 1, 8), "(0, 8, 5), (0, 1, 8) conflito")

		# Swap x 2-opt
		self.assertTrue(no_conflict(0, 4, 5, 1, 7, 8), "(0, 4, 5), (1, 7, 8) Sem conflito")
		self.assertTrue(no_conflict(0, 8, 5, 1, 7, 8), "(0, 8, 5), (1, 7, 8) Sem conflito")
		self.assertFalse(no_conflict(0, 8, 5, 1, 1, 8), "(0, 8, 5), (1, 1, 8) conflito")

		# Swap x oropt-1
		self.assertTrue(no_conflict(0, 4, 5, 2, 7, 8), "(0, 4, 5), (2, 7, 8) Sem conflito")
		self.assertTrue(no_conflict(0, 8, 5, 2, 7, 8), "(0, 8, 5), (2, 7, 8) Sem conflito")
		self.assertFalse(no_conflict(0, 8, 5, 2, 1, 8), "(0, 8, 5), (2, 1, 8) conflito")

		# Swap x oropt-2
		self.assertTrue(no_conflict(0, 4, 5, 3, 7, 8), "(0, 4, 5), (3, 7, 8) Sem conflito")
		self.assertTrue(no_conflict(0, 8, 5, 3, 7, 8), "(0, 8, 5), (3, 7, 8) Sem conflito")
		self.assertFalse(no_conflict(0, 8, 5, 3, 1, 8), "(0, 8, 5), (3, 1, 8) conflito")

		# Swap x oropt-3
		self.assertTrue(no_conflict(0, 4, 5, 4, 7, 8), "(0, 4, 5), (4, 7, 8) Sem conflito")
		self.assertTrue(no_conflict(0, 8, 5, 4, 7, 8), "(0, 8, 5), (4, 7, 8) Sem conflito")
		self.assertFalse(no_conflict(0, 8, 5, 4, 1, 8), "(0, 8, 5), (4, 1, 8) conflito")

	def test_get_no_conflict(self):
		movimentos = from_list_to_tuple([0, 0], [4, 7], [5, 8], [-10, -20])
		resp_movimentos = get_no_conflict(movimentos[0], movimentos[1], movimentos[2], movimentos[3])

		self.assertEqual(2, len(resp_movimentos[0]), "Quantidade de movimentos independentes")
		self.assertEqual(-30, sum(resp_movimentos[3]), "Soma dos movimentos independentes")
		for x in xrange(len(resp_movimentos[0])):
			self.assertEqual(movimentos[0][x], resp_movimentos[0][x], "Tipo do movimento igual")
			self.assertEqual(movimentos[1][x], resp_movimentos[1][x], "Coordenada i igual")
			self.assertEqual(movimentos[2][x], resp_movimentos[2][x], "Coordenada j igual")
			self.assertEqual(movimentos[3][x], resp_movimentos[3][x], "Custo igual")

		movimentos = from_list_to_tuple([0, 0, 0], [4, 7, 8], [5, 8, 5], [-10, -20, -1])
		resp_movimentos = get_no_conflict(movimentos[0], movimentos[1], movimentos[2], movimentos[3])
		self.assertEqual(2, len(resp_movimentos[0]), "Quantidade de movimentos independentes")
		self.assertEqual(-30, sum(resp_movimentos[3]), "Soma dos movimentos independentes")
		for x in xrange(len(resp_movimentos[0])):
			self.assertEqual(movimentos[0][x], resp_movimentos[0][x], "Tipo do movimento igual")
			self.assertEqual(movimentos[1][x], resp_movimentos[1][x], "Coordenada i igual")
			self.assertEqual(movimentos[2][x], resp_movimentos[2][x], "Coordenada j igual")
			self.assertEqual(movimentos[3][x], resp_movimentos[3][x], "Custo igual")

		movimentos = from_list_to_tuple([0, 0, 0], [4, 7, 8], [5, 8, 5], [-30, -20, -40])
		resp_movimentos = get_no_conflict(movimentos[0], movimentos[1], movimentos[2], movimentos[3], False, 10)
		self.assertEqual(2, len(resp_movimentos[0]), "Quantidade de movimentos independentes")
		self.assertEqual(-50, sum(resp_movimentos[3]), "Soma dos movimentos independentes")
		for x in xrange(len(resp_movimentos[0])):
			self.assertEqual(movimentos[0][x], resp_movimentos[0][x], "Tipo do movimento igual")
			self.assertEqual(movimentos[1][x], resp_movimentos[1][x], "Coordenada i igual")
			self.assertEqual(movimentos[2][x], resp_movimentos[2][x], "Coordenada j igual")
			self.assertEqual(movimentos[3][x], resp_movimentos[3][x], "Custo igual")

		multi_size = 100000
		movimentos = from_list_to_tuple([0, 0, 0] * multi_size, [4, 7, 8] * multi_size,
			[5, 8, 5] * multi_size, [-30, -20, -40] * multi_size)
		resp_movimentos = get_no_conflict(movimentos[0], movimentos[1], movimentos[2], movimentos[3], False, 10)
		sum_values = sum(resp_movimentos[3])
		self.assertIn(sum_values, [-40, -50], "Um dos possíveis valores")
