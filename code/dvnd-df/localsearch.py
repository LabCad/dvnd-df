from copy import *
from solution import Solution

def bestImprovement(solution, oper, undooper=None, mini=True):
	copia = Solution(solution.size, solution.route)
	resp = None
	while True:
		resp = __bi(copia, oper, undooper)
		if (mini and resp[1] <= 0) or (resp[1] >= 0):
			break
		copia = resp[0]
	return resp

def __bi(solution, oper, undooper=None):
	copia = Solution(solution.size, solution.route)
	temp = Solution(solution.size, solution.route)
	melhor = (copia, copia.value)
	undooper = undooper if undooper != None else oper
	for x in xrange(copia.size):
		for y in xrange(x + 1, copia.size):
			#solution.swap(x, y)
			oper(temp, x, y)
			value = temp.value
			if melhor[1] > value:
				#copia.swap(x, y)
				oper(copia, x, y)
				melhor = (copia, value)
			undooper(temp, x, y)
	return (melhor[0], temp.value - melhor[1])
