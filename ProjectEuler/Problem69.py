"""
n/t(n) is maximum  when n is very big and t(n) is very small. 
since t(n) = n * (1 - (1/p1)) * (1 - (1/p2))..
n/t(n) ==> 1/ (1 - (1/p1)) * (1 - (1/p2))..
then 1 - (1/p1), or p1-1/p1 must be very small, thus happened when p1 is very small. See:
2 -> 0.5
3 -> 0.66
4 -> 0.75
AND, he more unique primes are there, the smaller, since it gets multiplied. 
So the smallest will have primes like 2,3,5,7,...
in short, the properties are:
-n must not be prime
-n must be even
-n must be composed of as many as smaller primes as possible. since 6 produce max, and it's composed
 of 2,3, and let's assume that the max also composed of at least 2,3, thus mod 2 and mod 3
"""

limit = 1500000
is_prime = [True] * limit
for i in xrange(2,int(limit**0.5)):
    if is_prime[i]:
        for j in xrange(2*i, limit, i):
            is_prime[j] = False

primes = [i for i in xrange(2,limit) if is_prime[i]]

def totient(n):
    """
    http://en.wikipedia.org/wiki/Euler%27s_totient_function
    t(n) = n*(1 - 1/p1)*(1 - 1/p2).... where pn is distinct prime factors of n
    """
    #find prime factors. assuming there's a table of "primes"
    nt = n
    factors = set()
    add = factors.add
    i = 0
    while nt > 1:
        if is_prime[nt]:
            add(nt)
            break
        p = primes[i]
        if nt % p == 0:
            add(p)
            nt /= p
        else:
            i += 1

    for p in factors:
        n *= 1 - 1.0/p

    return n


def try1():
    max_ratio = 0
    max_n = None
    for n in xrange(2,1000000+1):
        if n % 2 != 0 or n % 3 != 0 or is_prime[n]:
            continue
        ratio = n/totient(n)
        if ratio > max_ratio:
            max_ratio, max_n = ratio, n
            print "max", max_n, max_ratio
            
    print "ans",max_n, max_ratio
        
try1()