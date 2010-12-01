"""
1 = 1 -> 1
2 = 2, 1+1 -> 2
3 = 3, (2+1, 1+1+1) + 0 -> 3
4 = 4, 3+1, 2+2, 2+1+1, 1+1+1+1 -> 5
    4 +1
    (3) + 1 -> 
    (2)
    1
--- 4 = 4, (3, 2+1, 1+1+1) +1, 2+2,  -> 5
    
5 = 5, 4+1, 3+2, 3+1+1, 2+2+1, 2+1+1+1, 1+1+1+1+1 -> 7
-- 5, (4, (3, 2+1, 1+1+1) +1, 2+2) + 1, 3+2

6 = 6, 5+1, 4+2, 4+1+1, 3+3, 3+2+1, 3+1+1+1, 2+2+2, 2+2+1+1, 2+1+1+1+1, 1+1+1+1+1+1 ->11
--- 6, (5, 4+1, 3+2, 3+1+1, 2+2+1, 2+1+1+1, 1+1+1+1+1) +1, 4+2, 3+3, 2+2+2, ->11


7 = 
7, 6+1, 5+1+1, 5+2, 4+1+1+1, 4+2+1, 4+3, 3+1+1+1+1, 3+2+1+1, 3+2+2, 3+3+1, 2+1+1+1+1+1, 
2+2+1+1+1, 2+2+2+1, 1+1+1+1+1+1+1 -> 15

7, (6, (5, 4+1, 3+2, 3+1+1, 2+2+1, 2+1+1+1, 1+1+1+1+1) +1, 4+2, 3+3, 2+2+2) + 1 ,
5+2, 4+3, 3+2+2

7, 6+1, 5+2, 5+1+1, 4+3, 4+2+1, 4+1+1+1, 3+3+1, 3+2+2, 3+2+1+1, 3+1+1+1+1
2+2+2+1, 2+2+1+1+1, 2+1+1+1+1+1, 1+1+1+1+1+1+1


8 =
8, 7+1, 6+2, 6+1+1, 5+3, 5+2+1, 5+1+1+1, 4+4, 4+3+1, 4+2+2, 4+2+1+1, 4+1+1+1+1
3+3+2, 3+3+1+1, 3+2+2+1, 3+2+1+1+1, 3+1+1+1+1+1, 2+2+2+2, 2+2+2+1+1, 2+2+1+1+1+1, 
2+1+1+1+1+1, 1+1+1+1+1+1+1+1+1+1 -> 22


5 = 7
6 = 11
7 = 15
8 = 22
f(x) = 7 + 4*(x-5) 

6, 
5+1, 
4+2, 4+1+1, 
3+3, 3+2+1, 3+1+1+1, 
2+2+2, 2+2+1+1, 2+1+1+1+1, 
1+1+1+1+1+1 ->11


1/1/1/1/1
2/1/1/1
2/2/1
3/1/1
3/2
4/1
5

7
4->n = 3, 1->n = 2, 1 -> n = 1, 1

"""

import time

def t4(n, prev=[]):
    limit = n if not prev else prev[-1]
    for i in xrange(1,limit+1):
        print "level", len(prev), i
        if (sum(prev) + i) >= n:
            return prev + [i]
        ret = t4(n, prev + [i])
        if ret:
            print ret

def t5(n, prev=[]):
    if n == 0:
        print prev[1:]
        return 1
    else:
        total = 0
        for i in xrange(1, min(n,prev[-1])+1):
            total += t5(n-i, prev + [i]) 
        return total

def countPartition(n, prev=[]):
    #fuckin slow!
    total = 0
    for i in xrange(1, min(n,prev[-1])+1):
        total += 1 if n-i == 0 else countPartition(n-i, prev + [i]) 
    return total
    
#http://wiki.python.org/moin/PythonDecoratorLibrary
class memoized(object):
   """Decorator that caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned, and
   not re-evaluated.
   """
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      try:
         return self.cache[args]
      except KeyError:
         value = self.func(*args)
         self.cache[args] = value
         return value
      except TypeError:
         # uncachable -- for instance, passing a list as an argument.
         # Better to not cache than to blow up entirely.
         return self.func(*args)
   def __repr__(self):
      """Return the function's docstring."""
      return self.func.__doc__
   def __get__(self, obj, objtype):
      """Support instance methods."""
      return functools.partial(self.__call__, obj)

@memoized
def p_fuckingstillslow(k, n):
    """
    learned from:
    http://en.wikipedia.org/wiki/Partition_%28number_theory%29
    """
    if k > n:
        return 0
    elif k == n:
        return 1
    else:
        return (p(k+1, n) + p(k, n-k)) % 1000000

def try3():
    st = time.time()
    import sys
    sys.setrecursionlimit(100000)
    n = 0
    while True:
        n += 1
        counts = p(1, n) % 1000000
        if counts == 0:
            break
        print n, counts
    print "ans:", n
    print time.time() - st

def generalizedPentagonal(i):
    #for n running over positive and negative integers: successively taking n = 1, -1, 2, -2, 3, -3, 4, -4,
    n = (i+2)/2
    if i % 2 != 0:
        n *= -1
    #"generalized pentagonal numbers of the form 0.5*n(3n - 1)"
    return 0.5*n*(3*n-1)
    
@memoized
def p(k):
    """
    http://en.wikipedia.org/wiki/Partition_%28number_theory%29:
    ...in conjunction with the pentagonal number theorem to derive a recurrence for the partition function stating that:
    p(k) = p(k - 1) + p(k - 2) - p(k - 5) - p(k - 7) + p(k - 12) + p(k - 15) - p(k - 22) - ... 
    where the sum is taken over all generalized pentagonal numbers of the form 0.5*n(3n - 1), 
    for n running over positive and negative integers: successively taking n = 1, -1, 2, -2, 3, -3, 4, -4, ..., 
    generates the values 1, 2, 5, 7, 12, 15, 22, 26, 35, 40, 51, .... 
    The signs in the summation continue to alternate +, +, -, -, +, +, ...
    """
    #"By convention p(0) = 1, p(n) = 0 for n negative"
    if k == 0 or k == 1:
        return 1
    elif k < 0:
        return 0

    total = 0
    sign = 1
    gp = 1
    i = 0
    while (k - gp) > 0:
        #"The signs in the summation continue to alternate +, +, -, -, +, +, ..."
        sign = -1 if ((i+2)/2)  % 2 == 0 else 1
        gp = generalizedPentagonal(i)
        total += sign* (p(k - gp) % 1000000)
        i += 1
    return total

def try4():
    st = time.time()
    n = 0
    while True:
        n += 1
        counts = p(n)
        if counts % 1000000 == 0:
            break
    print "ans:", n
    print time.time() - st


#print p(55374)
try4()