#!/usr/bin/python
# -*- coding: utf-8 -*-
import ctypes
import numpy
import util
import random
import os.path
import time
# from movement import *
from solution import SolutionVectorValue, SolutionMovementTuple
from util import compilelib


wamca2016path_uff = "/home/imcoelho/Rodolfo/wamca2016/"
wamca2016path_local = "/home/rodolfo/git/wamca2016/"
wamca2016_input_file_path = "/home/rodolfo/git/dvnd-df/doc/"
localpath_uff = "/home/imcoelho/Rodolfo/dvnd-df/code/dvnd-df/src/"
localpath_local = "/home/rodolfo/git/dvnd-df/code/dvnd-df/src/"

wamca2016path = wamca2016path_uff if os.path.isdir(wamca2016path_uff) else wamca2016path_local
localpath = localpath_uff if os.path.isdir(localpath_uff) else localpath_local

print("wamca2016path: {}".format(wamca2016path))
print("localpath: {}".format(localpath))

print "WAMCAPATH:" + wamca2016path


class WamcaWraper(object):
	def __init__(self, instancefile, mylibname='wamca2016lib', options=["-lgomp"], compiler_options=["-fopenmp"],
			verbose=True, useMultipleGpu=False, deviceCount=1, libpath=wamca2016path):
		assert instancefile is not None, "The file is mandatory"
		self.__file = instancefile
		self.__use_multiple_gpu = useMultipleGpu
		self.__device_count = deviceCount

		files = [libpath + "source/*.cu", libpath + "source/*.cpp"]
		compilelib(files, localpath, mylibname, options, compiler_options, verbose)
		self.__mylib = ctypes.cdll.LoadLibrary("{}{}.so".format(localpath, mylibname))

		# unsigned int bestNeighbor(char * file, int *solution, unsigned int solutionSize, int neighborhood,
		# 	bool justCalc = false, unsigned int hostCode = 0,
		#   unsigned int *useMoves = 0, unsigned short *ids = NULL, unsigned int *is = NULL,
		#   unsigned int *js = NULL, unsigned int *costs = NULL) {
		self.__mylib.bestNeighbor.argtypes = [ctypes.c_void_p, util.array_1d_int, ctypes.c_uint, ctypes.c_int,
			ctypes.c_bool, ctypes.c_uint,
			util.array_1d_uint, util.array_1d_ushort, util.array_1d_uint,
			util.array_1d_uint, util.array_1d_int, ctypes.c_bool, ctypes.c_uint, util.array_1d_int]
		# char * file, int *solution, unsigned int solutionSize, int neighborhood, bool justCalc = false
		self.__mylib.bestNeighbor.restype = ctypes.c_uint

		# int getNoConflictMoves(unsigned int useMoves, unsigned short * ids, unsigned int * is, unsigned int * js,
		#   int * costs, int * selectedMoves, int * impValue)
		self.__mylib.getNoConflictMoves.restype = ctypes.c_int
		self.__mylib.getNoConflictMoves.argtypes = [ctypes.c_uint, util.array_1d_ushort, util.array_1d_uint,
			util.array_1d_uint, util.array_1d_int, util.array_1d_int,
			util.array_1d_int, ctypes.c_bool]
		# ctypes.POINTER(c_int)

		# unsigned int applyMoves(char * file, int * solution, unsigned int solutionSize, unsigned int useMoves = 0,
		#   unsigned short * ids = NULL, unsigned int * is = NULL, unsigned int * js = NULL, int * costs = NULL)
		self.__mylib.applyMoves.restype = ctypes.c_uint
		self.__mylib.applyMoves.argtypes = [ctypes.c_void_p, util.array_1d_int, ctypes.c_uint, ctypes.c_uint,
			util.array_1d_ushort, util.array_1d_uint, util.array_1d_uint, util.array_1d_int]

		self.__mylib.noConflict.restype = ctypes.c_bool
		self.__mylib.noConflict.argtypes = [ctypes.c_ushort, ctypes.c_uint, ctypes.c_uint,
			ctypes.c_ushort, ctypes.c_uint, ctypes.c_uint]

		# extern "C" unsigned int bestNeighborSimple(char * file, int *solution, unsigned int solutionSize,
		# int neighborhood)
		self.__mylib.bestNeighborSimple.restype = ctypes.c_uint
		self.__mylib.bestNeighborSimple.argtypes = [ctypes.c_void_p, util.array_1d_int, ctypes.c_uint, ctypes.c_int]

	def __apply_moves(self, solint=[], cids=None, ciis=None, cjjs=None, ccosts=None):
		resto_time = -time.time()
		lenmovs = len(cids)
		# if lenmovs > 0:
		for i in xrange(len(cids) - 1, -1, -1):
			if cids[i] == 0 and ciis[i] == 0 and cjjs[i] == 0 and ccosts[i] == 0:
				lenmovs -= 1
			else:
				break
		for i in xrange(0, lenmovs - 1):
			if cids[i] == 0 and ciis[i] == 0 and cjjs[i] == 0 and ccosts[i] == 0:
				cids[i], ciis[i], cjjs[i], ccosts[i], \
				cids[lenmovs - 1], ciis[lenmovs - 1], cjjs[lenmovs - 1], ccosts[lenmovs - 1] = \
					cids[lenmovs - 1], ciis[lenmovs - 1], cjjs[lenmovs - 1], ccosts[lenmovs - 1], \
					cids[i], ciis[i], cjjs[i], ccosts[i]
				lenmovs -= 1
			# print "{}-{}".format(i, aa)
			if i >= lenmovs - 1:
				break
		lenmovs = len(cids)
		for i in xrange(len(cids) - 1, -1, -1):
			if cids[i] == 0 and ciis[i] == 0 and cjjs[i] == 0 and ccosts[i] == 0:
				lenmovs -= 1
			else:
				break
		resto_time += time.time()
		call_time = -time.time()
		moves = self.__mylib.applyMoves(self.__file, solint, len(solint), lenmovs, cids, ciis, cjjs, ccosts)
		call_time += time.time()
		# print("resto_time;%.5f;call_time;;%.5f;" % (resto_time, call_time))
		return moves

	def __apply_moves_tuple(self, solint=[], tupple=None):
		return self.__apply_moves(solint, tupple[0], tupple[1], tupple[2], tupple[3])

	def apply_moves(self, solution=None):
		if not solution.movapplied and len(solution.movtuple[0]) > 0:
			cop_time = -time.time()
			numpy.copyto(solution.movvector, solution.vector)
			cop_time += time.time()
			ap_time = -time.time()
			solution.value = self.__apply_moves_tuple(solution.movvector, solution.movtuple)
			ap_time += time.time()
			solution.movapplied = True
			# TODO remove debug time
			# print("cop_time;%.5f;ap_time;%.5f;" % (cop_time, ap_time))
			# solution.vector, solution.movvector = solution.movvector, solution.vector

	def __best_neighbor(self, solint=[], neighborhood=0, justcalc=False):
		# self.__mylib.bestNeighborSimple.argtypes = [ctypes.c_void_p, util.array_1d_int, ctypes.c_uint, ctypes.c_int]
		return self.__best_neighbor_moves(solint, neighborhood, 0, justcalc, numpy.array([], dtype=ctypes.c_int))

	def __best_neighbor_moves(self, solint=[], neighborhood=0, n_moves=0, justcalc=False, solintResp=None):
		carrays = from_list_to_tuple([0 for x in xrange(n_moves)], [0 for x in xrange(n_moves)],
			[0 for x in xrange(n_moves)], [0 for x in xrange(n_moves)])
		n_moves_array = numpy.array([n_moves], dtype=ctypes.c_uint)

		# mpi_call_time = 0
		# hostcode = 0 if not self.__use_multiple_gpu else neighborhood
		hostcode = 0
		if self.__use_multiple_gpu:
			from mpi4py import MPI
			comm = MPI.COMM_WORLD
			hostcode = comm.rank

		resp = self.__mylib.bestNeighbor(self.__file, solint, len(solint), neighborhood, justcalc, hostcode,# 0,#gethostcode(),
			n_moves_array, carrays[0], carrays[1], carrays[2], carrays[3], self.__use_multiple_gpu,
			self.__device_count, solintResp)

		carrays = [numpy.resize(x, int(n_moves_array[0])) for x in carrays]
		return solint, resp, carrays, (0, 0, 0, 0), solintResp

	def calculate_value(self, solint=[]):
		return self.__best_neighbor(solint, 1, True)[1]

	def create_initial_solution(self, solution_index=0, solver_param="", solution_instance_index=None):
		sol_info = wamca_solution_instance_file[solution_index]

		solint = numpy.arange(0, sol_info[1], dtype=ctypes.c_int)
		if solution_instance_index == -1:
			random.shuffle(solint)
		elif solution_instance_index >= 0:
			with open("{}/sol/{}_{}.in".format(wamca2016_input_file_path, sol_info[0][:-4], solution_instance_index),
					"r") as filesol:
				solint = numpy.array([int(x) for x in filesol.read()[1:-1].split(',')], dtype=ctypes.c_int)

		print "Size: {} - file name: {}".format(sol_info[1], sol_info[0])
		if "gdvnd" == solver_param:
			return SolutionMovementTuple(solint, self.calculate_value(solint), ([], [], [], []))
		else:
			return SolutionMovementTuple(solint, self.calculate_value(solint), ([], [], [], []))

	def merge_common_movs(self, solutions=None):
		if all([solutions[0].can_merge(solutions[x]) for x in xrange(1, len(solutions))]):
			intersection = set(from_tuple_to_movement_list(solutions[0].movtuple))
			for i in xrange(1, len(solutions)):
				intersection &= set(from_tuple_to_movement_list(solutions[i].movtuple))
			if len(intersection) > 0:
				new_solution_vetor = numpy.copy(solutions[0].vector)
				self.__apply_moves_tuple(new_solution_vetor, from_movement_list_to_tuple(intersection))
				new_value = self.calculate_value(new_solution_vetor)

				# Optimization for the case where all the solutions are the same
				# len(intersection) == len(solutions[0].movtuple[0])
				if all([len(intersection) == len(x.movtuple[0]) for x in solutions]) and len(set(solutions)) == 1:
					localsolution = SolutionMovementTuple(numpy.copy(new_solution_vetor), new_value,
						from_movement_list_to_tuple(list(set(from_tuple_to_movement_list(solutions[0].movtuple)) - intersection)))
					return [localsolution for sol in solutions], intersection
				else:
					return [SolutionMovementTuple(numpy.copy(new_solution_vetor), new_value,
						from_movement_list_to_tuple(list(set(from_tuple_to_movement_list(sol.movtuple)) - intersection)))
						for sol in solutions], intersection

		return solutions, None

	def neigh_gpu(self, solution=None, inimov=0):
		resp = self.__best_neighbor(solution.vector, inimov, False)

		return SolutionMovementTuple(resp[0], resp[1], ([], [], [], [])), (0, 0, 0, 0, 0)

	def neigh_gpu_moves(self, solution=None, inimov=0, n_moves=0):
		if len(solution.movtuple[0]) > 0:
			if not solution.movapplied:
				copy_sol = numpy.copy(solution.vector)
				self.__apply_moves_tuple(solution.movvector, solution.movtuple)
			else:
				copy_sol = numpy.copy(solution.movvector)
		else:
			copy_sol = numpy.copy(solution.vector)
		resp = self.__best_neighbor_moves(copy_sol, inimov, n_moves, False, numpy.copy(solution.movvector))
		meta = resp[3][0], resp[3][1], resp[3][2], resp[3][3], 0
		resp_sol = SolutionMovementTuple(resp[0], resp[1], resp[2], resp[4])
		resp_sol.movapplied = True
		return resp_sol, meta

	def no_conflict(self, id1=0, i1=0, j1=0, id2=0, i2=0, j2=0):
		return self.__mylib.noConflict(id1, i1, j1, id2, i2, j2)

	def merge_independent_movements(self, sol1, sol2):
		if sol1.can_merge(sol2):
			contat_time = -time.time()
			cids = numpy.concatenate((sol1.movtuple[0], sol2.movtuple[0]))
			ciis = numpy.concatenate((sol1.movtuple[1], sol2.movtuple[1]))
			cjjs = numpy.concatenate((sol1.movtuple[2], sol2.movtuple[2]))
			ccosts = numpy.concatenate((sol1.movtuple[3], sol2.movtuple[3]))
			contat_time += time.time()
			no_conflict_time = -time.time()
			independent_movs = self.get_no_conflict(cids, ciis, cjjs, ccosts)
			no_conflict_time += time.time()
			new_sol_time = -time.time()
			resp = SolutionMovementTuple(numpy.copy(sol1.vector), 0, independent_movs)
			new_sol_time += time.time()
			app_sol_time = -time.time()
			self.apply_moves(resp)
			app_sol_time += time.time()
			cp_sol_time = -time.time()
			numpy.copyto(resp.vector, sol1.vector)
			cp_sol_time += time.time()
			# TODO Remover contagem
			# print("contat_time;%.5lf;no_conflict_time;%.5lf;new_sol_time;%.5lf;app_sol_time;%.5lf;cp_sol_time;%.5lf;"
			# 	% (contat_time, no_conflict_time, new_sol_time, app_sol_time, cp_sol_time))
			return resp, True
		return sol1, False

	def get_no_conflict(self, cids, ciis, cjjs, ccosts, maximize=False, tentativas=2):
		impMoves = numpy.arange(0, len(cids), dtype=ctypes.c_int)
		impMovesTemp = numpy.arange(0, len(cids), dtype=ctypes.c_int)
		impValue = numpy.array([0], dtype=ctypes.c_int)
		impValueTemp = numpy.array([0], dtype=ctypes.c_int)

		nMoves = self.__mylib.getNoConflictMoves(len(cids), cids, ciis, cjjs, ccosts, impMoves, impValue, maximize)
		tentativas = min(tentativas, len(cids) - 1)
		removed_moves = set()
		for cont_tentativas in xrange(tentativas):
			random_list = list(set([x for x in xrange(nMoves)]) - removed_moves)
			if len(random_list) == 0:
				break
			random.shuffle(random_list)
			removeIndex = random_list[0]
			removed_moves.add(removeIndex)
			removeIndex = impMoves[removeIndex]

			ccosts[removeIndex] *= -1

			nMovesTemp = self.__mylib.getNoConflictMoves(len(cids), cids, ciis, cjjs, ccosts,
				impMovesTemp, impValueTemp, maximize)
			if (not maximize and impValue[0] > impValueTemp[0]) or \
					(maximize and impValue[0] < impValueTemp[0]):
				# print "trocou {} por {}".format(impValue[0], impValueTemp[0])
				nMoves = nMovesTemp
				impValue[0] = impValueTemp[0]
				for x in xrange(len(cids)):
					impMoves[x] = impMovesTemp[x]

			ccosts[removeIndex] *= -1

		# Return movements on the initial order
		impMoves = sorted(impMoves[:nMoves])
		return from_list_to_tuple([cids[x] for x in impMoves],
			[ciis[x] for x in impMoves],
			[cjjs[x] for x in impMoves],
			[ccosts[x] for x in impMoves])


def from_list_to_tuple(ids=[], iis=[], jjs=[], costs=[]):
	return numpy.array(ids, dtype=ctypes.c_ushort), \
		numpy.array(iis, dtype=ctypes.c_uint), \
		numpy.array(jjs, dtype=ctypes.c_uint), \
		numpy.array(costs, dtype=ctypes.c_int)


def from_tuple_to_movement_list(values_tuple):
	# return [SimpleMovement(values_tuple[0][x], values_tuple[1][x], values_tuple[2][x], values_tuple[3][x])
	# 	for x in xrange(len(values_tuple[0]))]

	# [(solutions[i].movtuple[0][x], solutions[i].movtuple[1][x],
	# solutions[i].movtuple[2][x], solutions[i].movtuple[3][x])
	# for x in xrange(len(solutions[i].movtuple[0]))]
	return [(values_tuple[0][x], values_tuple[1][x], values_tuple[2][x], values_tuple[3][x])
		for x in xrange(len(values_tuple[0]))]


def from_movement_list_to_tuple(values_tuple=[]):
	# return numpy.array([x.movtype for x in values_tuple], dtype=ctypes.c_ushort), \
	# 	numpy.array([x.value_i for x in values_tuple], dtype=ctypes.c_uint), \
	# 	numpy.array([x.value_j for x in values_tuple], dtype=ctypes.c_uint), \
	# 	numpy.array([x.cost for x in values_tuple], dtype=ctypes.c_int)
	return numpy.array([x[0] for x in values_tuple], dtype=ctypes.c_ushort), \
		numpy.array([x[1] for x in values_tuple], dtype=ctypes.c_uint), \
		numpy.array([x[2] for x in values_tuple], dtype=ctypes.c_uint), \
		numpy.array([x[3] for x in values_tuple], dtype=ctypes.c_int)


def get_file_name(solution_index=0):
	return wamca_intance_path + wamca_solution_instance_file[solution_index][0]


wamca_intance_path = wamca2016path + "instances/"
wamca_solution_instance_file = [
	("01_berlin52.tsp", 52),
	("02_kroD100.tsp", 100),
	("03_pr226.tsp", 226),
	("04_lin318.tsp", 318),
	("05_TRP-S500-R1.tsp", 501),
	("06_d657.tsp", 657),
	("07_rat784.tsp", 783),
	("08_TRP-S1000-R1.tsp", 1001),
	# http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/
	# 08
	("u1060.tsp", 1060),
	("vm1084.tsp", 1084),
	("u1432.tsp", 1432),
	("vm1748.tsp", 1748),
	("u1817.tsp", 1817),
	("rl1889.tsp", 1889),
	("u2152.tsp", 2152),
	# 15
	("u2319.tsp", 2319),
	("fnl4461.tsp", 4461),
	("rl5915.tsp", 5915),
	("rl5934.tsp", 5934),
	("rl11849.tsp", 11849),
	# 20
	("usa13509.tsp", 13509),
	("d18512.tsp", 18512)
]
