

class Solution(object):
	def __init__(self, size, route = None):
		self.size = size
		if route == None:
			self.route = [x for x in xrange(size)]
		else:
			self.route = [x for x in route]

	def __str__(self):
		return ("Solution(%d): %s - %d" % (self.size, self.route, self.value))

	@property
	def value(self):
		return sum([self.route[i] * (i + 1) for i in xrange(self.size)])

	def swap(self, x, y):
		self.route[x],self.route[y] = self.route[y],self.route[x]
		return self

	def invert(self, x, y):
		self.route[x], self.route[y] = self.route[y], self.route[x]
		for i in xrange(1, (y - x) // 2):
			self.route[x + i], self.route[y - i] = self.route[y - i], self.route[x + i]
		return self