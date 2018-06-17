# -*- coding: utf-8 -*-
from copy import *
# from solution import Solution


def bestImprovement(solution, oper, undooper=None, mini=True):
	copia = copy(solution)
	resp = None
	while True:
		resp = __bi(copia, oper, undooper)
		if (mini and resp[1] <= 0) or (resp[1] >= 0):
			break
		copia = resp[0]
	return resp


def __bi(solution, oper, undooper=None):
	copia = copy(solution)
	temp = copy(solution)
	melhor = (copia, copia.value)
	undooper = undooper if undooper != None else oper
	for x in xrange(len(copia)):
		for y in xrange(x + 1, len(copia)):
			# solution.swap(x, y)
			oper(temp, x, y)
			value = temp.value
			if melhor[1] > value:
				# copia.swap(x, y)
				oper(copia, x, y)
				melhor = (copia, value)
			undooper(temp, x, y)
	return melhor[0], temp.value - melhor[1]
