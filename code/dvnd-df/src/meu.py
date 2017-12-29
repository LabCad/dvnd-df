#!/usr/bin/python
# -*- coding: utf-8 -*-

from include_lib import *
from solution import *
from solution_movement import *

include_dvnd()
include_pydf()


from pyDF import *


class Memoria(Node):
	def __init__(self, f):
		self.f = f
		self.inport = [[], []]
		self.dsts = []
		self.affinity = None

	def run(self, args, workerid, operq):
		opers = self.create_oper(self.f([a.val for a in args]), workerid, operq)

		if opers[0].val is None:
			opers = [Oper(workerid, None, None, None)]
		self.sendops(opers, operq)


def ope1(args):
	print args[0]
	return max(args[0][0] - 1, 0), 1


def ope2(args):
	print args[0]
	return max(args[0][0] - 2, 0), 2


def ope_man(args):
	print args[0], args[1]
	if args[0][0] < args[1][0]:
		return args[0]
	elif args[1][0] < args[0][0]:
		return args[1]
	return None if args[0][1] == args[1][1] else (args[0][0], 0)


graph = DFGraph()

heurSize = 2

inicial = Feeder((10, 0))
heur = [Node(eval("ope%d" % i), 1) for i in xrange(1, heurSize + 1)]
man_node = Memoria(ope_man)

for h in heur:
	graph.add(h)
graph.add(inicial)
graph.add(man_node)

for h in heur:
	inicial.add_edge(h, 0)
	h.add_edge(man_node, 1)
	man_node.add_edge(h, 0)
inicial.add_edge(man_node, 0)
man_node.add_edge(man_node, 0)

sched = Scheduler(graph, 5, mpi_enabled=False)
sched.start()
