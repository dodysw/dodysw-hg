"""
2/1, 3/1, 8/3, 11/4, 19/7, 87/32, 106/39, 193/71
n2 = n1*d0+n0
106 = 87*7+19

"""

#http://en.wikipedia.org/wiki/Euler%27s_continued_fraction_formula
def e_convergent(n):
    print "sqrt(%d) = %s" % (n,n**0.5)
    num = int(n**0.5)+n
    den = n*int(n**0.5)
    for l in xrange(10):
        print "%d/%d = %s" % (num,den, num/float(den))
        num, den = n*den+num, den+num

convergent(23)