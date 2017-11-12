# -*- coding: utf-8 -*-

from include_lib import *
from solution import *

include_dvnd()
include_pydf()

from pyDF import *


def op1(arg):
	print "Op 1 - ", arg[0] if len(arg) > 0 else ""
	return 9


def op2(arg):
	print "Op 2 - ", arg[0] if len(arg) > 0 else ""
	return 3


def assist(args):
	print "Solution %s" % args[0], args[1]

	if args[1] < args[0] or args[0] is None:
		return args[1]
	else:
		return False


graph = DFGraph()

ini = Feeder(Solution(5, [1, 5, 4, 3, 2]))  # 100 is the initial solution
ini2 = Feeder(Solution(5, [1, 2, 3, 4, 5]))  # -1 is the initial value of the first input of the FliFlop node, to force it propagate the initial solution

heur1 = Node(op1, 1)
heur2 = Node(op2, 1)
# heur3 = Node(op3, 1)

assist1 = FlipFlop(assist)

for i in xrange(1, 3):
	graph.add(eval("heur%d" % i))
graph.add(ini)
graph.add(ini2)

graph.add(assist1)

heur1.add_edge(assist1, 1)
heur2.add_edge(assist1, 1)
# heur3.add_edge(assist1, 1)

assist1.add_edge(heur1, 0)
assist1.add_edge(heur2, 0)
# assist1.add_edge(heur3, 0)
assist1.add_edge(assist1, 0)

ini.add_edge(heur1, 0)
ini.add_edge(heur2, 0)
# ini.add_edge(heur3, 0)
ini.add_edge(assist1, 0)

ini2.add_edge(assist1, 1)

print len(ini.inport)
sched = Scheduler(graph, 5, mpi_enabled=False)
sched.start()

