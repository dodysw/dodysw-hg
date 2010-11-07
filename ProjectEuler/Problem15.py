"""
20x20 => 20 right + 20 down = 40 steps
can be think as 20 green marbles + 20 red marbles, take 40 marbles out of bag.

There are 40! number of permutation, but there are redundancies. 20 are the same (Green), and 20 again the same (Red).
So there are 20! * 20! redundancies
Total: 40!/(20! * 20!) = 137846528820



"""
import math
f = math.factorial

print f(40)/f(20)*f(20)