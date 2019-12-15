# -*- coding: utf-8 -*-


class VNS(object):
	def run(self, solution, kmax, tmax, shake, local_search):
		best = solution
		for _ in xrange(tmax):
			solution = best
			k = 1
			while k <= kmax:
				xline = shake(solution, k)
				xline = local_search(xline)
				if xline < best:
					best = xline
					k = 1
				else:
					k += 1

		return best
