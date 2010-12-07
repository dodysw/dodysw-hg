import time, math
st = time.time()
#formula to get HCF http://en.wikipedia.org/wiki/Greatest_common_divisor
# also http://en.wikipedia.org/wiki/Euclidean_algorithm
def hcf(a,b):
    while b != 0:
        a, b = b, a % b
    return a

#inspired by Pier at http://projecteuler.net/index.php?section=forum&id=73
#modified according to http://en.wikipedia.org/wiki/Stern%E2%80%93Brocot_tree
def arbol(n1, d1, n2, d2):
    global limit, arbolcount
    ad = d1+d2
    if ad > limit:
        return
    an = n1+n2
    #go through tree (left side) until denominator is 12k
    arbol(n1, d1, an, ad)
    #go through tree (right side) until denominator is 12k
    arbol(an, ad, n2, d2)
    arbolcount += 1
    
#From http://en.wikipedia.org/wiki/Farey_sequence
#Modified to fit into problem
def farey(n):
    """Python function to print the nth Farey sequence, either ascending or descending."""
    a, b, c, d = 0,1,1,n     # (*)
    count = 0
    begin_counting = False
    while (c < n):
        k = int((n + b)/d)
        a, b, c, d = c, d, k*c - a, k*d - b
        if a == 1 and b == 2:
            break
        if a == 1 and b == 3:
            begin_counting = True
        if begin_counting:
            count += 1
    return count - 1

    
def try1():
    limit = 12000
    count = 0
    ceil = math.ceil
    for d in xrange(2,limit+1):
        for n in xrange(d/3 + 1, int(ceil(d/2.0))):
            if hcf(n, d) == 1:
                count += 1
    print "ans:",count

def try2():
    global limit, arbolcount
    arbolcount = 0
    limit = 12000
    import sys
    sys.setrecursionlimit(limit)
    arbol(1,3,1,2)
    print "ans:", arbolcount
    # arbol(0,1,1,0)

def try3():
    limit = 12000
    print "ans:", farey(limit)

try3()

# 7295372
print time.time() - st