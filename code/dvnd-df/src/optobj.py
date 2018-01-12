# -*- coding: utf-8 -*-
from pydf import *


class DecisionNode(Node):
	def __init__(self, f, inputn, should_run=lambda x: True, keep_going=lambda x, y: True):
		Node.__init__(self, f, inputn)
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


class OptMessage:
	def __init__(self, solmap={}, source=0, target=[], not_improved=[]):
		self.__solmap = solmap
		self.__source = source
		self.__target = target
		self.__not_improved = not_improved

	def __getitem__(self, item):
		return self.__solmap[item]

	def __setitem__(self, item, val):
		self.__solmap[item] = val

	def get_best(self):
		return min(self.__solmap.values())

	@property
	def source(self):
		return self.__source

	def has_target(self, idx):
		return self.__target[idx]

	def has_not_improved(self, idx):
		return not self.__not_improved[idx]

	def no_improvement(self):
		return all(self.__not_improved)

	def unset_all_targets(self):
		self.__target = [False for x in self.__target]

	def set_target(self, idx, val=True):
		self.__target[idx] = val
