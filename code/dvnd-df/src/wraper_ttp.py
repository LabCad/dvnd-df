#!/usr/bin/python
# -*- coding: utf-8 -*-
import ctypes
import numpy
import util
from solution import SolutionTTP
from util import gethostcode, array_1d_int, compilelib


# # os.getenv('KEY_THAT_MIGHT_EXIST', default_value)
# # ttppath = os.getenv('WAMCA2016ABSOLUTEPATH', "/home/rodolfo/git/wamca2016/")
#
# # ttppath = "/home/imcoelho/Rodolfo/wamca2016/"
# ttppath = "/home/rodolfo/git/suggarc/suggarC/"
# # localpath = "/home/imcoelho/Rodolfo/dvnd-df/code/dvnd-df/src/"
# localpath = "/home/rodolfo/git/dvnd-df/code/dvnd-df/src/"
#
# print "WAMCAPATH:" + ttppath
#
#
# def create_ttplib():
# 	mylibname = 'ttplib'
# 	# "dvnd/*.cu",
# 	libfiles = ["dvnd/*.cu", "src/po/pmv/ProblemInfo.cu", "src/po/pmv/Solution.cu", "src/po/pmv/BuscaLocal.cu"]
# 	options = ["-std=c++11", "-I {}src".format(ttppath)]
# 	compilelib([ttppath + x for x in libfiles], localpath, mylibname, options)
# 	mylib = ctypes.cdll.LoadLibrary("{}{}.so".format(localpath, mylibname))
#
# 	mylib.bestNeighbor.restype = ctypes.c_double
# 	mylib.bestNeighbor.argtypes = [ctypes.c_void_p, util.array_1d_int, ctypes.c_uint, util.array_1d_bool, ctypes.c_uint,
# 		ctypes.c_uint]
#
# 	# unsigned long int calculateValue(char * file, int * percurso, unsigned int nCidades,
# 	# bool * mochila, unsigned int nMochila)
# 	mylib.calculateValue.restype = ctypes.c_double
# 	mylib.calculateValue.argtypes = [ctypes.c_void_p, util.array_1d_int, ctypes.c_uint, util.array_1d_bool, ctypes.c_uint]
# 	# ctypes.POINTER(c_int)
#
# 	return mylib
#
#
# ttplib = create_ttplib()
#
#
# def calculate_value(file_name="", solint=[], solbool=[]):
# 	csolint = numpy.array(solint, dtype=ctypes.c_int)
# 	csolbool = numpy.array(solbool, dtype=ctypes.c_bool)
# 	return ttplib.calculateValue(file_name, csolint, len(solint), csolbool, len(solbool))
#
#
# def best_neighbor(file_name="", solint=[], solbool=[], neighborhood=0):
# 	csolint = numpy.array(solint, dtype=ctypes.c_int)
# 	csolbool = numpy.array(solbool, dtype=ctypes.c_bool)
# 	resp = ttplib.calculateValue(file_name, csolint, len(solint), csolbool, len(solbool), neighborhood)
# 	solint = list(csolint)
# 	solbool = list(csolbool)
#
# 	return solint, resp, solbool
#
#
# def neigh_gpu(solution=None, file="", inimov=0):
# 	resp = best_neighbor(file, solution.vector, solution.knapsack, inimov)
# 	return SolutionTTP(resp[0], resp[1], resp[2])
#
#
# def get_file_name(solution_index=0):
# 	return ttp_intance_path + ttp_solution_instance_file[solution_index][0]
#
#
# def create_initial_solution(solution_index=0, solution_in_index=None):
# 	sol_info = ttp_solution_instance_file[solution_index]
#
# 	solint = [x for x in xrange(sol_info[1][0])]
# 	solbool = [False for x in xrange(sol_info[1][1])]
# 	print "Size: {},{} - file name: {}".format(sol_info[1][0], sol_info[1][1], sol_info[0])
# 	return SolutionTTP(solint, calculate_value(get_file_name(solution_index), solint, solbool), solbool)
#
#
# ttp_intance_path = ttppath + "../pmv/input/"
# ttp_solution_instance_file = [
# 	("eil51_n50_bounded-strongly-corr_10.ttp", (51, 50)),
# 	("eil51_n50_uncorr_10.ttp", (51, 50)),
# 	("eil51_n50_uncorr-similar-weights_10.ttp", (51, 50)),
# 	("eil51_n150_bounded-strongly-corr_10.ttp", (51, 150)),
# 	("eil51_n150_uncorr_10.ttp", (51, 150)),
# 	# 5
# 	("eil51_n150_uncorr-similar-weights_10.ttp", (51, 150)),
# 	("eil51_n250_bounded-strongly-corr_10.ttp", (51, 250)),
# 	("eil51_n250_uncorr_10.ttp", (51, 250)),
# 	("eil51_n250_uncorr-similar-weights_10.ttp", (51, 250)),
# 	("eil51_n500_bounded-strongly-corr_10.ttp", (51, 500)),
# 	# 10
# 	("eil51_n500_uncorr_10.ttp", (51, 500)),
# 	("eil51_n500_uncorr-similar-weights_10.ttp", (51, 500)),
# 	("berlin52_n51_bounded-strongly-corr_10.ttp", (52, 51)),
# 	("berlin52_n51_uncorr_10.ttp", (52, 51)),
# 	("berlin52_n51_uncorr-similar-weights_10.ttp", (52, 51)),
# 	# 15
# 	("berlin52_n153_bounded-strongly-corr_10.ttp", (52, 153)),
# 	("berlin52_n153_uncorr_10.ttp", (52, 153)),
# 	("berlin52_n153_uncorr-similar-weights_10.ttp", (52, 153)),
# 	("berlin52_n255_bounded-strongly-corr_10.ttp", (52, 255)),
# 	("berlin52_n255_uncorr_10.ttp", (52, 255)),
# 	# 20
# 	("berlin52_n255_uncorr-similar-weights_10.ttp", (52, 255)),
# 	("berlin52_n510_bounded-strongly-corr_10.ttp", (52, 510)),
# 	("berlin52_n510_uncorr_10.ttp", (52, 510)),
# 	("berlin52_n510_uncorr-similar-weights_10.ttp", (52, 510)),
# 	("st70_n69_bounded-strongly-corr_10.ttp", (70, 69)),
# 	# 25
# 	("st70_n69_uncorr_10.ttp", (70, 69)),
# 	("st70_n69_uncorr-similar-weights_10.ttp", (70, 69)),
# 	("st70_n207_bounded-strongly-corr_10.ttp", (70, 207)),
# 	("st70_n207_uncorr_10.ttp", (70, 207)),
# 	("st70_n207_uncorr-similar-weights_10.ttp", (70, 207)),
# 	# 30
# 	("st70_n345_bounded-strongly-corr_10.ttp", (70, 345)),
# 	("st70_n345_uncorr_10.ttp", (70, 345)),
# 	("st70_n345_uncorr-similar-weights_10.ttp", (70, 345)),
# 	("st70_n690_bounded-strongly-corr_10.ttp", (70, 690)),
# 	("st70_n690_uncorr_10.ttp", (70, 690)),
# 	# 35
# 	("st70_n690_uncorr-similar-weights_10.ttp", (70, 690)),
# 	("rat99_n98_bounded-strongly-corr_10.ttp", (99, 98)),
# 	("rat99_n98_uncorr_10.ttp", (99, 98)),
# 	("rat99_n98_uncorr-similar-weights_10.ttp", (99, 98)),
# 	("rat99_n294_bounded-strongly-corr_10.ttp", (99, 294)),
# 	# 40
# 	("rat99_n294_uncorr_10.ttp", (99, 294)),
# 	("rat99_n294_uncorr-similar-weights_10.ttp", (99, 294)),
# 	("rat99_n490_bounded-strongly-corr_10.ttp", (99, 490)),
# 	("rat99_n490_uncorr_10.ttp", (99, 490)),
# 	("rat99_n490_uncorr-similar-weights_10.ttp", (99, 490)),
# 	# 45
# 	("rat99_n980_bounded-strongly-corr_10.ttp", (99, 980)),
# 	("rat99_n980_uncorr_10.ttp", (99, 980)),
# 	("rat99_n980_uncorr-similar-weights_10.ttp", (99, 980)),
# 	("kroA100_n99_bounded-strongly-corr_10.ttp", (100, 99)),
# 	("kroA100_n99_uncorr_10.ttp", (100, 99)),
# 	# 50
# 	("kroA100_n99_uncorr-similar-weights_10.ttp", (100, 99)),
# 	("kroA100_n297_bounded-strongly-corr_10.ttp", (100, 297)),
# 	("kroA100_n297_uncorr_10.ttp", (100, 297)),
# 	("kroA100_n297_uncorr-similar-weights_10.ttp", (100, 297)),
# 	("kroA100_n495_bounded-strongly-corr_10.ttp", (100, 495)),
# 	# 55
# 	("kroA100_n495_uncorr_10.ttp", (100, 495)),
# 	("kroA100_n495_uncorr-similar-weights_10.ttp", (100, 495)),
# 	("kroA100_n990_bounded-strongly-corr_10.ttp", (100, 990)),
# 	("kroA100_n990_uncorr_10.ttp", (100, 990)),
# 	("kroA100_n990_uncorr-similar-weights_10.ttp", (100, 990))
# ]
