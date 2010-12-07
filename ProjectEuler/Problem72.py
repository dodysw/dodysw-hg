import time, math
st = time.time()
#formula to get HCF http://en.wikipedia.org/wiki/Greatest_common_divisor
# also http://en.wikipedia.org/wiki/Euclidean_algorithm
def hcf(a,b):
	while b != 0:
		a, b = b, a % b
	return a

#inspired by Pier at http://projecteuler.net/index.php?section=forum&id=73
#modified according to http://en.wikipedia.org/wiki/Stern%E2%80%93Brocot_tree
def arbol(n1, d1, n2, d2):
	global limit, arbolcount
	ad = d1+d2
	if ad > limit:
		return
	an = n1+n2
	#go through tree (left side) until denominator is 12k
	arbol(n1, d1, an, ad)
	#go through tree (right side) until denominator is 12k
	arbol(an, ad, n2, d2)
	arbolcount += 1
	
#From http://en.wikipedia.org/wiki/Farey_sequence
#Modified to fit into problem
def farey(n):
	"""Python function to print the nth Farey sequence, either ascending or descending."""
	a, b, c, d = 0,1,1,n	 # (*)
	count = 1
	#print "%d/%d" % (a,b),
	while c <= n:
		k = (n + b)/d
# 		a, b, c, d = c, d, k*c - a, k*d - b
		a1 = c
		b1 = d
		c = k*c - a
		d = k*d - b
		a = a1
		b = b1
		count += 1
		#print "%d/%d" % (a,b),
	return count
	
	
limit = 1500000
is_prime = [True] * limit
for i in xrange(2,int(limit**0.5)):
    if is_prime[i]:
        for j in xrange(2*i, limit, i):
            is_prime[j] = False

primes = [i for i in xrange(2,limit) if is_prime[i]]

def totient(n):
    """
    http://en.wikipedia.org/wiki/Euler%27s_totient_function
    t(n) = n*(1 - 1/p1)*(1 - 1/p2).... where pn is distinct prime factors of n
    """
    #find prime factors. assuming there's a table of "primes"
    nt = n
    factors = set()
    add = factors.add
    i = 0
    while nt > 1:
        if is_prime[nt]:
            add(nt)
            break
        p = primes[i]
        if nt % p == 0:
            add(p)
            nt /= p
        else:
            i += 1

    for p in factors:
        n *= 1 - 1.0/p

    return n
	
def farey_seqlength(n):
    #Fn = 1 + sum(totient(1..n))
    totient_total = 0
    for i in xrange(1,n+1):
        totient_total += int(totient(i))

    return totient_total + 1
	
def try1():
	limit = 8
	count = 0
	missed = 0
	ceil = math.ceil
	for d in xrange(2,limit+1):
		for n in xrange(1, d):
			if hcf(n, d) == 1:
				count += 1
			else:
				print n,'/',d
				missed += 1
	print "ans:",count, "missed", missed

def try2():
	global limit, arbolcount
	arbolcount = 0
	limit = 7
	import sys
	sys.setrecursionlimit(limit+2)
	arbol(0,1,1,1)
	print "ans:", arbolcount
	# arbol(0,1,1,0)
	
def try3():
#     for n in xrange(1,20):
# 	    print n, farey(n), farey_seqlength(n), totient(n)
  	print "ans:", farey_seqlength(1000000) - 2 # excluding first and last


def try4():
	"""By observation, 
	- total elements for n/d if n < d, excluding 0 and 1 is	 f(n) = n-1 + f(n-1) = 2(n-1) + f(n-2)	 7+6+5+4+3+2+1
	- if either denominator or numerator or both is prime, then it must be coprime
	- if one or both is not prime,	
	"""
	is_prime = [True] * limit
	for i in xrange(2,int(limit**0.5)):
		if is_prime[i]:
			for j in xrange(2*i, limit, i):
				is_prime[j] = False
	primes = [i for i in xrange(2,limit) if is_prime[i]]

try3()

print time.time() - st