def convergent(n):
    print "sqrt(%d) = %s" % (n,n**0.5)
    num = int(n**0.5)+n
    den = n*int(n**0.5)
    for l in xrange(10):
        print "%d/%d = %s" % (num,den, num/float(den))
        num, den = n*den+num, den+num

convergent(23)