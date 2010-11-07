def fibo(max_count=0):
    n = 1
    p0 = 1
    p1 = 1
    yield p0
    while n < max_count or max_count == 0:
        yield p1
        p0, p1 = p1, p0 + p1
        n += 1
        
for i, num in enumerate(fibo()):
    if len(str(num)) >= 1000:
        print i+1, num
        break   