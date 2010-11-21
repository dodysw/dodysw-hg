import sys
sys.setrecursionlimit(1001)

def sum_expanse(n1,n2):
    """a/b + c/d"""
    a,b = n1
    c,d = n2
    return a*d + b*c, b*d

def sum_iter(l=0):
    if l == 0:
        return 0,1
    a,b = sum_expanse([2,1],sum_iter(l-1))
    # 1/x
    return b,a

num_longer_than_denum = 0
for i in xrange(1000):
    num,denum = sum_expanse([1,1],sum_iter(i))
    if len(str(num)) > len(str(denum)):
        num_longer_than_denum += 1

print num_longer_than_denum