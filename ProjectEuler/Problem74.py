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
    
    #cache sum of (factorial's digits)
    sumfacts = {}
    
    #reduce permutations to its essential number, but record actual count of numbers that it represents
    uniquedigits = {}
    setdefault = uniquedigits.setdefault
    join = "".join
    for n in xrange(1,1000000):
        try:
            o = list(str(n))
            o.sort()
            o = join(o)
            uniquedigits[o] += 1
        except KeyError:
            uniquedigits[o] = 1
    
    #cache uniquedigits distance, bah only save 0.1sec
    distances = {}
    count = 0
    for n in uniquedigits.keys():
        sum_factorials = []
        add = sum_factorials.append
        sum_factorial = n
        while True:
            add(sum_factorial)
            if sum_factorial not in sumfacts:
                total = 0
                for i in map(int, sum_factorial):
                    total += factorials[i]
                total = list(str(total))                
                total.sort()
                sumfacts[sum_factorial] = join(total)
            sum_factorial = sumfacts[sum_factorial]
            if sum_factorial in distances:
                #cache found distance by adding current distance with the known distance of current summed factorials
                lensum = distances[n] = distances[sum_factorial] + len(sum_factorials)
                break
            if sum_factorial in sum_factorials:
                lensum = len(sum_factorials)
                #cache found recurrence's distance
                distances[sum_factorial] = lensum - sum_factorials.index(sum_factorial)
                break
        if lensum == 60:
            count += uniquedigits[n]
        
    print "ans:", count

try2()
print time.time() - st