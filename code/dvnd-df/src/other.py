#!/usr/bin/python
# -*- coding: utf-8 -*-

from include_lib import *
from  optobj import *
from solution import *
from solution_movement import *

include_dvnd()
include_pydf()


from pyDF import *


graph = DFGraph()
heurSize = 2

inisol = None

inicial = [Feeder(OptMessage({x: inisol}, x)) for x in xrange(heurSize + 1)]
inicialVazia = Feeder(OptMessage({}, x))
heur = [DecisionNode(eval("ope%d" % i), 1, None, None) for i in xrange(heurSize)]
ger = DecisionNode(None, 2, None, None)
fim = DecisionNode(None, 1, None, None)

graph.add(inicialVazia)
graph.add(ger)
for ini in inicial:
	graph.add(ini)
for h in heur:
	graph.add(h)

inicial[heurSize].add_edge(ger, 0)
inicialVazia.add_edge(ger, 1)
ger.add_edge(ger, 1)
for i in xrange(heurSize):
	inicial[i].add_edge(heur[i], 0)
for h in heur:
	ger.add_edge(h, 0)
	h.add_edge(ger, 0)

sched = Scheduler(graph, 4, mpi_enabled=False)
sched.start()
