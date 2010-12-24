from time import time
st = time()

def revnum(n):
    #reverse number without converting to string (warning: slower than int(str(n)[::-1])
    m = 0
    while n > 0:
        n, r = divmod(n,10)
        m = 10*m + r
    return m
        
def naive(limit):
    total = 0
    for n in xrange(11,limit):
        if n % 10 == 0:
            continue
        rev = n + int(str(n)[::-1])
        #rev = n + revnum(n)
        
        is_all_odd = True
        while rev > 0:
            rev, r = divmod(rev,10)
            if r % 2 == 0:
                is_all_odd = False
                break

        if is_all_odd:
            total += 1

            
    return total
    
print naive(1000000000)
#608720
print time() - st