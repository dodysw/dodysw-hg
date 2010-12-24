"""
1x1 = 11
1x2 = 11,22,12
1x3 = 13.12,23,11,22,33
2z2 = 
3x2 = 1,2,3,4,5,6,12,23,45,56,123,456,14,25,36,1245,2356,123456
Algorithm for all size (w,h)
for each row, 1+2+3+4...w
multipled by height, 1+2+3+4...h
using wolfram, got the formula:
0.5n*(n+1)
so w*h = 0.5w*(w+1)*0.5h*(h+1) = 0.25*w*(w+1)*h*(h+1)
"""
target = 2000000
nearest = target
nearest_size = None
from itertools import count
for i in count(1):
    #icount = sum(range(i+1))
    for j in xrange(1,i+1):
        #count = icount*sum(range(j+1))
        count = 0.25*i*(i+1)*j*(j+1)
        if i > 2000:
            print "OVERLIMIT!", count, j
            1/0
        if target - 1000 < count < target + 10000:
            diff = abs(target - count)
            if diff < nearest:
                nearest = diff
                nearest_size = i,j
                print "New nearest:",i,j,"at",count,"area:",i*j

#2772