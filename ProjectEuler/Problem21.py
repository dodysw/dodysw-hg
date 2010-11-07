#Let d(n) be defined as the sum of proper divisors of n (numbers less than n which divide evenly into n).
#If d(a) = b and d(b) = a, where a != b, then a and b are an amicable pair and each of a and b are called amicable numbers.
#For example, the proper divisors of 220 are 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 and 110; therefore d(220) = 284. The proper divisors of 284 are 1, 2, 4, 71 and 142; so d(284) = 220.
#Evaluate the sum of all the amicable numbers under 10000.

def proper_divisor(n):
    divisors = []
    t = 1
    while t <= n / 2:
        if n % t == 0:
            divisors.append(t)
        t += 1
    #print n, divisors
    return divisors
        
amicable_numbers = {}
for a in xrange(1,10000):
    if a in amicable_numbers:
        continue
    b = sum(proper_divisor(a))
    if a != b:
        is_a = sum(proper_divisor(b))
        if a == is_a:
            print "amic", a, b
            amicable_numbers[a] = 1
            if b < 10000:
                amicable_numbers[b] = 1 
        else:
            #print "notamic %s=>%s %s=>%s" % ( a, b, b, is_a)
            pass
print amicable_numbers.keys()
print sum(amicable_numbers.keys())