"""
n! means n x (n  - 1) x ... x 3 x 2 x 1
Find the sum of the digits in the number 100!
"""
import math
print sum([int(n) for n in str(math.factorial(100))])