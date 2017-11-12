# -*- coding: utf-8 -*-


class MovementType:
	SWAP = 1
	TWO_OPT = 2
	OR_OPT_K = 3


class Movement:
	def __init__(self, movtype, x=0, y=1, k=None):
		self.movtype = movtype
		self.x = x
		self.y = y
		self.k = k

	def __str__(self):
		return "{ type: %s, x: %d, y: %d%s }" % (self.movtype, self.x, self.y, (", k: %d" % self.k) if self.k is not None else "")

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.movtype == other.movtype and self.x == other.x \
				and self.y == other.y and self.k == other.k
		return False

	def __ne__(self, other):
		"""Define a non-equality test"""
		return not self.__eq__(other)

	def __hash__(self):
		return hash((self.movtype, self.x, self.y, self.k))

	def conflict(self, mov):
		return not self.not_conflict(mov)

	def not_conflict(self, mov):
		if self.movtype == MovementType.SWAP:
			if mov.movtype == MovementType.SWAP:
				return abs(self.x - mov.x) > 1 and abs(self.x - mov.y) > 1 \
					and abs(self.y - mov.x) > 1 and abs(self.y - mov.y) > 1
			elif mov.movtype == MovementType.TWO_OPT:
				return ((self.x < mov.x - 1) or (self.x > mov.y - 1)) \
					and ((self.y < mov.x - 1) or (self.y > mov.y + 1))
			elif mov.movtype == MovementType.OR_OPT_K:
				return (self.y < min(mov.x, mov.y) - 1) or (self.x > min(mov.x, mov.y) + mov. k) \
					or ((self.x < min(mov.x, mov.y) - 1) and (self.y > max(mov.x, mov.y) + mov.k))
		elif self.movtype == MovementType.TWO_OPT:
			if mov.movtype == MovementType.SWAP:
				return ((mov.x < self.x - 1) or (mov.x > self.y + 1)) \
					and ((mov.y < self.x - 1) or (mov.y > self.y + 1))
			elif mov.movtype == MovementType.TWO_OPT:
				return (self.y < mov.x - 1) or (self.x > mov.y + 1) \
					or (mov.y > self.x - 1) or (mov.x > self.y + 1)
			elif mov.movtype == MovementType.OR_OPT_K:
				return (self.x > max(mov.x, mov.y) + mov.k) or (self.y < min(mov.x, mov.y) - 1)
		elif self.movtype == MovementType.OR_OPT_K:
			if mov.movtype == MovementType.SWAP:
				return (mov.y < min(self.x, self.y) - 1) or (mov.x > max(self.x, self.y) + self.k) \
					or ((mov.x < min(self.x, self.y) - 1) and (mov.y > max(self.x, self.y) + self.k))
			elif mov.movtype == MovementType.TWO_OPT:
				return (mov.y < min(self.x, self.y) - 1) or (mov.x > max(self.x, self.y) + self.k)
			elif mov.movtype == MovementType.OR_OPT_K:
				return (max(self.x, self.y) + self.k < min(mov.x, mov.y)) \
					or (min(self.x, self.y) > max(mov.x, mov.y) + mov.k)
		return True
