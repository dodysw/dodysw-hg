import time
st = time.time()

limit = 10**7
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

    return int(n)

def try1():
    """
    observation from http://projecteuler.net/index.php?section=forum&id=70&page=2
    """
    
    print "Starting..."
    # ratio n/t(n) == n / n*reduce blabla = 1/((1 - 1/p)(1 - 1/p2)..). The minimum ratio is achieved
    # when p and p2 is as big as possible...
    min_ratio = 10
    min_n = -1
    # observation 1: n must NOT prime because if n is prime, t(n) is n - 1, if n-1 CANNOT be n permutation
    # observation 2:
    # since n cannot be prime, and ratio is minimized when p is as large as possible, then n must be composed of
    # 2 large unique primes (3 or more primes is not maximized)
    # so let's start from largest prime below sqrt(10**7) multiplied prime below it
    for n1 in xrange(1, len(primes)):
        for n2 in xrange(n1):
            n = primes[n1]*primes[n2]
            if n >= limit:
                break
            #we can calculate easily since n is composed of 2 primes
            #t = totient(n)
            #t = n*(1-1/p1)*(1-1/p2) = p1*p2*( (p1-1)/p1 )*( (p2 - 1)/p2 ) = (p1-1)*(p2-1) 
            #  = p1*p2 -p1 -p2 + 1 = n - p1 - p2 + 1
            t = n - primes[n1] - primes[n2] + 1
            
            # if n permutaion of t, the difference must be multiple of 9 (note: difference of 9 does not mean permutation, so we must check for sure below)
            if (n - t) % 9 != 0:
                continue
            ratio = n/float(t)
            if ratio < min_ratio:
                n_s = str(n)
                n_t = str(t)
                if len(n_s) == len(n_t):
                    n_l = list(n_s)
                    t_l = list(n_t)
                    n_l.sort()
                    t_l.sort()
                    if n_l == t_l:
                        print "%s/%s" % (n,t)
                        min_ratio = ratio
                        min_n = n
                        print "Min", min_ratio, "at", min_n
    print "ans:", min_n
    
try1()
# 8319823
# print totient(8319823)
print time.time() - st