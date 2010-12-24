import time
from bisect import bisect
st = time.time()

max_number = 50000000
#max prime would be the largest prime below (50M - 2**3+2**4)**0.5
max_prime = int((max_number - 2**3-2**4)**0.5)
#generate enough primes
#--------
limit = max_prime+1
is_prime = [True] * limit
for i in xrange(2,max(3,int(limit**0.5))):
    if is_prime[i]:
        for j in xrange(2*i, limit, i):
            is_prime[j] = False
primes = [i for i in xrange(2,limit) if is_prime[i]]
#--------
numbers = set()
add = numbers.add
a = 0
while a < len(primes):
    b = 0
    max_c = 1
    t = max_number - primes[a]**2
    while max_c >= 0:
        u = (t - primes[b]**3)
        if u <= 0:
            break
        a_and_b = max_number - u
        max_c = bisect(primes, u**0.25) - 1
        for k in xrange(max_c+1):
            add(a_and_b + primes[k]**4)
        b += 1
    a += 1
print "ans:", len(numbers)
#1097343
print time.time() - st