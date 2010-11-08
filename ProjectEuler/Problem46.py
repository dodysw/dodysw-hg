"""
Composite number is number that can be divided (whole number) by number other than 1 and itself.
9 =>3
15 => 3, 5
21 => 3, 7
25 => 5
27 => 3, 9
33 => 3, 11
pattern: odd composite number is always composed of odd numbers

"""
def odd_composite_number():
    n = 9 # first odd composite number
    while 1:
        for d in xrange(3,n/2+1,2):
            if n % d == 0:
                yield n
                break
        n += 2

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

import math
for n in odd_composite_number():
    conjecture = False
    print n
    #since odd composite number (n) = primenum + 2 * seq^2, then n - 2*seq^2 = primenum. since primenumber must be at least 3, 
    #n - 2*seq^2 >= 3 --> n-3 >= 2*seq^2 --> (n-3)/2 >= seq^2 --> sqrt(0.5*n-1.5) >= seq
    #or seq < sqrt(0.5*n-1.5)
    for seq in xrange(1,int(math.sqrt(0.5*n - 1.5)) + 1):
        if is_prime(n-2*seq*seq):
            print "%s = %s + 2*%s^2" % (n, n-2*seq*seq, seq)
            conjecture = True    
            break
    if conjecture == False:
        print "Found false conjecture:",n
        break