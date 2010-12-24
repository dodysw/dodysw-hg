from time import time
st = time()



def try1():
    limit = 10000000
    m = [0] * limit
    m[85] = m[89] = m[145] = m[42] = m[20] = m[4] = m[16] = m[37] = m[58] = 89
    m[44] = m[32] = m[13] = m[10] = m[1] = 1
    
    is89 = 0
    for i in xrange(1,limit):
        if m[i] == 0:
            #solve first
            found_set = set()
            add = found_set.add
            n = i
            while True:
                add(n)
                digits = map(int, str(n))
                n = 0
                for digit in digits:
                    n += digit*digit
                if m[n] in (89,1):
                    n = m[n]
                    break
            for s in found_set:
                m[s] = n
    
        if m[i] == 89:
            is89 += 1
        if i % 100000 == 0:
            print i, is89
    
    print "ans:", is89

def try2():
    limit = 10000000
    #optimization (Nikopol)
    #max num is 9999999 => 9**2 * 7 = 567, so let's simply make 567 array, and solve it
    is89 = 0
    m = [0] * (567+1)
    m[85] = m[89] = m[145] = m[42] = m[20] = m[4] = m[16] = m[37] = m[58] = 89
    m[44] = m[32] = m[13] = m[10] = m[1] = 1

    for i in xrange(1,568):
        total = i
        while total not in (89,1):
            digits = map(int, str(total))
            total = 0
            for digit in digits:
                total += digit*digit
        m[i] = total
        if total == 89:
            is89 += 1
    
    #then solve it
    for i in xrange(568,limit):
    
#         total = 0
#         for digit in map(int, str(i)):
#             total += digit*digit

        #optimization by Togra
        while total != 1 and total != 89:
            n = total
            total = 0
            while n:
                total += (n % 10)**2
                n /= 10

        if m[total] == 89:
            is89 += 1
        if i % 100000 == 0:
            print i, is89
    
    print "ans:", is89

try2()

print time() - st