"""
The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, is unusual in two ways: (i) each of the three terms are prime, and, (ii) each of the 4-digit numbers are permutations of one another.
There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property, but there is one other 4-digit increasing sequence.
What 12-digit number do you form by concatenating the three terms in this sequence?
"""
#build primes up to 9999 (4-digits)
limit = 9999+1
is_prime = [True] * limit
for i in xrange(2,int(limit**0.5)):
	if is_prime[i]:
		for j in xrange(2*i, limit, i):
			is_prime[j] = False
#get the first 4 digit primes
primes = [i for i in xrange(1000,limit) if is_prime[i]]

def slow():
	#brute force, number of loops: p_count*(pcount-1)*(pcount-2)
	p_count = len(primes)
	for i in xrange(p_count):
	 for j in xrange(i+1, p_count):
		 for k in xrange(j+1, p_count):
			 if primes[k] != (2*primes[j] - primes[i]):
				 continue
			 i_temp = list(str(primes[i]))
			 j_temp = list(str(primes[j]))
			 k_temp = list(str(primes[k]))
			 i_temp.sort()
			 j_temp.sort()
			 k_temp.sort()
			 if i_temp == j_temp == k_temp:
				 i_temp = str(primes[i])
				 j_temp = str(primes[j])
				 k_temp = str(primes[k])
	
				 print "Found:",i_temp, j_temp, k_temp
				 #print "Answer: %s%s%s" % (i_temp, j_temp, k_temp)

def faster():
	#still brute force, but reduced. By avoiding unnecessary loop by checking p3 based on p2-p1 delta.
	p_count = len(primes)
	for i in xrange(p_count):
		for j in xrange(i+1, p_count):
			prime_k = 2*primes[j] - primes[i]
			if prime_k > 9999:
				break
			if not is_prime[prime_k]:
				continue
			i_temp = list(str(primes[i]))
			j_temp = list(str(primes[j]))
			k_temp = list(str(prime_k))
			i_temp.sort()
			j_temp.sort()
			k_temp.sort()
			if i_temp == j_temp == k_temp:
				i_temp = str(primes[i])
				j_temp = str(primes[j])
				k_temp = str(prime_k)			
				print "Found:",i_temp, j_temp, k_temp

faster()