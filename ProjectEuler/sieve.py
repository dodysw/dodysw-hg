def sieve(n):
	#Create a list of consecutive integers from two to n: (2, 3, 4, ..., n).
	candidates = range(n+1)
	#Initially, let p equal 2, the first prime number. --> Repeat until p^2 is greater than n. ==> p > sqrt(n)
	for p in xrange(2, int(n**0.5) + 1):
		#Find the first number remaining on the list after p (this number is the next prime); replace p with this number.
		if not candidates[p]:
			continue
		#Strike from the list all multiples of p less than or equal to n. (2p, 3p, 4p, etc.)
		for k in xrange(2*p, n+1, p):
			candidates[k] = None
	return [i for i in candidates[2:] if i]
	
def sieve2(n):
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

def sieve_best(limit):
	# this is better if we need to generate prime AND check if number is prime
	global primes, is_prime
   is_prime = [True] * limit
   for i in xrange(2,int(limit**0.5)):
	   if is_prime[i]:
		   for j in xrange(2*i, limit, i):
			   is_prime[j] = False
   primes = [i for i in xrange(2,limit) if is_prime[i]]


import timeit
#print timeit.timeit("sieve(1000000)","from __main__ import sieve", number=5)
#print timeit.timeit("sieve2(1000000)","from __main__ import sieve_dody", number=5)
print timeit.timeit("sieve_best(1000000)","from __main__ import sieve_best", number=5)