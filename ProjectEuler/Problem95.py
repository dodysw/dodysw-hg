
def sum_proper_divisors(n):
    d = 2
    total = 0
    a = n
    is_div = [False] * n
    for i in xrange(2,int(n**0.5)):
        if not is_div[i]:
            while a > 1:
                a, b = divmod(a,d)
                if b == 0:
                    total += d + a
                else:
                    d += 1
    return total
    
    
print sum_proper_divisors(28)
print sum_proper_divisors(220)