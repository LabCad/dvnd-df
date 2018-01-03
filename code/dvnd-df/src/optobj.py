# -*- coding: utf-8 -*-
from pydf import *


class DecisionNode(Node):
	def __init__(self, f, inputn, should_run, keep_going):
		Node.__init__(self, f, inputn)
		self.__should_run = should_run
		self.__keep_going = keep_going

	def run(self, args, workerid, operq):
		if not self.__should_run(args):
			self.sendops([Oper(workerid, None, None, None)], operq)
		else:
			resp = self.f([a.val for a in args])

			if not self.__keep_going(args, resp):
				opers = [Oper(workerid, None, None, None)]
			else:
				opers = self.create_oper(resp, workerid, operq)

			self.sendops(opers, operq)


class OptMessage:
	def __init__(self, solmap, source):
		self.__solmap = solmap
		self.__source = source

	def __getitem__(self, item):
		return self.__solmap[item]

	def getbest(self):
		return min(self.__solmap.values())

	@property
	def source(self):
		return self.__source
