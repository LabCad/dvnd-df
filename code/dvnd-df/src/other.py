#!/usr/bin/python
# -*- coding: utf-8 -*-

from include_lib import *
from optobj import *
from solution import *
from solution_movement import *

include_dvnd()
include_pydf()


from pyDF import *


def fim(args):
	print "Fim - len: {0} - {1}".format(len(args), args)
	return args[0]


def manager(args):
	print "Manager - len: {0} - {1}".format(len(args), args)
	atual = args[0]
	melhor = args[1]
	melhor.unset_all_targets()
	if atual[atual.source] < melhor[atual.source]:
		melhor[atual.source] = atual[atual.source]
		melhor.set_target(atual.source)
	melhor[atual.source] = melhor.get_best()
	return melhor


def oper_n(args, n):
	print "oper{0} - len: {1} - {2}".format(n, len(args), args)
	args[0].source = n
	args[0][n] = 9 if n != 0 else 8
	return args[0]


def test_oper(args, n):
	print "test_oper{0} - len: {1} - {2}".format(n, len(args), args)
	return args[0].has_target(n)


numberOfWorkers = 2
numberOfOpers = 2
initialSolution = 10

graph = DFGraph()

fimNode = DecisionNode(fim, 1, lambda x: x[0].no_improvement())
graph.add(fimNode)

manNode = DecisionNode(manager, 2)
graph.add(manNode)
manNode.add_edge(manNode, 1)
manNode.add_edge(fimNode, 0)

iniManNode = Feeder(OptMessage({x: initialSolution for x in xrange(numberOfOpers)}, numberOfOpers, [True for i in xrange(numberOfOpers)]))
graph.add(iniManNode)
iniManNode.add_edge(manNode, 1)

# operNode = [DecisionNode(lambda y: oper_n(y, i), 1, lambda y: y[0].has_target(i), lambda x, y: x[0][i] > y[i]) for i in xrange(numberOfOpers)]
# operNode = [DecisionNode(lambda a: oper_n(a, i), 1, lambda b: test_oper(b, i), lambda x, c: x[0][i] > c[i]) for i in xrange(numberOfOpers)]
operNode = [DecisionNode(lambda a: oper_n(a, i), 1, lambda b: test_oper(b, i)) for i in xrange(numberOfOpers)]
for x in operNode:
	graph.add(x)
	manNode.add_edge(x, 0)
	x.add_edge(manNode, 0)

iniNode = [Feeder(OptMessage({x: initialSolution}, numberOfOpers, [x == y for y in xrange(numberOfOpers)])) for x in xrange(numberOfOpers)]
for i in xrange(numberOfOpers):
	graph.add(iniNode[i])
	iniNode[i].add_edge(operNode[i], 0)

Scheduler(graph, numberOfWorkers, mpi_enabled=False).start()
