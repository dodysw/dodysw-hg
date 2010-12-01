count = {}
for d in xrange(1,100):
    count[d] = 0
    for n in xrange(1,1000):
        digit_len = len(str(int(n**d)))
        if digit_len == d:
            count[d] += 1
        if digit_len > d:
            break
            
            
print sum(count.values())