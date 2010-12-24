from time import time
from itertools import permutations, product, count
from operator import add, sub, mul, truediv
st = time()

operators = add, sub, mul, truediv

def getnumset():
    for d in count(4):
        for c in xrange(3,d):
            for b in xrange(2,c):
                for a in xrange(1,b):
                    yield a,b,c,d
maxconlen = 0
maxnumset = None
ci = 0
for numset in getnumset():
#     print numset
    uniquesum = set()
    add = uniquesum.add
    t = 0
    for op in product(operators, repeat=3):
        +-* +*-
        +-/ + /-
        +*/ + /*
        -*/
        
        for num in permutations(numset):
            t += 1
            total = op[2](op[1](op[0](num[0], num[1]), num[2]), num[3])
            if total > 0 and total % 1 == 0:
                add(int(total))
    print t
    1/0
    #get consecutive length
    conlen = 0
    for i,n in enumerate(uniquesum):
        if n != i+1:
            conlen = i
            break

    if conlen > maxconlen:
        maxconlen = conlen
        maxnumset = numset
        print maxnumset,maxconlen

    ci += 1
#     if ci % 1000 == 0:
    if 1 in uniquesum:
        print numset, conlen, len(uniquesum)
# print "ans:", len(uniquesum), uniquesum,conlen
            