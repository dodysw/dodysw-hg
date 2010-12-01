#borrowed from solution Problem 78

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
        total += sign* p(k - gp)
        i += 1
    return total
    
# -1 since the problem excludes the 100 number itself
print "ans:", p(100) - 1