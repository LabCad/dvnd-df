#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
# from mpi4py import MPI
from optobj import DecisionNode, OptMessage
from pyDF import DFGraph, Feeder, Scheduler


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

		ini_node = Feeder([initial_solution, True])
		graph.add(ini_node)

		fim_node = DecisionNode(lambda y: result_callback([y[0][0]]), 1, lambda a: not a[0][1])
		graph.add(fim_node)

		if self.__is_rvnd:
			oper_funtions = [x for x in oper_funtions]
			random.shuffle(oper_funtions)

		number_of_opers = len(oper_funtions)
		oper_node = [DecisionNode(lambda arg, idx=x: DataFlowVND.__neighborhood(oper_funtions[idx], arg, self.__maximize), 1,
			lambda a, y=x: a[0][1] if y == 0 else (not a[0][1])) for x in xrange(number_of_opers)]

		for oper_it in oper_node:
			graph.add(oper_it)
			oper_it.add_edge(oper_node[0], 0)

		for x in xrange(number_of_opers - 1):
			oper_node[x].add_edge(oper_node[x + 1], 0)

		ini_node.add_edge(oper_node[0], 0)
		oper_node[number_of_opers - 1].add_edge(fim_node, 0)

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
		number_of_opers = len(oper_funtions)
		fimNode = DecisionNode(lambda y: result_callback([y[0][i] for i in xrange(number_of_opers)]), 1,
			lambda x: x[0].no_improvement())
		graph.add(fimNode)

		# Nó de gerenciamento ligado nele mesmo e no nó final
		man_node = DecisionNode(self.__manager, 2)
		graph.add(man_node)
		man_node.add_edge(man_node, 1)
		man_node.add_edge(fimNode, 0)

		# Nó que inicializa o nó gerenciador
		ini_man_node = Feeder(OptMessage({x: initial_solution for x in xrange(number_of_opers)}, number_of_opers,
			[False for y in xrange(number_of_opers)], [False for i in xrange(number_of_opers)]))
		graph.add(ini_man_node)
		ini_man_node.add_edge(man_node, 1)

		# Nós de operações
		oper_should_run = [lambda x, a=y: x[0].has_target(a) for y in xrange(number_of_opers)]
		oper_keep_going = [lambda a, b: True for y in xrange(number_of_opers)]
		oper_node = [DecisionNode(lambda arg, fnc=oper_funtions[i], it=i: DataFlowDVND.__neighborhood(fnc, arg, it),
			1, oper_should_run[i], oper_keep_going[i]) for i in xrange(number_of_opers)]
		for x in oper_node:
			graph.add(x)
			man_node.add_edge(x, 0)
			x.add_edge(man_node, 0)

		# if self.__mpi_enabled:
		# 	comm = MPI.COMM_WORLD
		# 	nprocs = comm.Get_size()
		# 	print "MPI {}/{}".format(comm.Get_rank(), nprocs)
		# 	for i in xrange(len(oper_node)):
		# 		# oper_node[i].pin([i % nprocs])

		# Nós que inicializam nós de operação
		ini_node = [Feeder(OptMessage({x: initial_solution}, x, [x == y for y in xrange(number_of_opers)],
			[False for i in xrange(number_of_opers)])) for x in xrange(number_of_opers)]
		for i in xrange(number_of_opers):
			graph.add(ini_node[i])
			ini_node[i].add_edge(oper_node[i], 0)

		Scheduler(graph, number_of_workers, mpi_enabled=self.__mpi_enabled).start()
