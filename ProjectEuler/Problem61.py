import sys, time

def is_pentagonal(y):
    x = (0.5 + (0.25+6*y)**0.5)/3
    return x % 1 == 0

def is_triangle(t):
    t = -0.5 + (0.25+2*t)**0.5
    return t % 1 == 0

def is_square(t):
    t **= 0.5
    return t % 1 == 0

def is_hexagonal(h):
    h = 0.25 + ((1 + 8*h)**0.5)/4
    return h % 1 == 0

def is_heptagonal(h):
    h = 0.3 + ((2.25 + 10*h)**0.5)/5
    return h % 1 == 0

def is_octagonal(o):
    o = (2 + (4 + 12*o)**0.5)/6
    return o % 1 == 0

methods = is_square, is_triangle, is_pentagonal, is_hexagonal, is_heptagonal, is_octagonal

#build list of numbers on each method, then try combining them, look for cycling
method_numbers  = [None]*len(methods)
for i,method in enumerate(methods):
    method_numbers[i] = [[n/100, n%100] for n in xrange(1010,10000) if method(n) and (n % 100) > 9]

def nextelements(lists, m, prev_tail):
    my_head = prev_tail
    my_tails = [x[1] for x in lists[m] if x[0] == my_head]
    #print "-"*m, my_head,my_tails
    if m == 6 and len(my_tails):
        return [1]
    for tail in my_tails:
        next = nextelements(lists, m+1, tail)
        if next:
            return [my_head*100+tail] + next

def permutationNorepeat(c, prev=[]):
    """Generate len(<c>) length permutation of a list of characters with no repetition.
    The number of result is always factorial(len(<c>))
    E.g.: abc -> abc, acb, bac, bca, cba, cab    
    """
    assert(len(c) > 1)
    if len(c) == 2:
        yield prev + [c[0]] + [c[1]]
        yield prev + [c[1]] + [c[0]]
    else:
        for n in xrange(len(c)):
            for permutenum in permutationNorepeat(c[1:], prev + [c[0]]):
                yield permutenum
            if (n+1) < len(c):
                c[0], c[n+1] = c[n+1], c[0]

for lists in permutationNorepeat(method_numbers):
    lists.append(0)
    for head,tail in lists[0]:
        lists[6] = [[head,tail]]
        ans = nextelements(lists, 0,head)
        if ans:
            print sum(ans[:-1])
            sys.exit()