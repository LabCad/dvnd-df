#!/usr/bin/python
# -*- coding: utf-8 -*-
from optobj import *
from include_lib import *
include_dvnd()
include_pydf()
from pyDF import Feeder


class DataFlowOpt(object):
	def __init__(self, maximize=False, mpi_enabled=False):
		self.__maximize = maximize
		self.__mpi_enabled = mpi_enabled

	def __manager(self, args):
		atual = args[0]
		melhor = args[1]
		# melhor.solvalue[atual.source] = atual.solvalue[atual.source]
		# ini_str = "sv: {}, m: !{}!".format(atual.solvalue, melhor)

		# melhor_ini = melhor.get_best()
		melhor.unset_all_targets()
		# atualValue = atual[atual.source]

		if (not self.__maximize and atual[atual.source] < melhor[atual.source]) \
				or (self.__maximize and atual[atual.source] > melhor[atual.source]):
			melhor[atual.source] = atual[atual.source]
			melhor.set_target(atual.source)
		else:
			melhor.set_not_improved(atual.source)
		best_sol = melhor[atual.source] = melhor.get_best(self.__maximize)
		# Caso não tenha melhorado mas tenha aparecido uma solução melhor
		for x in melhor.get_not_improveds():
			if (not self.__maximize and best_sol < melhor[x]) or (self.__maximize and best_sol > melhor[x]):
				melhor[x] = best_sol
				melhor.set_target(x)
				# Se vai chamar novamente remove o sinal
				melhor.set_not_improved(x, False)

		# print "Manager - s:{}, antes: {}, best: {}, atual: {} - {}, m2: !{}!".format(
		# 	atual.source, melhor_ini, melhor.get_best(), atualValue, ini_str, melhor)

		# TODO Remover
		print "melhor valor: ", best_sol.value
		return melhor

	def run(self, number_of_workers, initial_solution, oper_funtions, result_callback=lambda x: True):
		graph = DFGraph()

		fimNode = DecisionNode(result_callback, 1, lambda x: x[0].no_improvement())
		graph.add(fimNode)

		manNode = DecisionNode(self.__manager, 2)
		graph.add(manNode)
		manNode.add_edge(manNode, 1)
		manNode.add_edge(fimNode, 0)
		numberOfOpers = len(oper_funtions)

		iniManNode = Feeder(OptMessage({x: initial_solution for x in xrange(numberOfOpers)}, numberOfOpers,
			[False for y in xrange(numberOfOpers)], [False for i in xrange(numberOfOpers)]))
		graph.add(iniManNode)
		iniManNode.add_edge(manNode, 1)

		oper_should_run = [lambda x, a=y: x[0].has_target(a) for y in xrange(numberOfOpers)]
		oper_keep_going = [lambda a, b: True for y in xrange(numberOfOpers)]
		operNode = [DecisionNode(oper_funtions[i], 1, oper_should_run[i], oper_keep_going[i])
			for i in xrange(numberOfOpers)]
		for x in operNode:
			graph.add(x)
			manNode.add_edge(x, 0)
			x.add_edge(manNode, 0)

		iniNode = [Feeder(OptMessage({x: initial_solution}, x, [x == y for y in xrange(numberOfOpers)],
			[False for i in xrange(numberOfOpers)])) for x in xrange(numberOfOpers)]
		for i in xrange(numberOfOpers):
			graph.add(iniNode[i])
			iniNode[i].add_edge(operNode[i], 0)

		Scheduler(graph, number_of_workers, mpi_enabled=self.__mpi_enabled).start()
