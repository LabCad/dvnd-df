# -*- coding: utf-8 -*-
from include_lib import include_dvnd, include_pydf
include_dvnd()
include_pydf()
from pyDF import Node, Oper


class DecisionNode(Node):
	"""
	Decision node is a generalization of the default node that lets decide to process or not its input.
	"""
	def __init__(self, f=lambda x: None, inputn=1, should_run=lambda x: True, keep_going=lambda x, y: True):
		"""
		:param f: Function to be called for processing.
		:param inputn: Number of inputs.
		:param should_run: Lambda indicating if the function f has to be called.
		:param keep_going: Lambada indicating if comes back to the graph.
		"""
		super(DecisionNode, self).__init__(f, inputn)
		self.__should_run = should_run
		self.__keep_going = keep_going

	def run(self, args, workerid, operq):
		param_args = [a.val for a in args]
		if not self.__should_run(param_args):
			self.sendops([Oper(workerid, None, None, None)], operq)
		else:
			resp = self.f(param_args)

			if not self.__keep_going(param_args, resp):
				opers = [Oper(workerid, None, None, None)]
			else:
				opers = self.create_oper(resp, workerid, operq)

			self.sendops(opers, operq)


class Metadata(object):
	def __init__(self):
		"""Number of called localseaches."""
		self.age = 0

		"""Total time elapsed on the manager node."""
		self.man_time = 0
		"""Time elapsed on a single merge operation."""
		self.man_merge_time = 0
		"""Time getting best solution"""
		self.man_get_best_time = 0

		"""Time taken by neighborhood process."""
		self.neighbor_time = 0
		"""Time elapsed processing solution before it is sent to the localsearch."""
		self.neighbor_proc_before_time = 0
		"""Time elapsed on the localsearch itself."""
		self.neighbor_func_time = 0
		"""Time elapsed on the C function call."""
		self.neighbor_func_inner_time = 0
		"""Time elapsed allocating numpy arrays."""
		self.neighbor_func_numpy_alloc_time = 0
		self.neighbor_func_numpy_resize_time = 0
		self.neighbor_func_mpi_time = 0
		self.neighbor_func_rest = 0

		"""Vector of neighborhoods calls count."""
		self.counts = None
		"""Vector with the number of comibined solutions count."""
		self.combine_count = None
		"""Count of merges on the movements."""
		self.merge_count = 0


class OptMessage(object):
	"""
	History for the DVND.
	"""
	def __init__(self, solmap={}, source=0, target=[], not_improved=[]):
		"""
		:param solmap: Map os solutions (node code, actual solution).
		:param source: Source of the history.
		:param target: Targets to the history.
		:param not_improved: Nodes that couldn't improve the solution.
		"""
		self.__solmap = solmap
		self.__source = source
		self.__target = target
		self.__not_improved = not_improved
		self.metadata = Metadata()
		self.metadata.counts = [0 for x in target]
		self.metadata.combine_count = [0 for x in target]

	def __getitem__(self, item=0):
		return self.__solmap[item]

	def __setitem__(self, item=0, val=None):
		self.__solmap[item] = val

	def __len__(self):
		return len(self.__solmap)

	def get_best(self, maximize=False):
		"""
		:param maximize: Indicates is is a maximization o minimization problem.
		:return: Get the best solution on the history.
		"""
		return max(self.__solmap.values()) if maximize else min(self.__solmap.values())

	@property
	def source(self):
		return self.__source

	@source.setter
	def source(self, value):
		self.__source = value

	def has_target(self, idx=0):
		return self.__target[idx]

	def has_not_improved(self, idx=0):
		return not self.__not_improved[idx]

	def no_improvement(self):
		return all(self.__not_improved)

	def unset_all_targets(self):
		self.__target = [False for x in self.__target]

	def set_target(self, idx=0, val=True):
		self.__target[idx] = val

	def set_not_improved(self, idx=0, val=True):
		self.__not_improved[idx] = val

	def __contains__(self, item=None):
		return item in self.__solmap

	def __str__(self):
		return "sol: {}, s: {}, t: {}, ni: {}".format(self.__solmap, self.__source,
			self.__target, self.__not_improved)

	def get_not_improveds(self):
		return [x for x in xrange(len(self.__not_improved)) if self.__not_improved[x]]
