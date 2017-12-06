# -*- coding: utf-8 -*-

from include_lib import *

include_dvnd()
include_pydf()


from pyDF import *


def op1(intput):
	print "Op 1", intput
	return max(10, intput[0] - 1) if intput[0] > 0 else intput[0]


def op2(intput):
	print "Op 2", intput
	return max(10, intput[0] - 2) if intput[0] > 0 else intput[0]


def op3(intput):
	print "Op 3", intput
	return max(10, intput[0] - 3) if intput[0] > 0 else intput[0]


def assist(args):
	print "Solution %s" %args
	
	if args[1] < args[0] or args[0] < 0:
		return args[1]
	else:
		return False


graph = DFGraph()

ini = Feeder(-1) #-1 is the initial value of the first input of the FliFlop node, to force it propagate the initial solution
ini2 = Feeder(100) #100 is the initial solution

heur1 = Node(op1, 1)
heur2 = Node(op2, 1)
heur3 = Node(op3, 1)


assist1 = FlipFlop(assist)

for i in range(1, 4):
	graph.add(eval("heur%d" %i))
graph.add(ini)
graph.add(ini2)

graph.add(assist1)

heur1.add_edge(assist1, 1)
heur2.add_edge(assist1, 1)
heur3.add_edge(assist1, 1)

assist1.add_edge(heur1, 0)
assist1.add_edge(heur2, 0)
assist1.add_edge(heur3, 0)
assist1.add_edge(assist1, 0)

ini.add_edge(heur1, 0)
ini.add_edge(heur2, 0)
ini.add_edge(heur3, 0)
ini.add_edge(assist1, 0)

ini2.add_edge(assist1, 1)

print len(ini.inport)
sched = Scheduler(graph, 5, mpi_enabled = False)
sched.start()

