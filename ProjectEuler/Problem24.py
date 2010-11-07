"""
0123456789, 0->1
0123456798, 0->2
0123456879, 0->1
0123456897, 2->0
0123456978, 0->1
0123456987,

"""

basepermutation = "0123456789"
#basepermutation = "abcd" #-> abc, acb, bac, bca, cab, cba

def genpermutation(c, prev=""):
    if len(c) == 2:
        yield "%s%s%s" % (prev, c[0], c[1])
        yield  "%s%s%s" % (prev, c[1], c[0])
    else:
        for n in xrange(len(c)):
            for permutenum in genpermutation(c[1:], prev + c[0]):
                yield permutenum
            if n+1 == len(c):
                break
            #swap position
            c[0], c[n+1] = c[n+1], c[0]

count = 0    
for permutenum in genpermutation(list(basepermutation)):
    count += 1
    if count >= 1000000:
        print count, permutenum
        break