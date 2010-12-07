from time import time
st = time()

#http://en.wikipedia.org/wiki/Methods_of_computing_square_roots
#continued fraction expansion
def cfe(S, limit=500):
    m, d = 0, 1
    a0 = a = int(S**0.5)
    seq = []
    append = seq.append
    for l in xrange(limit):
        m = d*a-m
        d = (S-m*m)/d
        a = (a0+m)/d
        append(a)
    return seq

def period(seq):
    #detect lengths of periodicity of a list of numbers
    seq_length = len(seq)
    candidate = []
    for s in xrange(1,seq_length/2 + 1):
        test = seq[:s]
        if test * (seq_length/s) == seq[:seq_length - seq_length%s]:
            candidate = test
            break
    return len(candidate)

def try1():
    odd_period_count = 0
    for n in xrange(2,10000+1):
        if not (n**0.5) % 1: continue
        cf = cfe(n)
        period_len = period(cf)
        #print n,cf,period_len
        #assert period_len != 0, "period 0 for n=%d. Seq:%s" % (n,cf)
        if period_len % 2 != 0:
            odd_period_count += 1
    print "ans:", odd_period_count
    
try1()
print time() - st