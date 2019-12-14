# -*- coding: utf-8 -*-
from dataflow.vnd import *


def create_solver(param, mylib, is_use_metadata):
	solver = None
	if param.solver.endswith("_no_df"):
		if "rvnd_no_df" == param.solver or "vnd_no_df" == param.solver:
			solver = VND("rvnd_no_df" == param.solver)
		elif "dvnd_no_df" == param.solver:
			solver = DVND()
	elif "dvnd" == param.solver:
		solver = DataFlowDVND(param.goal, param.mpi_enabled, use_metadata=is_use_metadata,
			use_multiple_output=not param.single_output_gate)
	elif "rvnd" == param.solver:
		solver = DataFlowVND(param.goal, param.mpi_enabled, True)
	elif "vnd" == param.solver:
		solver = DataFlowVND(param.goal, param.mpi_enabled)
	elif "gdvnd" == param.solver:
		assert "ml" == param.problem_name, "Merge solutions not implemented for TTP"
		print("number_of_moves: {}".format(param.number_of_moves))

		def apply_moves_to_sol_on_oper(sol):
			"""
			Apply the moves to the solution.
			:param sol: Solution
			:return: Solution with the moves applied.
			"""
			if len(sol.movtuple[0]) > 0:
				mylib.apply_moves(sol)
			return sol

		def combine_solutions(sol1, sol2):
			return mylib.merge_independent_movements(sol1, sol2)

		solver = DataFlowGDVND(param.goal, param.mpi_enabled,
				apply_moves_to_sol_on_oper,
				mylib.merge_common_movs,
				lambda sol1, sol2: combine_solutions(sol1, sol2), use_metadata=is_use_metadata,
				use_multiple_output=not param.single_output_gate)

	return solver
