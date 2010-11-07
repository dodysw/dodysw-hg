"""123456789
1*2=3456789
1234
1 * 2 = 34
1 * 23 = 4
12 * 3 = 4
3 * 4 = 12
4 * 3 = 12
4 * 3 = 21
"""
products = {}
for a in xrange(100,10000):
    #print "A", a
    for b in xrange(1,100):
        #print "B", b
        c = a*b
        abc = str(a) + str(b) + str(c)
        
        #print a,b,c        
        if len(abc) != 9:
            continue
        if '0' in abc:
            continue
        elif len(dict.fromkeys(abc)) != 9:
            continue
        #elif c % 9 != 0:
        #    continue        
        else:
            print "%s x %s = %s" % (a, b, c)
            products[c] = None
            
print sum(products)