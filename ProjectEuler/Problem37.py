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
    
trunctable_primes = {}
i = 11
while 1:
    if is_prime(i):
    
        is_trunctable_prime = True    
        
        #from right
        p = i
        while p > 9:
            p /= 10
            if not is_prime(p):
                is_trunctable_prime = False
                break
        
        #from left
        if is_trunctable_prime:
            p = list(str(i))
            while len(p) > 0:
                p.pop(0)
                if not is_prime(int(''.join(p))):
                    is_trunctable_prime = False
                    break
    
        if is_trunctable_prime:
            print i
            trunctable_primes[i] = None
            if len(trunctable_primes) >= 11:
                break
        else:
            print "Not trunctable prime", i
            
    i += 1
            
print trunctable_primes.keys(), sum(trunctable_primes)
    
            