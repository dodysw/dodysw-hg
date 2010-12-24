
def fibo(n):
    f1, f2 = 1, 1
    if n == 1:
        return f1
    elif n == 2:
        return f2
    for i in xrange(3,n+1):
        f3 = f2 + f1
        f1, f2 = f2, f3
    return f3

correct_seq = map(str,range(1,10))    

i = 3
# f1, f2 = 1, 1
f1a, f2a, f1b, f2b = 1,1,1,1

while True:
#     if i % 100 == 0:
#         print i
    
#     f3 = f2 + f1
#     f1, f2 = f2, f3
    
    #left side
    f3a = f2a + f1a
    if f3a > 999999999:
        f3a /= 10.0
        f2a /= 10.0
    f1a, f2a = f2a, f3a
    
    #right side
    f3b = (f2b + f1b) % 1000000000
    f1b, f2b = f2b, f3b

    
    if sorted(str(f3b)) == correct_seq:
        if sorted(str(int(f3a))) == correct_seq:
            break
    i += 1
print "ans:",i