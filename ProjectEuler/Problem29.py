seq = {}
for a in xrange(2,101):
    for b in xrange(2,101):
        seq[a**b] = 1
print len(seq.keys())