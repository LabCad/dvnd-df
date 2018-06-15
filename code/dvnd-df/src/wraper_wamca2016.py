#!/usr/bin/python
# -*- coding: utf-8 -*-
import ctypes
import numpy
import util
import os.path
from movement import *
from solution import SolutionVectorValue, SolutionMovementTuple
from util import compilelib


# os.getenv('KEY_THAT_MIGHT_EXIST', default_value)
# wamca2016path = os.getenv('WAMCA2016ABSOLUTEPATH', "/home/rodolfo/git/wamca2016/")

wamca2016path_uff = "/home/imcoelho/Rodolfo/wamca2016/"
wamca2016path_local = "/home/rodolfo/git/wamca2016/"
localpath_uff = "/home/imcoelho/Rodolfo/dvnd-df/code/dvnd-df/src/"
localpath_local = "/home/rodolfo/git/dvnd-df/code/dvnd-df/src/"

wamca2016path = wamca2016path_uff if os.path.isdir(wamca2016path_uff) else wamca2016path_local
localpath = localpath_uff if os.path.isdir(localpath_uff) else localpath_local

print("wamca2016path: {}".format(wamca2016path))
print("localpath: {}".format(localpath))

print "WAMCAPATH:" + wamca2016path


class MLMove(object):
	"""
	typedef enum {
		MLMI_SWAP,
		MLMI_2OPT,
		MLMI_OROPT1,
		MLMI_OROPT2,
		MLMI_OROPT3,
	} MLMoveId;

	struct MLMove {
		MLMoveId  id;
		int       i;
		int       j;
		int       cost;
	};
	"""
	def __init__(self, id=0, i=0, j=0, cost=0):
		self.id = id
		self.i = i
		self.j = j
		self.cost = cost

	def __str__(self):
		return "{{id:{},i:{},j:{},cost:{}}}".format(self.id, self.i, self.j, self.cost)


def create_wamca2016lib():
	files = [wamca2016path + "source/*.cu", wamca2016path + "source/*.cpp"]
	mylibname = 'wamca2016lib'
	options = ["-lgomp"]
	# options = []
	compiler_options = ["-fopenmp"]
	# compiler_options = []
	compilelib(files, localpath, mylibname, options, compiler_options)
	mylib = ctypes.cdll.LoadLibrary("{}{}.so".format(localpath, mylibname))

	# unsigned int bestNeighbor(char * file, int *solution, unsigned int solutionSize, int neighborhood,
	# 	bool justCalc = false, unsigned int hostCode = 0,
	#   unsigned int useMoves = 0, unsigned short *ids = NULL, unsigned int *is = NULL,
	#   unsigned int *js = NULL, unsigned int *costs = NULL) {
	mylib.bestNeighbor.argtypes = [ctypes.c_void_p, util.array_1d_int, ctypes.c_uint, ctypes.c_int,
		ctypes.c_bool, ctypes.c_uint,
		ctypes.c_uint, util.array_1d_ushort, util.array_1d_uint,
		util.array_1d_uint, util.array_1d_int]
	# char * file, int *solution, unsigned int solutionSize, int neighborhood, bool justCalc = false
	mylib.bestNeighbor.restype = ctypes.c_uint

	# int getNoConflictMoves(unsigned int useMoves, unsigned short * ids, unsigned int * is, unsigned int * js,
	#   int * costs, int * selectedMoves, int * impValue)
	mylib.getNoConflictMoves.restype = ctypes.c_int
	mylib.getNoConflictMoves.argtypes = [ctypes.c_uint, util.array_1d_ushort, util.array_1d_uint,
		util.array_1d_uint, util.array_1d_int, util.array_1d_int, util.array_1d_int]
	# ctypes.POINTER(c_int)

	# unsigned int applyMoves(char * file, int * solution, unsigned int solutionSize, unsigned int useMoves = 0,
	#   unsigned short * ids = NULL, unsigned int * is = NULL, unsigned int * js = NULL, int * costs = NULL)
	mylib.applyMoves.restype = ctypes.c_uint
	mylib.applyMoves.argtypes = [ctypes.c_void_p, util.array_1d_int, ctypes.c_uint, ctypes.c_uint,
		util.array_1d_ushort, util.array_1d_uint, util.array_1d_uint, util.array_1d_int]

	return mylib


wamca2016lib = create_wamca2016lib()


def calculate_value(file_name="", solint=[]):
	return best_neighbor(file_name, solint, 1, True)[1]


def best_neighbor(file="", solint=[], neighborhood=0, justcalc=False):
	# csolint = numpy.array(solint, dtype=ctypes.c_int)
	# csolint = solint
	resp = wamca2016lib.bestNeighbor(file, solint, len(solint), neighborhood, justcalc, 0,#gethostcode(),
		0, numpy.array([], dtype=ctypes.c_ushort), numpy.array([], dtype=ctypes.c_uint),
		numpy.array([], dtype=ctypes.c_uint), numpy.array([], dtype=ctypes.c_int))
	# solint = list(csolint)
	# solint = list(numpy.ctypeslib.as_array(csolint, shape=(len(solint),)))

	return solint, resp


def from_list_to_tuple(ids=[], iis=[], jjs=[], costs=[]):
	return numpy.array(ids, dtype=ctypes.c_ushort), \
		numpy.array(iis, dtype=ctypes.c_uint), \
		numpy.array(jjs, dtype=ctypes.c_uint), \
		numpy.array(costs, dtype=ctypes.c_int)


def from_tuple_to_movement(value_tuple):
	return SimpleMovement(value_tuple[0], value_tuple[1], value_tuple[2], value_tuple[3])


def from_tuple_to_movement_list(values_tuple):
	return [SimpleMovement(values_tuple[0][x], values_tuple[1][x], values_tuple[2][x], values_tuple[3][x])
		for x in xrange(len(values_tuple[0]))]


def from_movement_list_to_tuple(values_tuple=[]):
	return numpy.array([x.movtype for x in values_tuple], dtype=ctypes.c_ushort), \
		numpy.array([x.value_i for x in values_tuple], dtype=ctypes.c_uint), \
		numpy.array([x.value_j for x in values_tuple], dtype=ctypes.c_uint), \
		numpy.array([x.cost for x in values_tuple], dtype=ctypes.c_int)


def merge_solutions(solutions):
	if all([solutions[0].can_merge(solutions[x]) for x in xrange(1, len(solutions))]):
		intersection = set(from_tuple_to_movement_list(solutions[0].movtuple))
		for i in xrange(1, len(solutions)):
			intersection &= set(from_tuple_to_movement_list(solutions[i].movtuple))
		if len(intersection) > 0:
			# FIXME Aplicar os movimentos ao vector
			return [SolutionMovementTuple(sol.vector, sol.value,
				from_movement_list_to_tuple(list(set(from_tuple_to_movement_list(sol.movtuple)) - intersection)))
				for sol in solutions]
	return solutions


def best_neighbor_moves(file="", solint=[], neighborhood=0, n_moves=0):
	# csolint = numpy.array(solint, dtype=ctypes.c_int)
	# csolint = solint

	carrays = from_list_to_tuple([0 for x in xrange(n_moves)], [0 for x in xrange(n_moves)],
		[0 for x in xrange(n_moves)], [0 for x in xrange(n_moves)])

	# cids = numpy.array([0 for x in xrange(n_moves)], dtype=ctypes.c_ushort)
	# ciis = numpy.array([0 for x in xrange(n_moves)], dtype=ctypes.c_uint)
	# cjjs = numpy.array([0 for x in xrange(n_moves)], dtype=ctypes.c_uint)
	# ccosts = numpy.array([0 for x in xrange(n_moves)], dtype=ctypes.c_int)

	resp = wamca2016lib.bestNeighbor(file, solint, len(solint), neighborhood, False, 0,#gethostcode(),
		n_moves, carrays[0], carrays[1], carrays[2], carrays[3])
	# resp = wamca2016lib.bestNeighbor(file, solint, len(solint), neighborhood, False, 0,# gethostcode(),
	# 	0, numpy.array([], dtype=ctypes.c_ushort), numpy.array([], dtype=ctypes.c_uint),
	# 	numpy.array([], dtype=ctypes.c_uint), numpy.array([], dtype=ctypes.c_int))
	# solint = list(csolint)
	# mlmoves = []
	# for i in xrange(n_moves):
	# 	mlmoves.append(MLMove(cids[i], ciis[i], cjjs[i], ccosts[i]))

	# return solint, resp, (cids, ciis, cjjs, ccosts)
	return solint, resp, carrays


def neigh_gpu(solution=None, file="", inimov=0):
	resp = best_neighbor(file, solution.vector, inimov)
	return SolutionVectorValue(resp[0], resp[1])


def neigh_gpu_moves(solution=None, file="", inimov=0, n_moves=0):
	resp = best_neighbor_moves(file, solution.vector, inimov, n_moves)
	return SolutionMovementTuple(resp[0], resp[1], resp[2])


def get_file_name(solution_index=0):
	return wamca_intance_path + wamca_solution_instance_file[solution_index][0]


def copy_solution(ini_solution):
	return SolutionVectorValue(numpy.copy(ini_solution.vector), ini_solution.value)


def create_initial_solution(solution_index=0, solver_param=""):
	sol_info = wamca_solution_instance_file[solution_index]

	# solint = [x for x in xrange(sol_info[1])]
	solint = numpy.array([x for x in xrange(sol_info[1])], dtype=ctypes.c_int)
	print "Size: {} - file name: {}".format(sol_info[1], sol_info[0])
	if "gdvnd" == solver_param:
		return SolutionMovementTuple(solint, calculate_value(get_file_name(solution_index), solint), ([], [], [], []))
	else:
		return SolutionVectorValue(solint, calculate_value(get_file_name(solution_index), solint))


def merge_moves(moves1=[], moves2=[]):
	len1 = len(moves1[0])
	for i in xrange(len1):
		if moves1[3][i] >= 0:
			len1 = i
			break

	len2 = len(moves2[0])
	for i in xrange(len2):
		if moves2[3][i] >= 0:
			len2 = i
			break

	return numpy.concatenate((moves1[0][:len1], moves2[0][:len2])), \
			numpy.concatenate((moves1[1][:len1], moves2[1][:len2])), \
			numpy.concatenate((moves1[2][:len1], moves2[2][:len2])), \
			numpy.concatenate((moves1[3][:len1], moves2[3][:len2]))


def get_no_conflict(cids, ciis, cjjs, ccosts):
	print "Todos os movimentos"
	for i in xrange(len(cids)):
		print "{}-id:{}, i: {}, j: {}, cost: {}".format(i, cids[i], ciis[i], cjjs[i], ccosts[i])
	impMoves = numpy.array([x for x in xrange(100)], dtype=ctypes.c_int)
	impValue = numpy.array([0], dtype=ctypes.c_int)
	nMoves = wamca2016lib.getNoConflictMoves(len(cids), cids, ciis, cjjs, ccosts, impMoves, impValue)
	impValue = impValue[0]
	# TODO Testar se os movimentos aplicados chegam na mesma solução
	impId = numpy.array([cids[(x + 1) % nMoves] for x in xrange(nMoves)], dtype=ctypes.c_ushort)
	impI = numpy.array([ciis[(x + 1) % nMoves] for x in xrange(nMoves)], dtype=ctypes.c_uint)
	impJ = numpy.array([cjjs[(x + 1) % nMoves] for x in xrange(nMoves)], dtype=ctypes.c_uint)
	impCost = numpy.array([ccosts[(x + 1) % nMoves] for x in xrange(nMoves)], dtype=ctypes.c_int)
	print "pyth selected"
	print " ".join([str(impMoves[x]) for x in xrange(nMoves)])
	# for i in xrange(nMoves):
	# 	impId[i] = cids[impMoves[(i + 1) % nMoves]]
	# 	impI[i] = ciis[impMoves[(i + 1) % nMoves]]
	# 	impJ[i] = cjjs[impMoves[(i + 1) % nMoves]]
	# 	impCost[i] = ccosts[impMoves[(i + 1) % nMoves]]
	# print "Python {} moves, impvalue: {}".format(nMoves, impValue[0])
	return impId, impI, impJ, impCost, impValue


def apply_moves_tuple(file="", solint=[], tupple=None):
	return apply_moves(file, solint, tupple[0], tupple[1], tupple[2], tupple[3])


def apply_moves(file="", solint=[], cids=None, ciis=None, cjjs=None, ccosts=None):
	# unsigned int applyMoves(char * file, int * solution, unsigned int solutionSize, unsigned int useMoves = 0,
	#   unsigned short * ids = NULL, unsigned int * is = NULL, unsigned int * js = NULL, int * costs = NULL)
	return wamca2016lib.applyMoves(file, solint, len(solint), len(cids), cids, ciis, cjjs, ccosts)
	# return wamca2016lib.applyMoves(file, solint, len(solint), 1, cids,ciis, cjjs, ccosts)
	# idx = 0
	# return wamca2016lib.applyMoves(file, solint, len(solint), 1, cids[idx:], ciis[idx:], cjjs[idx:], ccosts[idx:])


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
