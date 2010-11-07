"""
a/b
"""
fractions = [1,1]
for b in xrange(11,100):
    for a in xrange(10,b):
        if a % 10 == 0 and b % 10 == 0:
            #trivial
            continue
        c = float(a)/b
        # try removing 1 char
        sa, sb = str(a), str(b)
        for n in [0,1]:
            if sa[n] in sb:                
                new_a = int(sa[n ^ 1])
                #print sa, sb, n
                new_b = int(sb.replace(sa[n], "", 1))
                if new_b != 0 and float(new_a)/new_b == c:
                    fractions[0] *= new_a
                    fractions[1] *= new_b
                    print "%s / %s == %s / %s" % (new_a, new_b, a, b)
            
print fractions
        