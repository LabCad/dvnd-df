# -*- coding: utf-8 -*-


class SolverType(object):
	VND = 1
	RVND = 2
	DVND = 3
	GDVND = 4


class CommandParams(object):
	def __init__(self, solution_index=0, solution_instance_index=-2, goal="min",
			problem_name="ml", number_of_moves=10, device_count=1, solver="gdvnd", workers=1, single_output_gate=None):
		from util import getparam, hasparam
		self.solution_index = int(getparam("in", None, solution_index))
		self.solution_instance_index = int(getparam("sii", "solution_instance_index", solution_instance_index))
		# solution_in_index = None if "-sn" not in sys.argv else int(sys.argv[sys.argv.index("-sn") + 1])
		self.multi_gpu = hasparam("mg", "multi_gpu")
		self.goal = getparam(None, "goal", goal).lower() == "max"
		self.problem_name = getparam("p", None, problem_name).lower()
		self.number_of_moves = int(getparam(None, "number_of_moves", number_of_moves))
		self.device_count = int(getparam("dc", "device_count", device_count))
		self.solver = getparam("s", "solver", solver).lower()
		self.mpi_enabled = hasparam("mpi")
		self.workers = int(getparam("n", None, workers))

		self.use_dataflow = not self.solver.endswith("_do_df")
		tempmap = {"vnd": SolverType.VND, "rvnd": SolverType.RVND,
			"dvnd": SolverType.DVND, "gdvnd": SolverType.GDVND}
		self.simple_solver = tempmap[self.solver] if self.use_dataflow else tempmap[self.solver[0:-6]]

		self.single_output_gate = single_output_gate if single_output_gate is not None else \
			hasparam("sog", "single_output_gate")

	def __str__(self):
		return "{{solution_index:{}, solution_instance_index:{}, multi_gpu:{}, goal:{}, problem_name:{}, " \
				"number_of_moves:{}, device_count:{}, solver:{}, mpi_enabled:{}, workers:{}}}".\
			format(self.solution_index, self.solution_instance_index, self.multi_gpu, self.goal, self.problem_name,
				self.number_of_moves, self.device_count, self.solver, self.mpi_enabled, self.workers)
