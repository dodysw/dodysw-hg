def divisor_count(n):
    """Count number of divisors. Used on problem 12, 179.
    """
    divcount = 0
    tmax = n**0.5
    for t in xrange(1, int(tmax+1)):
        if n % t == 0:
            print t, n/t
            divcount += 2
    if t == tmax:
        divcount -= 1
    return divcount

def divisor_count_up_to(limit):
    """Count number of divisors. Used on problem 12, 179.
    divide n by primes (p), the number of divisors is sum of 2xnumber of divisior of the result
    """
    assert limit > 3
    #we need primes up to (limit**0.5 / 2.0)
    plimit = int(limit**0.5)
    is_prime = [True] * plimit
    for i in xrange(2,int(plimit**0.5)):
        if is_prime[i]:
            for j in xrange(2*i, plimit, i):
                is_prime[j] = False
    primes = [i for i in xrange(2,plimit) if is_prime[i]]

    #prepare cache of divisors
    divs = [-1000000] * (limit+1)
    #initialize with known numbers
    divs[1] = 1
    divs[2] = 2
    divs[3] = 2
    totals = 5
    for i in xrange(4,limit+1):
        total = 2
        checklimit = int(i**0.5/2)
        print i,"cl",checklimit
        for prime in primes:
            a,b = divmod(i, prime)
            print "ab", a,b
            if b == 0:
                total += divs[a]
                if a == prime:
                    total -= 1
            if prime > checklimit:
                break
        totals += total
        divs[i] = total
        assert total == divisor_count(i), "%d: %d should be %d" % (i, total, divisor_count(i))
        print "==",i,total

    return totals

# total = divisor_count_up_to(20)
# print "Total:", total

def divisor_count_up_to2(limit):
    divs = [2] * (limit+1)
    divs[1] = 1 #just for completion, not used
    for i in xrange(2,int((limit+1)/2)):
        for j in xrange(2*i, (limit+1), i):
            divs[j] += 1
    total = 0
    for n in xrange(2,limit):
        if divs[n] == divs[n+1]:
#             print n,'and',n+1,'has same divisors',divs[n]
            total += 1
    return total
    
# total = 0
# dc0 = None
# for n in xrange(2,10**7):
#     if n % 100000 == 0:
#         print n
#     dc1 = divisor_count(n)
#     if dc1 == dc0:
#         total += 1
#     dc0 = dc1
    
print "ans:", divisor_count_up_to2(10**7)