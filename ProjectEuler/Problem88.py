import time
st = time.time()

limit = 12500+1
is_prime = [True] * limit
for i in xrange(2,int(limit**0.5)):
    if is_prime[i]:
        for j in xrange(2*i, limit, i):
            is_prime[j] = False
#primes = [i for i in xrange(2,limit) if is_prime[i]]

def factors(n):
    #generate all possible unique factors of a number
    f = set()
    add = f.add
    for i in xrange(2, n/2 + 1):
        a,b = divmod(n,i)
        if b == 0:
            add(i)
            add(a)
    return f


def factors_mult(n, prev=[]):
    #generate all possible multiplication that lead to n
    #note: 1 is excluded since it does not affect the result
    i = 2 if not prev else prev[-1]
    while i <= n:
        a,b = divmod(n,i)
        if b == 0:
            if a == 1:
                #done. now calculate how many numbers (k) does this factors will need to sum to product-sum.
                global ks, product_sum
                sum_num = sum(prev + [i])
                k = (product_sum - sum_num) + len(prev) + 1
                #check if there's already smaller one
                ks[k] = min(product_sum, ks[k])
                return
            else:
                factors_mult(a, prev + [i])
        i += 1
        
ks = [100000] * 12500 #add a bit more because to get at least 12000 numbers, the worst case is 1++1...12k times...then a number like 12200
for product_sum in xrange(4, 12500+1):
    if is_prime[product_sum]:
        #no product-sum is prime because the mult is always 2 char. Proof: 1x61 != 1+61
        continue
    factors_mult(product_sum)

print "ans:", sum(set(ks[2:12000+1]))
#7587457
print time.time() - st