"""
By replacing the 1^(st) digit of *3, it turns out that six of the nine
possible values: 13, 23, 43, 53, 73, and 83, are all prime. By replacing
the 3^(rd) and 4^(th) digits of 56**3 with the same digit, this 5-digit
number is the first example having seven primes among the ten generated
numbers, yielding the family: 56003, 56113, 56333, 56443, 56663, 56773,
and 56993. Consequently 56003, being the first member of this family, is
the smallest prime with this property. Find the smallest prime which, by
replacing part of the number (not necessarily adjacent digits) with the
same digit, is part of an eight prime value family.
"""
import sys, time

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


bench_start = time.time()

limit = 999999+1
is_prime = [True] * limit
for i in xrange(2,int(limit**0.5)):
    if is_prime[i]:
        for j in xrange(2*i, limit, i):
            is_prime[j] = False
            
def slow():
    done = False
    #get the first 4-6 digit primes
    for digit_length in xrange(4,6+1):
        #print digit_length, "digits"
        max_sequence = [0,0]
        primes = [i for i in xrange(10**(digit_length-1), 10**digit_length) if is_prime[i]]
        masks = list(permutationSizeList(['0','1'],digit_length))[1:-1]
        smallest_possible = 10**(digit_length-1)
        for prime in primes:
            #print "Prime:", prime
            for mask in masks:
                #print "Mask:", mask
                # define a starting point number based on current mask
                #. eg, prime is 1234, mask is -x-x (0,1,0,1)
                # get 1030
                starting_point = list(str(prime))
                for m in xrange(digit_length):
                    if mask[m] == '1':
                        starting_point[m] = '0'
                starting_point = int(''.join(starting_point))
                #print "Masked Prime:", starting_point
                adder = int(''.join(mask))
                
                #start counting the occurence of prime
                not_prime_count = 0
                moving_point = starting_point
                res = []
                for n in xrange(0,10):
                    # 8 occurance is the target, so if reach 3 false, consider it hopeless
                    if moving_point < smallest_possible or not is_prime[moving_point]:
                        not_prime_count += 1
                    else:
                        res.append(moving_point)
                    if not_prime_count > 2:
                        break
                    moving_point += adder
                if not_prime_count <= 2:
                    print "Mask is:", mask,"Res:",res, "Prime:", prime
                    print "Answer:", res[0]
                    done = True
                    break
            if done: break
        if done: break
        
def fast():
    """Ripped+inspired by bubblehead   (Python). Brilliant and simple.
    """
    #get the first 4-6 digit primes
    for num in xrange(1000,1000000+1):
        if not is_prime[num]:
            continue
        num = str(num)
        do_check = False
        for r in '012':
            if num.count(r):
                do_check = True
                break
        if not do_check:
            continue
        prime_candidates = []
        fail_count = 0
        for m in '0123456789':
            check_n = num.replace(r, m)
            if check_n[0] != '0' and is_prime[int(check_n)]:
                prime_candidates.append(check_n)
            else:
                fail_count += 1
            if fail_count > 2:
                break
        if fail_count <= 2:
            print "Answer:", prime_candidates[0]
            break
        
slow_start = time.time()
slow()
print "Slow:", time.time()-slow_start

fast_start = time.time()
fast()
print "Fast:", time.time()-fast_start
fast()

print time.time() - bench_start