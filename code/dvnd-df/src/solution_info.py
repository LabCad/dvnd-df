# -*- coding: utf-8 -*-
from abc import *
from math import sqrt


class SolutionInfo(object):
	@abstractmethod
	def get_distance(self, x, y):
		pass

	@abstractmethod
	def __len__(self):
		pass


class SolutionInfoAdjacencyMatrix(SolutionInfo):
	def __init__(self, distvec=[]):
		self.__distvec = distvec

	def get_distance(self, x, y):
		return self.__distvec[x][y]

	def __len__(self):
		return len(self.__distvec)

	def __str__(self):
		return "{{distvec: {}}}".format(self.__distvec)


class SolutionInfoEuclidianPosition(SolutionInfo):
	def __init__(self, positions=[]):
		self.__positions = positions

	def get_distance(self, x, y):
		xd = self.__positions[x][0] - self.__positions[y][0]
		yd = self.__positions[x][1] - self.__positions[y][1]
		return sqrt(xd * xd + yd * yd)

	def __len__(self):
		return len(self.__positions)

	def __str__(self):
		return "{{pos: {}}}".format(self.__positions)
