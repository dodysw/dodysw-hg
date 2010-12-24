"""
For equilateral triangle with side a
Area = a*a*0.25*3**0.5
Perimeter = 3a

For triangle with 2 equal side (Isosceles)
http://mathworld.wolfram.com/IsoscelesTriangle.html
If b is the equal side, and a is the different one:
Area = 0.5 * a**2 * (b**2/a**2 - 0.25)**0.5

this is also called heronian triangle
http://en.wikipedia.org/wiki/Heronian_triangle

"""
from time import time
st = time()

def try1():
    limit = 1000000000
    p = total = 0
    for b in xrange(2,limit/3 + 1):
        a1 = 0.5*b-0.5
        a2 = a1 + 1
        for a_2 in (a1, a2):
            if a_2*(b*b - a_2*a_2)**0.5 % 1 == 0:
                print b,b,int(a_2 + a_2), "|",(b*b - a_2*a_2)**0.5, a_2, "=", a_2*(b*b - a_2*a_2)**0.5,"??",a_2*a_2*(b*b - a_2*a_2) % 0.5
                p = int(b+b+a_2+a_2)
                total += p
    return total
                
def try2():
    limit = 1000000000
    p = total = 0
    for n in xrange(3,limit):
#         A1 = ((1.5*n-0.5)*(0.5*n-0.5)**2*(0.5*n-1.5))**0.5
        A1 = (n-1)*(3*n*n-n)**0.5 % 4
#         A2 = ((1.5*n+0.5)*(0.5*n+0.5)**2*(0.5*n+1.5))**0.5  #n+1
        A2 = ((3*n+1)*(n+1)*(n+1)*(n-1))**0.5 % 4  #n+1
        if A1 == 0:
            print n, n, n-1, A1
#         if A2 == 0:
#             print n, n, n+1, A2
#         if A1 % 1 == 0 or A2 % 1 == 0:
#             print n, n, n-1, A1
#         if A2 % 1 == 0:
#             print n, n, n+1, A2
                
def try3():
    for m in xrange(5):
        for n in xrange(5):
            for k in xrange(5):
                a = n*(m**2 + k**2)
                b = m*(n**2 + k**2)
                c = (m+n)*(m*n - k**2)
                if a % 1 == 0 and b % 1 == 0 and c % 1 == 0 and a > 0 and b > 0 and c > 0:
                    print a,b,c, "at", m,n,k
                    
def isosceles_area(a,b):
    return 0.5 * a * a * ((b*b)/(a*a) - 0.25)**0.5

def try4():
    """
    A = (s(s-a)(s-b)(s-c))**0.5
    s = (a+b+c)/2
    
    for n+1:
        a = b = n
        c = n+1
        s = (3n+1)/2
        s-a = s-b = (n+1)/2
        s-c = (n-1)/2
        A = sqrt((3n+1)(n+1)^2(n-1)/16) = sqrt((3n+1)(n+1)^2(n-1))/4
          = (n+1)sqrt((3n+1)(n-1))/4
    Note: for A to be integer, (3n+1)(n-1) must be a square, and (n+1)sqrt((3n+1)(n-1)) divisible by 16
    for n-1:
        a = b = n
        c = n-1
        s = (3n-1)/2
        s-a = s-b = (n-1)/2
        s-c = (n+1)/2
        A = (n-1)sqrt((3n-1)(n+1))/4
    Note: for A to be integer, (3n-1)(n+1) must be a square, and (n-1)sqrt((3n-1)(n+1)) divisible by 4
    """

    total_perim = 0
    limit = 1000000000
    
    #for n+1
    n = 2
    while True:
        o = ((3*n+1)*(n-1))**0.5
        o2 = o*(n+1)
        if o % 1 == 0 and o2 % 4 == 0:
            p = n+n+n+1
            if p > limit:
                break
            print n, n, n+1, o
            total_perim += p
        
        o = ((3*n-1)*(n+1))**0.5
        o2 = o*(n-1)
        if o % 1 == 0 and o2 % 4 == 0:
            p = n+n+n-1
            if p > limit:
                break
            print n, n, n-1, o
            total_perim += p
        n += 1
    print "ans:", total_perim
            
                
try4()

print time() - st