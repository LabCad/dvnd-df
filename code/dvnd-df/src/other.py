#!/usr/bin/python
# -*- coding: utf-8 -*-

from include_lib import *
from optobj import *
from solution import *
from solution_movement import *

include_dvnd()
include_pydf()


from pyDF import *


initialSolution = 10


def fim(args):
	print "Fim - len: {} - sv: {}, best: {}".format(len(args), args[0].solvalue, args[0].get_best())


def manager(args):
	atual = args[0]
	melhor = args[1]
	melhor.solvalue[atual.source] = atual.solvalue[atual.source]
	ini_str = "sv: {}, m: !{}!".format(atual.solvalue, melhor)

	melhor_ini = melhor.get_best()
	melhor.unset_all_targets()
	atualValue = atual[atual.source]

	if atual[atual.source] < melhor[atual.source]:
		melhor[atual.source] = atual[atual.source]
		melhor.set_target(atual.source)
	else:
		melhor.set_not_improved(atual.source)
	melhor[atual.source] = melhor.get_best()

	print "Manager - s:{}, antes: {}, best: {}, atual: {} - {}, m2: !{}!".format(
		atual.source, melhor_ini, melhor.get_best(), atualValue, ini_str, melhor)
	return melhor


def oper_n(args, oper_idx):
	antes = args[0][oper_idx]
	args[0].source = oper_idx
	solvalue = args[0].solvalue
	str_antes = "oper{} - sv: {}".format(oper_idx, solvalue)
	args[0][oper_idx] = solvalue[oper_idx].pop(0) if len(solvalue[oper_idx]) > 0 else args[0][oper_idx]
	print "{} - {}, antes: {}, best: {}".format(str_antes, solvalue, antes, args[0][oper_idx])
	return args[0]


def test_oper(args, n):
	# print "test_oper{} - len: {} - {}".format(n, len(args), args[0][n])
	return args[0].has_target(n)


numberOfWorkers = 2
numberOfOpers = 2

operFunc = [lambda x: oper_n(x, 0), lambda x: oper_n(x, 1)]
operShouldRunFunc = [lambda x: test_oper(x, 0), lambda x: test_oper(x, 1)]
operKeepGoinFunc = [lambda a, b: True, lambda a, b: True]
# operNode = [DecisionNode(lambda y: oper_n(y, i), 1, lambda y: y[0].has_target(i), lambda x, y: x[0][i] > y[i]) for i in xrange(numberOfOpers)]

graph = DFGraph()

fimNode = DecisionNode(fim, 1, lambda x: x[0].no_improvement())
graph.add(fimNode)

manNode = DecisionNode(manager, 2)
graph.add(manNode)
manNode.add_edge(manNode, 1)
manNode.add_edge(fimNode, 0)

iniManNode = Feeder(OptMessage({x: initialSolution for x in xrange(numberOfOpers)}, numberOfOpers,
	[False for y in xrange(numberOfOpers)], [False for i in xrange(numberOfOpers)]))
graph.add(iniManNode)
iniManNode.add_edge(manNode, 1)

operNode = [DecisionNode(operFunc[i], 1, operShouldRunFunc[i], operKeepGoinFunc[i]) for i in xrange(numberOfOpers)]
for x in operNode:
	graph.add(x)
	manNode.add_edge(x, 0)
	x.add_edge(manNode, 0)

iniNode = [Feeder(OptMessage({x: initialSolution}, x, [x == y for y in xrange(numberOfOpers)],
	[False for i in xrange(numberOfOpers)])) for x in xrange(numberOfOpers)]
for i in xrange(numberOfOpers):
	graph.add(iniNode[i])
	iniNode[i].add_edge(operNode[i], 0)

Scheduler(graph, numberOfWorkers, mpi_enabled=False).start()
