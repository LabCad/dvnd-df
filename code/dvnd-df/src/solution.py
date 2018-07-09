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
	"""
	Solution that includes the list of movements.
	"""
	def __init__(self, vector, value, movtuple):
		super(SolutionMovementTuple, self).__init__(vector, value)
		self.movtuple = movtuple
		self.movvector = numpy.copy(vector)
		self.movapplied = False

	def can_merge(self, other):
		"""
		Indicates if this solution can merge the other.
		:param other: Solution to merge.
		:return: True if the solution can merge.
		"""
		# return super(SolutionMovementTuple, self).__eq__(other)
		return (other.vector == self.vector).all()

	# def merge(self, other):
	# 	newtuple = set(SimpleMovement.from_tuple_to_list(self.movtuple)) - \
	# 		set(SimpleMovement.from_tuple_to_list(other.movtuple))
	# 	newtuple = SimpleMovement.from_list_to_tuple(list(newtuple))
	# 	return SolutionMovementTuple(deepcopy(self.vector), self.value, newtuple)

	def __str__(self):
		return "{}-movtuple: []".format(super(SolutionMovementTuple, self).__str__(), self.movtuple)


class SolutionTTP(SolutionVectorValue):
	"""
	Solution representation for the Traveling Thief Problem.
	"""
	def __init__(self, vector, value, knapsack):
		super(SolutionTTP, self).__init__(vector, value)
		self.knapsack = knapsack

	def __str__(self):
		return "{}-{}-{}".format(self.value, self.vector, self.knapsack)
