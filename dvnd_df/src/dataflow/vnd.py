#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import time
import threading
# from mpi4py import MPI
from optobj import DecisionNode, OptMessage, Metadata
from pyDF import DFGraph, Feeder, Scheduler, SelectOutputNode, Node


class Solver(object):
	def run(self, number_of_workers=1, initial_solution=None, oper_functions=[], result_callback=lambda x, y: True):
		raise NotImplementedError()


class DataFlowVND(Solver):
	def __init__(self, maximize=False, mpi_enabled=False, is_rvnd=False):
		"""
		:param maximize: Indica se é um problema de maximização ou minimização.
		:param mpi_enabled: Indica se usa MPI.
		:param is_rvnd: Indica se o método é VND ou RVND
		"""
		self.__maximize = maximize
		self.__mpi_enabled = mpi_enabled
		self.__is_rvnd = is_rvnd

	@staticmethod
	def __neighborhood(func=lambda args: None, args=[], maximize=False):
		resp = func(args[0][0])[0]
		return [max(resp, args[0][0]) if maximize else min(resp, args[0][0]),
			resp < args[0][0] if not maximize else args[0][0] < resp, args[0][2] + 1]

	def run(self, number_of_workers=1, initial_solution=None, oper_funtions=[], result_callback=lambda x, y: True):
		"""
		:param number_of_workers: Número de workers Sucuri.
		:param initial_solution: Solução inicial.
		:param oper_funtions: Funções dos operadores, vizinhanças.
		:param result_callback: Método chamado quando o processo termina.
		"""
		graph = DFGraph()

		ini_node = Feeder([initial_solution, True, 0])
		graph.add(ini_node)

		fim_node = DecisionNode(lambda y: result_callback([y[0][0]], Metadata(counts=[y[0][2]])), 1, lambda a: not a[0][1])
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


class DataFlowDVND(Solver):
	def __init__(self, maximize=False, mpi_enabled=False, process_sol_before_oper=lambda arg: arg, use_metadata=False,
			use_multiple_output=True):
		"""
		:param maximize: Indica se é um problema de maximização ou minimização.
		:param mpi_enabled: Indica se usa MPI.
		"""
		self.maximize = maximize
		self.__mpi_enabled = mpi_enabled
		self.__process_sol_before_oper = process_sol_before_oper
		self.use_metadata = use_metadata
		self.use_multiple_output = use_multiple_output

	def __neighborhood(self, func=lambda arg: None, args=[], inimov=0):
		atual = args[0]
		atual.metadata.neigh_time = -time.time()
		atual.source = inimov
		sol_param = atual[inimov] if self.__process_sol_before_oper is None \
			else self.__process_sol_before_oper(atual[inimov])

		func_resp = func(sol_param)
		atual[inimov] = max(atual[inimov], func_resp[0]) if self.maximize \
			else min(atual[inimov], func_resp[0])

		atual.metadata.neigh_time += time.time()
		return atual

	def best_solution(self, atual=None, anterior=None, melhor=None):
		"""
		Decide qual é a melhor solução.
		:param atual: Solution returned by the operation node.
		:param anterior: Actual solution on the manager node.
		:param melhor: Best solution on manager node.
		:return: Melhor solução e flag indicando se a melhor é a atual.
		"""
		if (not self.maximize and atual < anterior) or (self.maximize and anterior < atual):
			return atual, True, False
		return anterior, False, False

	def manager(self, args=[]):
		atual = args[0]
		melhor = args[1]
		melhor.metadata.man_time -= time.time()

		# melhor_ini = melhor.get_best()
		melhor.unset_all_targets()
		# atualValue = atual[atual.source]

		melhor.metadata.man_best_sol_time -= time.time()
		atual_melhor = self.best_solution(atual[atual.source], melhor[atual.source], melhor.get_best())
		melhor[atual.source] = atual_melhor[0]
		melhor.metadata.man_best_sol_time += time.time()

		if atual_melhor[1]:
			melhor.set_target(atual.source)
		else:
			melhor.set_not_improved(atual.source)

		best_sol = melhor[atual.source] = melhor.get_best()
		# Caso não tenha melhorado mas tenha aparecido uma solução melhor
		for x in melhor.get_not_improveds():
			if (not self.maximize and best_sol < melhor[x]) or (self.maximize and best_sol > melhor[x]):
				melhor[x] = best_sol
				melhor.set_target(x)
				# Se vai chamar novamente remove o sinal
				melhor.set_not_improved(x, False)

		melhor.metadata.man_time += time.time()
		melhor.metadata.neigh_time += atual.metadata.neigh_time
		melhor.metadata.man_combine_sol_time += atual_melhor[3] if len(atual_melhor) > 3 else 0
		melhor.metadata.counts[atual.source] += 1
		return DataFlowDVND.create_response_map(melhor, len(melhor)) if self.use_multiple_output else melhor

	@staticmethod
	def create_response_map(optmessage, number_of_opers):
		if optmessage.no_improvement():
			return {number_of_opers + 1: optmessage}
		else:
			resp = {x: optmessage for x in xrange(len(optmessage)) if optmessage.has_target(x)}
			resp[number_of_opers] = optmessage
			return resp

	def run(self, number_of_workers=1, initial_solution=None, oper_funtions=[], result_callback=lambda x, y: True):
		"""
		:param number_of_workers: Número de workers Sucuri.
		:param initial_solution: Solução inicial.
		:param oper_funtions: Funções dos operadores, vizinhanças.
		:param result_callback: Método chamado quando o processo termina.
		"""
		graph = DFGraph()

		number_of_opers = len(oper_funtions)
		# End node only processed when there is no improvement
		if self.use_multiple_output:
			fimNode = Node(lambda y: result_callback([y[0][i] for i in xrange(number_of_opers)], y[0].metadata), 1)
		else:
			fimNode = DecisionNode(lambda y: result_callback([y[0][i] for i in xrange(number_of_opers)], y[0].metadata),
				1, lambda x: x[0].no_improvement())
		graph.add(fimNode)

		# Nó de gerenciamento ligado nele mesmo e no nó final
		if self.use_multiple_output:
			man_node = SelectOutputNode(self.manager, 2)
			graph.add(man_node)
			man_node.add_edge(man_node, 1, number_of_opers)
			man_node.add_edge(fimNode, 0, number_of_opers + 1)
		else:
			man_node = DecisionNode(self.manager, 2)
			graph.add(man_node)
			man_node.add_edge(man_node, 1)
			man_node.add_edge(fimNode, 0)

		# Nó que inicializa o nó gerenciador
		if self.use_multiple_output:
			ini_man_node = Feeder(OptMessage({x: initial_solution for x in xrange(number_of_opers)}, number_of_opers,
				[False for y in xrange(number_of_opers)], [False for i in xrange(number_of_opers)], self.maximize))
		else:
			ini_man_node = Feeder(OptMessage({x: initial_solution for x in xrange(number_of_opers)}, number_of_opers,
				[False for y in xrange(number_of_opers)], [False for i in xrange(number_of_opers)]))
		graph.add(ini_man_node)
		ini_man_node.add_edge(man_node, 1)

		# Nós de operações
		if self.use_multiple_output:
			oper_node = [Node(lambda arg, fnc=oper_funtions[i], it=i: self.__neighborhood(fnc, arg, it), 1)
				for i in xrange(number_of_opers)]
			for i in xrange(number_of_opers):
				graph.add(oper_node[i])
				man_node.add_edge(oper_node[i], 0, i)
				oper_node[i].add_edge(man_node, 0)
		else:
			oper_should_run = [lambda x, a=y: x[0].has_target(a) for y in xrange(number_of_opers)]
			oper_keep_going = [lambda a, b: True for y in xrange(number_of_opers)]
			oper_node = [DecisionNode(lambda arg, fnc=oper_funtions[i], it=i: self.__neighborhood(fnc, arg, it),
				1, oper_should_run[i], oper_keep_going[i]) for i in xrange(number_of_opers)]
			for x in oper_node:
				graph.add(x)
				man_node.add_edge(x, 0)
				x.add_edge(man_node, 0)

		# Nós que inicializam nós de operação
		ini_node = [Feeder(OptMessage({x: initial_solution}, x, [x == y for y in xrange(number_of_opers)],
			[False for i in xrange(number_of_opers)], self.maximize)) for x in xrange(number_of_opers)]
		for i in xrange(number_of_opers):
			graph.add(ini_node[i])
			ini_node[i].add_edge(oper_node[i], 0)

		Scheduler(graph, number_of_workers, mpi_enabled=self.__mpi_enabled).start()


class DataFlowGDVND(DataFlowDVND):
	def __init__(self, maximize=False, mpi_enabled=False, process_sol_before_oper=lambda arg: None,
			merge_solutions=lambda sols=[]: sols, combine_sol=lambda sol1, sol2: sol1, use_metadata=False,
			use_multiple_output=True):
		"""
		:param maximize: Indica se é um problema de maximização ou minimização.
		:param mpi_enabled: Indica se usa MPI.
		:param merge_solutions: The merge solution function.
		:param process_sol_before_oper: Process the solution before it is sent to the operation node.
		"""
		super(DataFlowGDVND, self).__init__(maximize, mpi_enabled, process_sol_before_oper, use_metadata,
			use_multiple_output)
		self.__merge_solutions = merge_solutions
		self.__combine_sol = combine_sol

	def best_solution(self, atual=None, anterior=None, melhor=None):
		if len(atual.movtuple[0]) > 0 and len(melhor.movtuple[0]) > 0:
			combine_time = -time.time()
			combined_sol_resp = self.__combine_sol(atual, melhor)
			combine_time += time.time()
			combined_sol = combined_sol_resp[0]
			if self.maximize:
				resp_sol = max(atual, anterior, melhor, combined_sol)
				return resp_sol, resp_sol > melhor, combined_sol_resp[1], combine_time
			else:
				resp_sol = min(atual, anterior, melhor, combined_sol)
				return resp_sol, resp_sol < melhor, combined_sol_resp[1], combine_time
		return super(DataFlowGDVND, self).best_solution(atual, anterior, melhor)

	def manager(self, args=[]):
		man_time_before = args[1].metadata.man_time
		man_time = time.time()
		resp = super(DataFlowGDVND, self).manager(args).itervalues().next()

		resp.metadata.man_merge_sol_time -= time.time()
		resp_tuple = self.__merge_solutions([resp[x] for x in xrange(len(resp))])
		resp.metadata.man_merge_sol_time += time.time()

		resp_sol = resp_tuple[0]
		for x in xrange(len(resp)):
			resp[x] = resp_sol[x]

		resp.metadata.man_time = man_time_before + time.time() - man_time
		return DataFlowDVND.create_response_map(resp, len(resp)) if self.use_multiple_output else resp


class VND(Solver):
	def __init__(self, isrvnd=True):
		self.isrvnd = isrvnd

	def run(self, number_of_workers=1, initial_solution=None, oper_funtions=[], result_callback=lambda x, y: True):
		from copy import deepcopy

		if self.isrvnd:
			random.shuffle(oper_funtions)

		metadata = Metadata(counts=[0 for x in xrange(len(oper_funtions))])
		solution = deepcopy(initial_solution)
		k = 0
		while k < len(oper_funtions):
			metadata.counts[k] += 1
			# numpy.copyto(solution2.vector, solution.vector)
			# solution2.value = solution.value
			solution2 = deepcopy(solution)
			# resp = mylib.neigh_gpu(solution2, k)
			resp = oper_funtions[k](solution2)
			if resp[0] < solution:
				k = 0
				# numpy.copyto(solution.vector, resp[0].vector)
				# solution.value = resp[0].value

				solution = deepcopy(resp[0])
			else:
				k += 1

		result_callback([solution], metadata)


class NeighborhoodThread(threading.Thread):
	def __init__(self, fun, sol):
		super(NeighborhoodThread, self).__init__()
		self.setDaemon(True)
		self.resp = None
		self.fun = fun
		self.solution = sol

	def run(self):
		self.resp = self.fun(self.solution)[0]


class DVND(Solver):
	def run(self, number_of_workers=1, initial_solution=None, oper_funtions=[], result_callback=lambda x, y: True):
		from copy import deepcopy

		def negigh_dvnd(solution, idx, resp, funfun):
			resp[idx] = funfun(solution)[0]
			return resp[idx]

		# neigh_op = [lambda sol, idx, resp, funfun=ope, y=mv: negigh_dvnd(sol, idx, resp, funfun) for ope in neigh_op]
		neigh_count = len(oper_funtions)
		solution = deepcopy(initial_solution)
		metadata = Metadata(counts=[0 for x in xrange(len(oper_funtions))])

		melhorou = True
		while melhorou:
			my_threads = [NeighborhoodThread(oper_funtions[i], deepcopy(initial_solution)) for i in xrange(neigh_count)]
			melhorou = False
			for i in xrange(neigh_count):
				metadata.counts[i] += 1
				my_threads[i].start()

			for it_tread in my_threads:
				# if it_tread.isAlive():
				it_tread.join()
				if it_tread.resp < solution:
					melhorou = True
					solution = deepcopy(it_tread.resp)

			if not melhorou:
				for i in xrange(neigh_count):
					resp = oper_funtions[i](deepcopy(solution))[0]
					metadata.counts[i] += 1
					if resp < solution:
						melhorou = True
						solution = deepcopy(resp)
						break

		result_callback([solution], metadata)
