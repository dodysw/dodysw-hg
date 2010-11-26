import time

limit = 10000
is_prime = [True] * limit
for i in xrange(2,int(limit**0.5)):
    if is_prime[i]:
        for j in xrange(2*i, limit, i):
            is_prime[j] = False
primes = [i for i in xrange(2,limit) if is_prime[i]]

L = len(primes)

class Found(Exception):pass

def is_prime_naive(i):
    #only 2 is even prime
    if i == 2:
        return 1
    if i % 2 == 0:
        return 0
    #skip even numbers
    for t in xrange(3, int(i**0.5)+1, 2):
        if i % t == 0:
            return 0
    return 1

def try1():
    try:
        for i1 in xrange(L):
            p1 = str(primes[i1])
            for i2 in xrange(i1+1,L):
                p2 = str(primes[i2])
                if not is_prime_naive(int(p1+p2)) or not is_prime_naive(int(p2+p1)):
                    continue
                #print "2 ok", p1,p2
                for i3 in xrange(i2+1,L):
                    p3 = str(primes[i3])
                    if (not is_prime_naive(int(p1+p3)) or not is_prime_naive(int(p3+p1)) or
                       not is_prime_naive(int(p2+p3)) or not is_prime_naive(int(p3+p2))):
                        continue
                    #print "3 ok", p1,p2,p3
                    for i4 in xrange(i3+1, L):
                        p4 = str(primes[i4])
                        if (not is_prime_naive(int(p1+p4)) or not is_prime_naive(int(p4+p1)) or
                           not is_prime_naive(int(p2+p4)) or not is_prime_naive(int(p4+p2)) or
                           not is_prime_naive(int(p3+p4)) or not is_prime_naive(int(p4+p3))):
                            continue
                        #print "4 ok", p1,p2,p3,p4
                        for i5 in xrange(i4+1, L):
                            p5 = str(primes[i5])
                            if (not is_prime_naive(int(p1+p5)) or not is_prime_naive(int(p5+p1)) or
                               not is_prime_naive(int(p2+p5)) or not is_prime_naive(int(p5+p2)) or
                               not is_prime_naive(int(p3+p5)) or not is_prime_naive(int(p5+p3)) or
                               not is_prime_naive(int(p4+p5)) or not is_prime_naive(int(p5+p4))):
                                continue
                            raise Found
    except Found:
#        print "Sum:",sum([primes[i] for i in (i1,i2,i3,i4)])
        ans_primes = [primes[i] for i in (i1,i2,i3,i4,i5)]
        print "Sum:",sum(ans_primes), "From", ans_primes

st = time.time()
try1()                        
print time.time() - st