# -*- coding: utf-8 -*-
import numpy


class SolutionVectorValue(object):
	def __init__(self, vector, value):
		if type(vector) is not numpy.ndarray:
			raise ValueError('Use a numpy array in the vector, for performance reasons')
		self.vector = vector
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


class SolutionMovementTuple(SolutionVectorValue):
	def __init__(self, vector, value, movtuple):
		super(SolutionMovementTuple, self).__init__(vector, value)
		self.movtuple = movtuple

	def can_merge(self, other):
		return super(SolutionMovementTuple, self).__eq__(other)

	# def merge(self, other):
	# 	newtuple = set(SimpleMovement.from_tuple_to_list(self.movtuple)) - \
	# 		set(SimpleMovement.from_tuple_to_list(other.movtuple))
	# 	newtuple = SimpleMovement.from_list_to_tuple(list(newtuple))
	# 	return SolutionMovementTuple(deepcopy(self.vector), self.value, newtuple)

	def __str__(self):
		return "{}-movtuple: []".format(super(SolutionMovementTuple, self).__str__(), self.movtuple)


class SolutionTTP(SolutionVectorValue):
	def __init__(self, vector, value, knapsack):
		super(SolutionTTP, self).__init__(vector, value)
		self.knapsack = knapsack

	def __str__(self):
		return "{}-{}-{}".format(self.value, self.vector, self.knapsack)
