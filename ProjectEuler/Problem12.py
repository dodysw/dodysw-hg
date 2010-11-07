def triagen():
    n = i = 1
    while 1:
        yield i
        n += 1
        i += n
        
def divisor_count(n):
    return sum([1 for i in xrange(2,n/2) if n % i == 0]) + 2
        
for i in triagen():
    divnum = divisor_count(i)
    if divnum > 100:
        print i, divnum
    if  divnum > 500:
        print i
        break