limit = 100000
is_prime = [True] * limit
for i in xrange(2,int(limit**0.5)):
    if is_prime[i]:
        for j in xrange(2*i, limit, i):
            is_prime[j] = False
primes = [i for i in xrange(2,limit) if is_prime[i]]

def countPartitionPrimes(n, prev):
    total = 0
    for i in xrange(2, min(n, prev) +1):
        if not is_prime[i]:
            continue
        total += 1 if n-i == 0 else countPartitionPrimes(n-i, i) 
    return total

counts = 0
n = 2
while counts <= 5000:
    n += 1
    counts = countPartitionPrimes(n, n)
print "ans:", n