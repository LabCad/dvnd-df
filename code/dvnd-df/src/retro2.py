from include_lib import *
from solution import *
from solution_movement import *

include_dvnd()
include_pydf()

from pyDF import *


def ope_x(args, idx, inimov):
	if args[1] is None:
		return None
	if args[0] is None or args[1][1] == idx:
		sol = args[1][0][idx] if args[0] is None else min(args[0][0][args[0][1]], args[1][0][idx])
		mov = inimov
		best_sol = deepcopy(sol)
		best_val = sol.value
		for i in xrange(len(sol)):
			for j in xrange(i + 1, len(sol)):
				mov.x, mov.y = i, j
				sol.accept(mov)
				new_val = sol.value
				if new_val < best_val:
					best_sol = deepcopy(sol)
					best_val = new_val
				sol.accept(mov)
		return {idx: best_sol}, idx
	else:
		return args[0]


def op0(arg):
	return ope_x(arg, 0, Movement(MovementType.SWAP))


def op1(arg):
	return ope_x(arg, 1, Movement(MovementType.TWO_OPT))


def ger(args):
	if args[0] is None:
		args[0] = {}
	if len(args[0]) == 0 or args[1][1] not in args[0]:
		args[0][args[1][1]] = args[1][0]

	return args[0]


sols = [x.rand() for x in [Solution(5) for x in xrange(2)]]
resp = op0([({0: sols[0]}, 0), ({0: sols[1]}, 0)])
print resp
print resp[0]

resp2 = ger([None, ({0: sols[0]}, 0)])
print resp2
print resp2[0]
