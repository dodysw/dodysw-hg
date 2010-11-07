import math

prime_cache = {1: False}
def is_prime(i):
    if i in prime_cache:
        return prime_cache[i]
    for t in range(2,int(i**0.5)+1):
        if i % t == 0:
            prime_cache[i] = False
            return False
    prime_cache[i] = True
    return True

circular_primes = {}

for n in xrange(2,1000000):
    n_len = len(str(n))
    if n in circular_primes:
        continue
    if not is_prime(n):
        continue
    is_circular_prime = True
    for i in xrange(n_len):
        if not is_prime(n):
            is_circular_prime = False
        # rotate
        if n_len > 1:
            n = n % 10 * 10**int(math.log10(n)) + n / 10
    if is_circular_prime:
        circular_primes[n] = None
            
print circular_primes.keys(), len(circular_primes)