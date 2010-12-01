import time, sys
st = time.time()

"""
"""

def try1():
    #brute force try numbers, and match with keylog until all satisfied
    keys = dict.fromkeys(file("keylog.txt").read().split()).keys()
    #there's no 4 and 5, so it must be at least 8 digits
    n = 10000000-1
    while True:
        n += 1
        s = str(n)
        if '4' in s or '5' in s:
            continue
        try:
            idx = s.index
            for key in keys:
                idx(key[2],idx(key[1],idx(key[0])))
            print "Ans:", s
            break
        except ValueError:
            pass

def try2():
    """
    On each key, try to keep sequence match by moving digits in invalid position to the tail, then restart
    """
    #the minimum digit initially should contain all kind of digits in keylog.txt which is 0,1,2,3,6,7,8,9
    #so set it as initial guess
    guess = list("01236789")
    keys = list(set(file("keylog.txt").read().split()))
    i = 0
    while i < len(keys):
        #test
        key = keys[i]
        p = 0
        for n in (0,1,2):
            try:
                p = guess.index(key[n], p)
            except ValueError:
                guess.append(guess.pop(guess.index(key[n])))
                i = -1
                continue
        i += 1
    print "ans:", ''.join(guess)
    
#try1() # TOO LONG!
try2()

print >>sys.stderr, time.time() - st