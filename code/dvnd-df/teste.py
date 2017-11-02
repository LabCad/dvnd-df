from solution import Solution
from localsearch import *


s = Solution(15)

print(s)

print("%s - bi" % bestImprovement(s, lambda sol,x,y: sol.swap(x, y))[0])
print("%s - s" % s)

print("%s - invert" % s.invert(0, 1))
s.invert(0, 1)
print("%s - invert" % s.invert(0, 2))
s.invert(0, 2)
print("%s - invert" % s.invert(0, 3))
s.invert(0, 3)
print("%s - invert" % s.invert(0, 4))
