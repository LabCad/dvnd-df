from solution import Solution
from localsearch import *


s = Solution(10)

print(s)

print("%s - swap" % bestImprovement(s, lambda sol,x,y: sol.swap(x, y), lambda sol,x,y: sol.swap(x, y), False)[0])
# print("%s - s" % s)
print("%s - invert" % bestImprovement(s, lambda sol,x,y: sol.invert(x, y), lambda sol,x,y: sol.invert(x, y), False)[0])
print("%s - s" % s)

# print("%s - invert" % s.invert(0, 1))
# s.invert(0, 1)
# print("%s - invert" % s.invert(0, 2))
# s.invert(0, 2)
# print("%s - invert" % s.invert(0, 3))
# s.invert(0, 3)
# print("%s - invert" % s.invert(0, 4))
