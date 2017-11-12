# -*- coding: utf-8 -*-

from include_lib import *
from solution import *
from copy import *

include_dvnd()
include_pydf()

from pyDF import *


def op1(arg):
	sol = arg[0]
	print "Op 1 - ", sol if len(arg) > 0 else ""
	best_move = None
	best_move_value = sol.value
	mov = Movement(MovementType.SWAP)
	for i in xrange(len(sol)):
		for j in xrange(i + 1, len(sol)):
			mov.x, mov.y = i, j
			sol.accept(mov)
			actual_val = sol.value
			if sol.value < best_move_value:
				best_move_value = actual_val
				best_move = Movement(mov.movtype, mov.x, mov.y)
			sol.accept(mov)
	if best_move is not None:
		# sol = copy(sol)
		sol.accept(best_move)

	# print "Op 1 - ", sol if len(arg) > 0 else ""
	return sol


def op2(arg):
	sol = arg[0]
	print "Op 2 - ", sol if len(arg) > 0 else ""
	best_move = None
	best_move_value = sol.value
	mov = Movement(MovementType.TWO_OPT)
	for i in xrange(len(sol)):
		for j in xrange(i + 1, len(sol)):
			mov.x, mov.y = i, j
			sol.accept(mov)
			actual_val = sol.value
			if sol.value < best_move_value:
				best_move_value = actual_val
				best_move = Movement(mov.movtype, mov.x, mov.y)
			sol.accept(mov)
	if best_move is not None:
		sol.accept(best_move)

	# print "Op 2 - ", sol if len(arg) > 0 else ""
	return sol


def assist(args):
	print "Solution %s" % args[0], args[1]

	if (len(args[1]) > 0 and args[1] < args[0]) or len(args[0]) == 0:
		return args[1]
	else:
		return False


graph = DFGraph()

emptySol = Solution(0)
iniSol = Solution(10)
iniSol.rand()

print "emptySol ", emptySol
print "iniSol ", iniSol

ini = Feeder(emptySol)  # -1 is the initial value of the first input of the FliFlop node, to force it propagate the initial solution
ini2 = Feeder(iniSol)  # 100 is the initial solution

heurSize = 2

heur = [Node(eval("op%d" % i), 1) for i in xrange(1, heurSize + 1)]

assist1 = FlipFlop(assist)

for i in xrange(heurSize):
	graph.add(heur[i])
graph.add(ini)
graph.add(ini2)

graph.add(assist1)

for i in xrange(heurSize):
	heur[i].add_edge(assist1, 1)

for i in xrange(heurSize):
	assist1.add_edge(heur[i], 0)
assist1.add_edge(assist1, 0)

# for i in xrange(heurSize):
# 	ini.add_edge(heur[i], 0)

ini.add_edge(assist1, 0)
ini2.add_edge(assist1, 1)

# print len(ini.inport)

sched = Scheduler(graph, 5, mpi_enabled=False)
sched.start()
