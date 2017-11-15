# -*- coding: utf-8 -*-

from include_lib import *
from solution import *
from solution_movement import *

include_dvnd()
include_pydf()

from pyDF import *


def op_param(movtype, arg):
	sol = (arg[0]).gen_solution()
	best_move = None
	best_move_value = ini_sol_value = sol.value
	mov = Movement(movtype)
	for i in xrange(len(sol)):
		for j in xrange(i + 1, len(sol)):
			mov.x, mov.y = i, j
			sol.accept(mov)
			actual_val = sol.value
			if actual_val < best_move_value:
				best_move_value = actual_val
				best_move = Movement(mov.movtype, mov.x, mov.y)
			sol.accept(mov)

	if best_move is not None:
		solmov = SolutionMovement(sol, best_move, best_move_value - ini_sol_value)
		if arg[0].can_merge(solmov):
			arg[0].merge(solmov)
		else:
			resp = SolutionMovementCollection(sol)
			resp.merge(solmov)
			return resp

	return arg[0]


def op1(arg):
	return op_param(MovementType.SWAP, arg)


def op2(arg):
	return op_param(MovementType.TWO_OPT, arg)


def assist(args):
	# print "Solution %s - %s" % (args[0], args[1])
	# print "final %s - %s" % (args[0].gen_solution(), args[1].gen_solution())

	if args[0].value is None or args[1] < args[0]:
		print "sol mov %s - %s" % (args[1], args[1].gen_solution())
		return deepcopy(args[1])
	else:
		# print "Parou2 ", args[0], args[1]
		return False


graph = DFGraph()

emptySol = Solution(0)
iniSol = Solution(50)
print "iniSol ", iniSol

ini = Feeder(SolutionMovementCollection(iniSol))  # -1 is the initial value of the first input of the FliFlop node, to force it propagate the initial solution
ini2 = Feeder(SolutionMovementCollection(emptySol))  # 100 is the initial solution

heurSize = 2

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

sched = Scheduler(graph, 5, mpi_enabled=False)
sched.start()
