limit = 500000
is_prime = [True] * limit
for i in xrange(2,int(limit**0.5)):
    if is_prime[i]:
        for j in xrange(2*i, limit, i):
            is_prime[j] = False
primes = [i for i in xrange(2,limit) if is_prime[i]]

def factors_slow(n):
    div = 2    
    res = []
    while div <= n:
        if n % div == 0:
            res.append(div)
            n /= div
        else:
            div += 1
    return res

def factors_fast(n):
    i = 0
    res = []
    while primes[i] <= n:
        prime = primes[i]
        if n % prime == 0:
            res.append(prime)
            n /= prime
        else:
            i += 1
    return res

import time

def try2():
    st = time.time()
    n = 2
    target = 0
    while target < 4:
        if len(set(factors_fast(n))) == 4:
            target += 1
        else:
            target = 0
        n += 1    
    print n - 4
    print time.time() - st

def try3():
    #4 block "homing"
    st = time.time()
    n = minimum_n = 2
    target = 0
    while target < 4:
        if len(set(factors_fast(n))) == 4:
#            print n
            target = 1
            #go back and forward
            minimum_n = n
            for direction in [-1,1]:
                for offset in xrange(1,4):
                    new_n = n+(direction*offset)
#                    print "--",new_n
                    if len(set(factors_fast(new_n))) == 4:
                        target += 1
                        minimum_n = min(minimum_n, new_n)
                    else:
                        break
        n += 4    
    print minimum_n
    print time.time() - st
    
try3()