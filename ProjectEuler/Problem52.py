"""
It can be seen that the number, 125874, and its double, 251748, contain exactly the same digits, but in a different order.

Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, contain the same digits.
"""
import math
n = 1
while 1:
    n += 1
    #if n x 6 makes the digit increases, then it will not contain the same digits
    if int(math.log10(n*6)) > int(math.log10(n)):
        continue
    n2 = list(str(n*2))
    n3 = list(str(n*3))
    n2.sort()
    n3.sort()
    if n2 != n3:
        continue

    n4 = list(str(n*4))
    n4.sort()
    if n2 != n4:
        continue
        
    n5 = list(str(n*5))
    n5.sort()
    if n2 != n5:
        continue
        
    n6 = list(str(n*6))
    n6.sort()
    if n2 != n6:
        continue

    print "Found:", n
    break