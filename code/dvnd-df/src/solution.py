# -*- coding: utf-8 -*-
import numpy


class SolutionVectorValue(object):
	"""
	Solution representation by vector and value.
	Value is used to avoid calculate the objective function each time it is needed.
	"""
	def __init__(self, vector, value=0):
		if type(vector) is not numpy.ndarray:
			raise ValueError('Use a numpy array in the vector, for performance reasons')
		self.__vector = vector
		self.value = value

	def __lt__(self, other):
		return self.value < other.value

	def __len__(self):
		return len(self.vector)

	def __str__(self):
		return "{}-{}".format(self.value, self.vector)

	def __eq__(self, other):
		return other.value == self.value and (other.vector == self.vector).all()

	def __hash__(self):
		return self.value + self.vector[0]

	@property
	def vector(self):
		return self.__vector

	@vector.setter
	def vector(self, value):
		self.__vector = value


class SolutionMovementTuple(SolutionVectorValue):
	"""
	Solution that includes the list of movements.
	"""
	def __init__(self, vector, value, movtuple, movvector=None):
		super(SolutionMovementTuple, self).__init__(vector, value)
		self.__movtuple = movtuple
		self.movvector = movvector if movvector is not None else numpy.copy(vector)
		self.movapplied = False

	def can_merge(self, other):
		"""
		Indicates if this solution can merge the other.
		:param other: Solution to merge.
		:return: True if the solution can merge.
		"""
		# return super(SolutionMovementTuple, self).__eq__(other)
		return (other.vector == self.vector).all()

	@property
	def movtuple(self):
		return self.__movtuple

	@movtuple.setter
	def movtuple(self, value):
		self.__movtuple = value
		self.movapplied = False

	@property
	def vector(self):
		return super(SolutionMovementTuple, self).vector

	@SolutionVectorValue.vector.setter
	def vector(self, value):
		SolutionVectorValue.vector.fset(self, value)
		self.movapplied = False

	def __str__(self):
		return "{}-movtuple: {}".format(super(SolutionMovementTuple, self).__str__(), self.movtuple)


class SolutionTTP(SolutionVectorValue):
	"""
	Solution representation for the Traveling Thief Problem.
	"""
	def __init__(self, vector, value, knapsack):
		super(SolutionTTP, self).__init__(vector, value)
		self.knapsack = knapsack

	def __str__(self):
		return "{}-{}-{}".format(self.value, self.vector, self.knapsack)
