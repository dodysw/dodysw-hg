def permutationNorepeat(c, prev=""):
    """Generate len(<c>) length permutation of a list of characters with no repetition.
    The number of result is always factorial(len(<c>))
    E.g.: abc -> abc, acb, bac, bca, cba, cab    
    """
    assert(len(c) > 1)
    if len(c) == 2:
        yield "%s%s%s" % (prev, c[0], c[1])
        yield  "%s%s%s" % (prev, c[1], c[0])
    else:
        for n in xrange(len(c)):
            for permutenum in permutationNorepeat(c[1:], prev + c[0]):
                yield permutenum
            if (n+1) < len(c):
                c[0], c[n+1] = c[n+1], c[0]

def permutationNorepeatSize(c, size=None, prev=""):
    """Generate fixed length permutation of a list of characters with no repetition.
    The number of result is always factorial(len(<c>)) / factorial(len(<c>) - <size>)
    E.g.: abc -> abc, acb, bac, bca, cba, cab    
    """
    assert(len(c) > 1)
    if size is None:
        size = len(c)
    if len(c) == 2:
        yield "%s%s%s" % (prev, c[0], c[1])
        yield  "%s%s%s" % (prev, c[1], c[0])
    else:
        for n in xrange(len(c)):
            for permutenum in permutationNorepeatSize(c[1:size], size-1, prev + c[0]):
                yield permutenum
            if (n+1) < len(c):
                c[0], c[n+1] = c[n+1], c[0]

            
def permutationSize(c, size=1, prev=""):
    """Generate <size> length permutation of a list of <c> characters, with repetition allowed.
    It's like rolling a dice <size> times. The number of result is always len(<c>)^size
    E.g.: abc 2 -> aa, ab, ac, ba, bb, bc, ca, cb, cc   
    """
    for n in xrange(len(c)):
        if size == 1:
            yield "%s%s" % (prev, c[n])
        else:
            for p in permutationSize(c, size-1, prev + c[n]):
                yield p

def permutationSizeList(c, size=1, prev=[]):
    """Generate <size> length permutation of a list of <c> characters, with repetition allowed.
    It's like rolling a dice <size> times. The number of result is always len(<c>)^size
    E.g.: abc 2 -> aa, ab, ac, ba, bb, bc, ca, cb, cc   
    """
    for n in xrange(len(c)):
        if size == 1:
            yield prev + [c[n]]
        else:
            for p in permutationSizeList(c, size-1, prev + [c[n]]):
                yield p

                
def permutationSize2(c, size=1, prev=""):
    """Similar to permutationSize, but without recursive
    """
    res = [0]*size
    done = False
    p = size - 1
    lenc = len(c)
    while not done:
        out = [c[x] for x in res] # this is slow!
        yield out
        res[p] += 1
        #overflow scan
        q = p
        while res[q] >= lenc:
            #overflow detected!
            if q == 0:
                #no more digit to carry over, time to quit
                done = True
                break
            else:
                res[q] = 0
                res[q-1] += 1
            q -= 1

if __name__ == '__main__':
     permutationSize2([0,1],5)
