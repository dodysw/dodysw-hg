"""
for 2x2:
00 10 01
00 10 11
00 10 02
00 10 12
00 20 01

00 20 11
00 20 21
00 20 02
00 20 22
00 11 01

00 21 01
00 11 02
00 12 02
00 22 02

a^2 + b^2 = c^2
00 01 10
v1,v2,v3
1, 1, sqr(2)

sorted:
00 01 10
00 01 11
00 01 12 X
00 01 20
00 01 21
00 01 22 X

00 02 10
00 02 11 
00 02 12
00 02 20
00 02 21 X
00 02 22 

00 10 11
00 10 12
00 10 20 X

00 11 20
00 20 21
00 20 22


------

"""

from time import time

st = time()

def is_rightangle(c1,c2,c3):
    #convert point c to vector v
    v1 = c2[0] - c1[0], c2[1] - c1[1]
    v2 = c3[0] - c2[0], c3[1] - c2[1]
    v3 = c1[0] - c3[0], c1[1] - c3[1]
    #square distance
    sqd1 = v1[0]**2 + v1[1]**2
    sqd2 = v2[0]**2 + v2[1]**2
    sqd3 = v3[0]**2 + v3[1]**2
    #the longest vector must equal sum of the others
    return sqd1 + sqd2 + sqd3 - 2*max(sqd1,sqd2,sqd3) == 0
    
    #BjornEdstrom (fasteR)
    #return sqd1 + sqd2 == sqd3 or sqd1 + sqd3 == sqd2 or sqd3 + sqd2 == sqd1
    
def is_rightangle_from_origin(p0,p1):
    """
    a^2 + b^2 = c^2
    x0y0 is at 90deg angle, x2y2 is origin (0,0)
    a^2 = square distance between origin and x0y0 = x0^2 + y0^2
    b^2 = square distance between x0y0 and x1y1 = (x1-x0)^2 + (y1-y0)^2
    c^2 = square distance between origin and x1y1 = x1^2 + y1^2
    plug them together and simplify...
    x0^2 + y0^2 - x1*x0 - y1*y0 = 0
    """
    x0,y0 = p0
    x1,y1 = p1
    return x0**2 + y0**2 - x1*x0 - y1*y0 == 0
    
def distance(v):
    #calculate vector distance
    return (v[0]**2+v[1]**2)**0.5

from itertools import combinations, product

total = 0
for c in combinations(product(range(50+1),repeat=2), 3):
    if c[0] != (0,0):
        break
#     if is_rightangle(*c):
        total += 1

print "ans:", total
#14234
print time() - st