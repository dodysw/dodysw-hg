import math
def is_pentagonal(y):
    """
    y = x(3x-1)/2.
    y is the input, we need to find x, and whether it's an positive integer. Using quadratic equation, we convert to the following:
    
    x = (-b +- sqrt(b^2-4ac))/2a
    since y = x(3x-1)/2 is 1.5*x^2 - 0.5*x - y = 0, then a = 1.5, b = 0.5, c = -y
    x = (0.5 +- sqrt(0.25+6y)/3. Since x must be positive integer, then -1.5 must be added with positive number. so:
    x = (0.5 + sqrt(0.25+6y)/3

    """
    x = (0.5 + math.sqrt(0.25+6*y))/3
    if x % int(x) == 0:
    	return x
	return False
	
def is_triangle(t):
    """
    t = n(n+1)/2 => 0.5*n^2 + 0.5*n - t = 0
    x = -0.5 +- sqrt(0.25+2*t) / 1
      = -0.5 + sqrt(0.25+2*t)     
    """
    t = -0.5 + math.sqrt(0.25+2*t)
    return t % int(t) == 0

def is_hexagonal(h):
    """
    h = n(2n-1) => 2*n^2 - n - h = 0
    x = (1 +- sqrt(1 + 8*h)) / 4
      = 0.25 + sqrt(1 + 8*h)/4
    """
    h = 0.25 + math.sqrt(1 + 8*h)/4
    if h % int(h) == 0:
    	return h
   	return False
    
n = 1
while 1:
    T = n*(n+1)/2
    if is_hexagonal(T) and is_pentagonal(T):
        print "T(%s)=%s is hexagonal(%s) and pentagonal(%s)" % (n,T, is_hexagonal(T), is_pentagonal(T))
    n += 1