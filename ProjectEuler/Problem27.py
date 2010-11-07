
def is_prime(i):
    for t in range(2,int(i**0.5)+1):
        if i % t == 0:
            return False
    return True

max_consecutive = [0,None, None]
for a in xrange(-999, 1000):
    for b in xrange(-999, 1000):
        n = 0
        result_is_prime = True
        while result_is_prime:
            result = n*n + a*n + b
            if result < 0:
                break
            if not is_prime(result):
                break
            n += 1

        if n > max_consecutive[0]:
            max_consecutive = [n, a, b]
            
print max_consecutive
print max_consecutive[1] * max_consecutive[2]