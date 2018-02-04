#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
from optobj import *
from include_lib import *
include_dvnd()
include_pydf()
from pyDF import Feeder


class DataFlowVND(object):
	def __init__(self, maximize=False, mpi_enabled=False, is_rvnd=False):
		self.__maximize = maximize
		self.__mpi_enabled = mpi_enabled
		self.__is_rvnd = is_rvnd

	@staticmethod
	def __neighborhood(func, args, maximize):
		resp = func(args[0][0])
		return [resp, resp < args[0][0] if not maximize else args[0][0] < resp]

	def run(self, number_of_workers, initial_solution, oper_funtions, result_callback=lambda x: True):
		graph = DFGraph()

		iniNode = Feeder([initial_solution, True])
		graph.add(iniNode)

		fimNode = DecisionNode(lambda y: result_callback([y[0][0]]), 1, lambda a: not a[0][1])
		graph.add(fimNode)

		if self.__is_rvnd:
			oper_funtions = [x for x in oper_funtions]
			random.shuffle(oper_funtions)

		numberOfOpers = len(oper_funtions)
		operNode = [DecisionNode(lambda arg, idx=x: DataFlowVND.__neighborhood(oper_funtions[idx], arg, self.__maximize), 1,
			lambda a, y=x: a[0][1] if y == 0 else (not a[0][1])) for x in xrange(numberOfOpers)]

		for operIt in operNode:
			graph.add(operIt)
			operIt.add_edge(operNode[0], 0)

		for x in xrange(numberOfOpers - 1):
			operNode[x].add_edge(operNode[x + 1], 0)

		iniNode.add_edge(operNode[0], 0)
		operNode[numberOfOpers - 1].add_edge(fimNode, 0)

		Scheduler(graph, number_of_workers, mpi_enabled=self.__mpi_enabled).start()


class DataFlowDVND(object):
	def __init__(self, maximize=False, mpi_enabled=False):
		self.__maximize = maximize
		self.__mpi_enabled = mpi_enabled

	@staticmethod
	def __neighborhood(func, args, inimov):
		atual = args[0]
		atual.source = inimov
		atual[inimov] = func(atual[inimov])
		return atual

	def __manager(self, args):
		atual = args[0]
		melhor = args[1]

		# melhor_ini = melhor.get_best()
		melhor.unset_all_targets()
		# atualValue = atual[atual.source]

		if (not self.__maximize and atual[atual.source] < melhor[atual.source]) \
				or (self.__maximize and melhor[atual.source] < atual[atual.source]):
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

		return melhor

	def run(self, number_of_workers, initial_solution, oper_funtions, result_callback=lambda x: True):
		graph = DFGraph()

		# Nó final Cria n
		numberOfOpers = len(oper_funtions)
		fimNode = DecisionNode(lambda y: result_callback([y[0][i] for i in xrange(numberOfOpers)]), 1,
			lambda x: x[0].no_improvement())
		graph.add(fimNode)

		# Nó de gerenciamento ligado nele mesmo e no nó final
		manNode = DecisionNode(self.__manager, 2)
		graph.add(manNode)
		manNode.add_edge(manNode, 1)
		manNode.add_edge(fimNode, 0)

		# Nó que inicializa o nó gerenciador
		iniManNode = Feeder(OptMessage({x: initial_solution for x in xrange(numberOfOpers)}, numberOfOpers,
			[False for y in xrange(numberOfOpers)], [False for i in xrange(numberOfOpers)]))
		graph.add(iniManNode)
		iniManNode.add_edge(manNode, 1)

		# Nós de operações
		oper_should_run = [lambda x, a=y: x[0].has_target(a) for y in xrange(numberOfOpers)]
		oper_keep_going = [lambda a, b: True for y in xrange(numberOfOpers)]
		operNode = [DecisionNode(lambda arg, fnc=oper_funtions[i], it=i: DataFlowDVND.__neighborhood(fnc, arg, it),
			1, oper_should_run[i], oper_keep_going[i]) for i in xrange(numberOfOpers)]
		for x in operNode:
			graph.add(x)
			manNode.add_edge(x, 0)
			x.add_edge(manNode, 0)

		# Nós que inicializam nós de operação
		iniNode = [Feeder(OptMessage({x: initial_solution}, x, [x == y for y in xrange(numberOfOpers)],
			[False for i in xrange(numberOfOpers)])) for x in xrange(numberOfOpers)]
		for i in xrange(numberOfOpers):
			graph.add(iniNode[i])
			iniNode[i].add_edge(operNode[i], 0)

		Scheduler(graph, number_of_workers, mpi_enabled=self.__mpi_enabled).start()
