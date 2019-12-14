# -*- coding: utf-8 -*-
from dvnd_df.wrapper.wamca2016 import WamcaWraper


def create_lib_connection(param):
	mylib = None
	goal = False
	if "tt" == param.problem_name:
		from wrapper.ttp import create_initial_solution, neigh_gpu, get_file_name
		file_name = get_file_name(param.solution_index)
		if not param.only_compile:
			ini_solution = create_initial_solution(param.solution_index)

			neigh_op = [lambda ab, y=mv: neigh_gpu(ab, file_name, y) for mv in xrange(5)]
		goal = True
	elif "ml" == param.problem_name:
		from wrapper.wamca2016 import get_file_name

		file_name = get_file_name(param.solution_index)
		mylib = WamcaWraper(file_name, useMultipleGpu=param.multi_gpu, deviceCount=param.device_count)
		if not param.only_compile:
			ini_solution = mylib.create_initial_solution(param.solution_index, param.solver,
				param.solution_instance_index)

			if "gdvnd" == param.solver:
				neigh_op = [lambda ab, y=mv: mylib.neigh_gpu_moves(ab, y, param.number_of_moves)
					for mv in xrange(param.number_of_moves)]
			else:
				neigh_op = [lambda ab, y=mv: mylib.neigh_gpu(ab, y) for mv in xrange(param.number_of_moves)]

	return mylib, ini_solution, neigh_op, goal
