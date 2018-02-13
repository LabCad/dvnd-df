#!/usr/bin/python
# -*- coding: utf-8 -*-
import ctypes
import numpy
from solution import SolutionVectorValue
from util import array_1d_int, compilelib


# os.getenv('KEY_THAT_MIGHT_EXIST', default_value)
# ttppath = os.getenv('WAMCA2016ABSOLUTEPATH', "/home/rodolfo/git/wamca2016/")

# ttppath = "/home/imcoelho/Rodolfo/wamca2016/"
ttppath = "/home/rodolfo/git/suggarc/"
# localpath = "/home/imcoelho/Rodolfo/dvnd-df/code/dvnd-df/src/"
localpath = "/home/rodolfo/git/dvnd-df/code/dvnd-df/src/"

print "WAMCAPATH:" + ttppath


def create_ttplib():
	mylibname = 'wamca2016lib'
	compilelib([ttppath + "source/*.cu", ttppath + "source/*.cpp"], localpath, mylibname)
	mylib = ctypes.cdll.LoadLibrary("{}{}.so".format(localpath, mylibname))

	# unsigned int bestNeighbor(char * file, int *solution, unsigned int solutionSize, int neighborhood,
	# 	bool justCalc = false, unsigned int hostCode = 0) {
	mylib.bestNeighbor.argtypes = [ctypes.c_void_p, array_1d_int, ctypes.c_uint, ctypes.c_int, ctypes.c_bool,
		ctypes.c_uint]
	# char * file, int *solution, unsigned int solutionSize, int neighborhood, bool justCalc = false
	# mylib.bestNeighbor.argtypes = [ctypes.c_void_p, array_1d_int, ctypes.c_uint, ctypes.c_int, ctypes.c_bool]
	mylib.bestNeighbor.restype = ctypes.c_uint
	# ctypes.POINTER(c_int)

	return mylib


ttplib = create_ttplib()


def calculate_value(file_name, solint, solbool):
	return 1


def best_neighbor(file, solint, solbool, neighborhood, justcalc=False):
	csolint = numpy.array(solint, dtype=ctypes.c_int)
	csolbool = numpy.array(solbool, dtype=ctypes.c_bool)
	# resp = wamca2016lib.bestNeighbor(file, csolint, len(solint), neighborhood, justcalc, gethostcode())
	solint = list(csolint)
	solbool = list(csolbool)
	# solint = list(numpy.ctypeslib.as_array(csolint, shape=(len(solint),)))

	return [], 1


def neigh_gpu(solution, file, inimov):
	resp = best_neighbor(file, solution.vector, inimov)
	return SolutionVectorValue(resp[0], resp[1])


ttp_intance_path = ttppath + "pmv/input/"
ttp_solution_instance_file = [
	("eil51_n50_bounded-strongly-corr_10.ttp", (51, 50)),
	("eil51_n50_uncorr_10.ttp", (51, 50)),
	("eil51_n50_uncorr-similar-weights_10.ttp", (51, 50)),
	("eil51_n150_bounded-strongly-corr_10.ttp", (51, 150)),
	("eil51_n150_uncorr_10.ttp", (51, 150)),
	# 5
	("eil51_n150_uncorr-similar-weights_10.ttp", (51, 150)),
	("eil51_n250_bounded-strongly-corr_10.ttp", (51, 250)),
	("eil51_n250_uncorr_10.ttp", (51, 250)),
	("eil51_n250_uncorr-similar-weights_10.ttp", (51, 250)),
	("eil51_n500_bounded-strongly-corr_10.ttp", (51, 500)),
	# 10
	("eil51_n500_uncorr_10.ttp", (51, 500)),
	("eil51_n500_uncorr-similar-weights_10.ttp", (51, 500)),
	("berlin52_n51_bounded-strongly-corr_10.ttp", (52, 51)),
	("berlin52_n51_uncorr_10.ttp", (52, 51)),
	("berlin52_n51_uncorr-similar-weights_10.ttp", (52, 51)),
	# 15
	("berlin52_n153_bounded-strongly-corr_10.ttp", (52, 153)),
	("berlin52_n153_uncorr_10.ttp", (52, 153)),
	("berlin52_n153_uncorr-similar-weights_10.ttp", (52, 153)),
	("berlin52_n255_bounded-strongly-corr_10.ttp", (52, 255)),
	("berlin52_n255_uncorr_10.ttp", (52, 255)),
	# 20
	("berlin52_n255_uncorr-similar-weights_10.ttp", (52, 255)),
	("berlin52_n510_bounded-strongly-corr_10.ttp", (52, 510)),
	("berlin52_n510_uncorr_10.ttp", (52, 510)),
	("berlin52_n510_uncorr-similar-weights_10.ttp", (52, 510)),
	("st70_n69_bounded-strongly-corr_10.ttp", (70, 69)),
	# 25
	("st70_n69_uncorr_10.ttp", (70, 69)),
	("st70_n69_uncorr-similar-weights_10.ttp", (70, 69)),
	("st70_n207_bounded-strongly-corr_10.ttp", (70, 207)),
	("st70_n207_uncorr_10.ttp", (70, 207)),
	("st70_n207_uncorr-similar-weights_10.ttp", (70, 207)),
	# 30
	("st70_n345_bounded-strongly-corr_10.ttp", (70, 345)),
	("st70_n345_uncorr_10.ttp", (70, 345)),
	("st70_n345_uncorr-similar-weights_10.ttp", (70, 345)),
	("st70_n690_bounded-strongly-corr_10.ttp", (70, 690)),
	("st70_n690_uncorr_10.ttp", (70, 690)),
	# 35
	("st70_n690_uncorr-similar-weights_10.ttp", (70, 690)),
	("rat99_n98_bounded-strongly-corr_10.ttp", (99, 98)),
	("rat99_n98_uncorr_10.ttp", (99, 98)),
	("rat99_n98_uncorr-similar-weights_10.ttp", (99, 98)),
	("rat99_n294_bounded-strongly-corr_10.ttp", (99, 294)),
	# 40
	("rat99_n294_uncorr_10.ttp", (99, 294)),
	("rat99_n294_uncorr-similar-weights_10.ttp", (99, 294)),
	("rat99_n490_bounded-strongly-corr_10.ttp", (99, 490)),
	("rat99_n490_uncorr_10.ttp", (99, 490)),
	("rat99_n490_uncorr-similar-weights_10.ttp", (99, 490)),
	# 45
	("rat99_n980_bounded-strongly-corr_10.ttp", (99, 980)),
	("rat99_n980_uncorr_10.ttp", (99, 980)),
	("rat99_n980_uncorr-similar-weights_10.ttp", (99, 980)),
	("kroA100_n99_bounded-strongly-corr_10.ttp", (100, 99)),
	("kroA100_n99_uncorr_10.ttp", (100, 99)),
	# 50
	("kroA100_n99_uncorr-similar-weights_10.ttp", (100, 99)),
	("kroA100_n297_bounded-strongly-corr_10.ttp", (100, 297)),
	("kroA100_n297_uncorr_10.ttp", (100, 297)),
	("kroA100_n297_uncorr-similar-weights_10.ttp", (100, 297)),
	("kroA100_n495_bounded-strongly-corr_10.ttp", (100, 495)),
	# 55
	("kroA100_n495_uncorr_10.ttp", (100, 495)),
	("kroA100_n495_uncorr-similar-weights_10.ttp", (100, 495)),
	("kroA100_n990_bounded-strongly-corr_10.ttp", (100, 990)),
	("kroA100_n990_uncorr_10.ttp", (100, 990)),
	("kroA100_n990_uncorr-similar-weights_10.ttp", (100, 990))
]
