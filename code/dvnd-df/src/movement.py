# -*- coding: utf-8 -*-

class MovementType:
	SWAP = 1
	TWO_OPT = 2
	OR_OPT_K = 3

class Movement:
	def __init__(self, type, x, y, k = None):
		self.type = type
		self.x = x
		self.y = y
		self.k = k

	def __str__(self):
		return ("{ type: %s, x: %d, y: %d%s }" % (self.type, self.x, self.y, (", k: %d" % self.k) if self.k != None else ""))

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.type == other.type and self.x == other.x \
				and self.y == other.y and self.k == other.k
		return False

	def __ne__(self, other):
		"""Define a non-equality test"""
		return not self.__eq__(other)

	def __hash__(self):
		return hash((self.type, self.x, self.y, self.k))

	def conflict(self, mov):
		return not self.notConflict(mov)

	def notConflict(self, mov):
		if self.type == MovementType.SWAP:
			if mov.type == MovementType.SWAP:
				return abs(self.x - mov.x) > 1 and abs(self.x - mov.y) > 1 \
					and abs(self.y - mov.x) > 1 and abs(self.y - mov.y) > 1
			elif mov.type == MovementType.TWO_OPT:
				return ((self.x < mov.x - 1) or (self.x > mov.y - 1)) \
					and ((self.y < mov.x - 1) or (self.y > mov.y + 1))
			elif mov.type == MovementType.OR_OPT_K:
				return (self.y < min(mov.x, mov.y) - 1) or (self.x > min(mov.x, mov.y) + mov. k) \
					or ((self.x < min(mov.x, mov.y) - 1) and (self.y > max(mov.x, mov.y) + mov.k))
		elif self.type == MovementType.TWO_OPT:
			if mov.type == MovementType.SWAP:
				return ((mov.x < self.x - 1) or (mov.x > self.y + 1)) \
					and ((mov.y < self.x - 1) or (mov.y > self.y + 1))
			elif mov.type == MovementType.TWO_OPT:
				return (self.y < mov.x - 1) or (self.x > mov.y + 1) \
					or (mov.y > self.x - 1) or (mov.x > self.y + 1)
			elif mov.type == MovementType.OR_OPT_K:
				return (self.x > max(mov.x, mov.y) + mov.k) or (self.y < min(mov.x, mov.y) - 1)
		elif self.type == MovementType.OR_OPT_K:
			if mov.type == MovementType.SWAP:
				return (mov.y < min(self.x, self.y) - 1) or (mov.x > max(self.x, self.y) + self.k) \
					or ((mov.x < min(self.x, self.y) - 1) and (mov.y > max(self.x, self.y) + self.k))
			elif mov.type == MovementType.TWO_OPT:
				return (mov.y < min(self.x, self.y) - 1) or (mov.x > max(self.x, self.y) + self.k)
			elif mov.type == MovementType.OR_OPT_K:
				return (max(self.x, self.y) + self.k < min(mov.x, mov.y)) \
					or (min(self.x, self.y) > max(mov.x, mov.y) + mov.k)
		return True