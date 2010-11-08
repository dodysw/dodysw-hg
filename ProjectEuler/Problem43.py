"""
The number, 1406357289, is a 0 to 9 pandigital number because it is made up of each of the digits 0 to 9 in some order, but it also has a rather interesting sub-string divisibility property.

Let d_(1) be the 1^(st) digit, d_(2) be the 2^(nd) digit, and so on. In this way, we note the following:

    * d_(2)d_(3)d_(4)=406 is divisible by 2
    * d_(3)d_(4)d_(5)=063 is divisible by 3
    * d_(4)d_(5)d_(6)=635 is divisible by 5
    * d_(5)d_(6)d_(7)=357 is divisible by 7
    * d_(6)d_(7)d_(8)=572 is divisible by 11
    * d_(7)d_(8)d_(9)=728 is divisible by 13
    * d_(8)d_(9)d_(10)=289 is divisible by 17

Find the sum of all 0 to 9 pandigital numbers with this property.

"""

basepermutation = "0123456789"
def genpermutation(c, prev=""):
    if len(c) == 2:
        yield "%s%s%s" % (prev, c[0], c[1])
        yield  "%s%s%s" % (prev, c[1], c[0])
    else:
        for n in xrange(len(c)):
            for permutenum in genpermutation(c[1:], prev + c[0]):
                yield permutenum
            if n+1 == len(c):
                break
            #swap position
            c[0], c[n+1] = c[n+1], c[0]
            
divcheck = [2,3,5,7,11,13,17]
results = []
for n in genpermutation(list(basepermutation)):
    if n.startswith('0'):
        continue
    #print n
    all_divisible = True
    for i, div in enumerate(divcheck):
        check_n = int(n[i+1:i+4])
        if check_n % div != 0:
            all_divisible = False
            #print "%s/%s = FALSE" % (check_n, div)
            break
        #print "%s/%s = ok" % (check_n, div)
    if all_divisible:
        print n
        results.append(int(n))
        
print results
print sum(results)
            