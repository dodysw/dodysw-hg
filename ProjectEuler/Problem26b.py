def cycle(b):
    a = 10
    s = {}
    i = 0
    while (not s.has_key(a)):
        s[a] = i
        i += 1
        q = a/b
        r = a%b
        a = 10*r
        print q,r,a
    #print s
    return i-s[a]
 
t = {}
for d in range(983,984):
    f = cycle(d)
    if t.has_key(f):
        t[f].append(d)
    else:
        t[f]=[d]
#print t
m = max(t.keys())
print 'max=',m,'with',t[m]