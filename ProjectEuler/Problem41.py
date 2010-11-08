"""
We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and is also prime.

What is the largest n-digit pandigital prime that exists?
"""
def is_prime(n):
    for t in xrange(2, int(n**0.5)+1):
        if n % t == 0:
            return False
    return True

basepermutation = "123456789"
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

#my strategy is to generate all permutation of 1 to 9, starting the length of 9 (maximum of pandigits) up to 2.
#the advantage is we don't need to check whether the generated number is pandigital, since the permution implies that only one of the selected digit will appear

last_result = 0
for lendigits in xrange(9,1,-1):
    for n in genpermutation(list(basepermutation[:lendigits])):
        m = int(n)
        if is_prime(m) and m > last_result:
            last_result = m

print last_result