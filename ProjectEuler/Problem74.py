import time, math
st = time.time()

def try1():
    #cache result of 1 digit factorial
    factorials = [math.factorial(n) for n in xrange(10)]
    #cache sumfact
    sumfacts = [0] * 3000000
    
    count = 0
    for n in xrange(1,1000000):
        sum_factorials = set()
        add = sum_factorials.add
        sum_factorial = n
        while sum_factorial not in sum_factorials:
            add(sum_factorial)        
            if sumfacts[sum_factorial] == 0:
                sumfacts[sum_factorial] = sum((factorials[i] for i in map(int, str(sum_factorial))))
            sum_factorial = sumfacts[sum_factorial]
        lensum = len(sum_factorials)
        if lensum == 60:
            count += 1
        
    print "ans:", count

def try2():
    #cache result of 1 digit factorial
    factorials = [math.factorial(n) for n in xrange(10)]
    #cache sumfact
    sumfacts = {}
    
    #reduce permutations to its essential number, but record actual count of numbers that it represents
    uniquedigits = {}
    join = "".join
    for n in xrange(1,1000000):
        o = join(sorted(str(n)))
        uniquedigits.setdefault(o, 0)
        uniquedigits[o] += 1
    
    count = 0
    for n in uniquedigits.keys():
        sum_factorials = set()
        add = sum_factorials.add
        sum_factorial = n
        while sum_factorial not in sum_factorials:
            add(sum_factorial)
            if sum_factorial not in sumfacts:
                sumfacts[sum_factorial] = join(sorted(str(sum((factorials[i] for i in map(int, sum_factorial))))))
            sum_factorial = sumfacts[sum_factorial]
        lensum = len(sum_factorials)
        if lensum == 60:
            print n
            count += uniquedigits[n]
        
    print "ans:", count
    
try2()

print time.time() - st