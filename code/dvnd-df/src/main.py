#!/usr/bin/python2
# -*- coding: utf-8 -*-

from include_lib import *
from solution import *
from solution_movement import *

include_dvnd()
include_pydf()

from pyDF import *

def op_param(inimov, arg):
	solmovcol = deepcopy(arg[0])
	sol = solmovcol.gen_solution()
	ini_sol_value = sol.value
	moves = []
	mov = inimov
	for i in xrange(len(sol)):
		for j in xrange(i + 1, len(sol)):
			mov.x, mov.y = i, j
			sol.accept(mov)
			actual_val = sol.value
			if actual_val < ini_sol_value:
				moves.append((Movement(mov.movtype, mov.x, mov.y, mov.k), actual_val))
			sol.accept(mov)
	moves.sort(key=lambda ax: ax[1])
	moves = [x[0] for x in moves]
	unused = []
	solmovcol_nu = deepcopy(arg[0])
	for x in moves:
		if solmovcol.can_merge(x):
			solmovcol.merge(x)
		else:
			unused.append(x)
	for x in unused:
		solmovcol_nu.merge(x)

	solmovcol_new = SolutionMovementCollection(sol)
	for x in moves:
		solmovcol_new.merge(x)

	return min(solmovcol, solmovcol_nu, solmovcol_new)


def op1(arg):
	return op_param(Movement(MovementType.SWAP), arg)


def op2(arg):
	return op_param(Movement(MovementType.TWO_OPT), arg)


def op3(arg):
	return op_param(Movement(MovementType.OR_OPT_K, 0, 0, 2), arg)


def assist(args):
	print "Solution %s - %s" % (args[0], args[1])
	print "final %s - %s" % (args[0].gen_solution(), args[1].gen_solution())

	assert(len(args[1]) > 0)

	if len(args[0]) == 0 or (args[0].value is None) or args[1] < args[0]:
		print "sol mov %s - %s" % (args[1], args[1].gen_solution())

		x = deepcopy(args[1])
		assert(len(x) == len(args[1]))
		return x
	else:
		# print "Parou2 ", args[0], args[1]
		return False


graph = DFGraph()

emptySol = Solution(0)
# iniSol = Solution(10, [1, 0, 3, 2, 5, 8, 9, 6, 7, 4])
iniSol = Solution(4)
iniSol.rand()
print "iniSol ", iniSol

ini  = Feeder(SolutionMovementCollection(iniSol))  # -1 is the initial value of the first input of the FliFlop node, to force it propagate the initial solution
ini2 = Feeder(SolutionMovementCollection(emptySol))  # 100 is the initial solution

heurSize = 1

heur = [Node(eval("op%d" % i), 1) for i in xrange(1, heurSize + 1)]

assist1 = FlipFlop(assist)

for h in heur:
	graph.add(h)
graph.add(ini)
graph.add(ini2)

graph.add(assist1)

for h in heur:
	h.add_edge(assist1, 1)

for h in heur:
	assist1.add_edge(h, 0)
assist1.add_edge(assist1, 0)

for h in heur:
	ini.add_edge(h, 0)

ini.add_edge(assist1, 0)
ini2.add_edge(assist1, 1)

# print len(ini.inport)

sched = Scheduler(graph, 3, mpi_enabled=False)

print("OI2")

sched.start()

