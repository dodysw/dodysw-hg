"""
The prime 41, can be written as the sum of six consecutive primes:
41 = 2 + 3 + 5 + 7 + 11 + 13

This is the longest sum of consecutive primes that adds to a prime below one-hundred.

The longest sum of consecutive primes below one-thousand that adds to a prime, contains 21 terms, and is equal to 953.

Which prime, below one-million, can be written as the sum of the most consecutive primes?
"""
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
    
def sieve(n):
	#Create a list of consecutive integers from two to n: (2, 3, 4, ..., n).
	candidates = range(n+1)
	#Initially, let p equal 2, the first prime number. --> Repeat until p^2 is greater than n. ==> p > sqrt(n), or while p <= sqrt(n)
	p = 2
	final = int(n**0.5)
	while p <= final:
		#Find the first number remaining on the list after p (this number is the next prime); replace p with this number.
		if not candidates[p]:
			p += 1
			continue
		#Strike from the list all multiples of p less than or equal to n. (2p, 3p, 4p, etc.)
		for k in xrange(2*p, n+1, p):
			candidates[k] = None
		
		p += 1
	#All the remaining numbers in the list are prime.	
	return [i for i in candidates[2:] if i]	




def try1():
	#generate 1 million primes
	primes = sieve(1000000)
	prime_len = len(primes)

	#start from beginning, add until >1 million, count how  many prime
	results = []
	last_max_count = 0
	for i in xrange(prime_len-1,0,-1):
		if i % 100 == 0: print "Prime:",primes[i] 
		for j in xrange(0,i):
			psum = 0
			pcount = 0
			for k in xrange(j,prime_len):
				if (psum + primes[k]) > primes[i]:
					#print "Max sum", psum, "j/k", j, k
					break
				psum += primes[k]
				pcount += 1
				if psum == primes[i]:
					#found!
					#print "Found", psum, "j/k", j, k, "Count", pcount
					results.append([pcount, primes[i], j, k])
					if last_max_count < pcount:
						last_max_count = pcount
						prime_max = primes[i]
						print "Prime %s has %s consecutive primes" % (prime_max, last_max_count)
					break
				
def try2():

	# this is better if we need to generate prime AND check if number is prime
	limit = 1000000
	is_prime = [True] * limit
	for i in xrange(2,int(limit**0.5)):
		if is_prime[i]:
			for j in xrange(2*i, limit, i):
				is_prime[j] = False
	primes = [i for i in xrange(2,limit) if is_prime[i]]
	prime_len = len(primes)
	max_prime = primes[-1]
	max_pcount = 0
	for start in xrange(prime_len):
		psum = 0
		for i in xrange(start, prime_len):
			if (psum + primes[i]) > max_prime:
				break
			psum += primes[i]
 			if is_prime[psum]:
 				last_psum_prime = psum
 				last_pcount_prime = i-start-1
		if last_pcount_prime > max_pcount:
			max_pcount = last_pcount_prime
			max_prime = last_psum_prime
			print "Prime %s has %s consecutive primes" % (max_prime, max_pcount)
			
try2()
			
			