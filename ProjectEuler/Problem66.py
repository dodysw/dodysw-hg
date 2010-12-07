"""
x*x - D*y*y = 1
x*x = 1 + D*y*y
D*y*y = x*x - 1
y*y = (x*x - 1)/D
y = ((x*x - 1)/D)**0.5

http://en.wikipedia.org/wiki/Pell%27s_equation

"""
import time
st = time.time()

D_Raw = """2	3
3	2
5	9
6	5
7	8
8	3
10	19
11	10
12	7
13	649
14	15
15	4
17	33
18	17
19	170
20	9
21	55
22	197
23	24
24	5
26	51
27	26
28	127
29	9801
30	11
31	1520
32	17
33	23
34	35
35	6
37	73
38	37
39	25
40	19
41	2049
42	13
43	3482
44	199
45	161
46	24335
47	48
48	7
50	99
51	50
52	649
53	66249
54	485
55	89
56	15
57	151
58	19603
59	530
60	31
61	1766319049
62	63
63	8
65	129
66	65
67	48842
68	33
69	7775
70	251
71	3480
72	17
73	2281249
74	3699
75	26
76	57799
77	351
78	53
79	80
80	9
82	163
83	82
84	55
85	285769
86	10405
87	28
88	197
89	500001
90	19
91	1574
92	1151
93	12151
94	2143295
95	39
96	49
97	62809633
98	99
99	10
101	201
102	101
721	1915369156164159145737805889536""".split('\n')
xsols = dict([map(int, el.split("\t")) for el in D_Raw])

def chakravala(n):
    """
    http://en.wikipedia.org/wiki/Chakravala_method
    any triple x,y,z:
    x**2 - D*y**2 = k
    can be composed with trivial triple m, 1, m**2-D. Test: D=2, m = 3 -> 3, 1, 7
        3**2 - 2 = 7 -> YUP
    to get new triple: x*m + D*b, x + y*m, k*(m**2 - D)
    now if x,y is chosen which gcf(x,y) = 1, then:
        ((x*m + D*y)/k)**2 - D*((x + y*m)/k)**2 = (m*m - D)/k
    """
    #first round
    #a^2 - Db^2 = k, let b = 1, then find a as such that it's minimum
    a = b = 1
    while True:
        k = a**2 - n
        next_k = (a+1)**2 - n
        if abs(k) < abs(next_k):
            break
        a += 1
    triple1 = a,b,k
    #print "f) %d^2 - %dx%d^2 = %d" % (a, n, b, k)

    # now that we found a,b,k triple, the next steps are to come up with new triple that has k = 1
    # we use a few methods: 1) bhaskara's lemma, and 2) brahmagupta observation
    
    while True:
    
    
        #if we're lucky, k is 1
        if k == 1:
            break
        #otherwise, we go second method.    
        #based on brahmagupta observation, composition of two triples (x1,y1,k1) and (x2,y2,k2) can generate new triples (3), by using this formula:
        #new_a = x3 = x1*x2+N*y1*y2   new_b = y3 = x1*y2+x2*y1   new_k = k3=k1*k2
        #note that new_k is squared, thus this is great if k is -1; we can compose the triple with its own (e.g. x1=x2=a...)
        elif k == -1 and 1 == 0:
            #compose with its own, so that -1*-1 become 1
#             print "a) %d^2 - %dx%d^2 = %d (m=%d)" % (a, n, b, k, m)
            a,b,k = (a*a + n*b*b), (a*b+a*b), k*k
#             print "b) %d^2 - %dx%d^2 = %d (m=%d)" % (a, n, b, k, m)
            #print "B) %d^2 - %dx%d^2 = %d" % (a, n, b, k)
            break
        #for -2,2,-4,4 it's similar to -1, but since k will be squared, we need to divide k with k**2 i
        #since a and b is actually a square (remember the original relation: x*x - D*y*y = k)
        #a and b must be divided by k. Proof: (x**2 - D*y**2)/z = k/z <=> x**2/z - D*y**2/z = k/z <=> (x/z**0.5)**2 - D*(y/z**0.5)**2 = k/z
        #however, this can only be done if the new a and b is also integer, otherwise, no.
        elif k in [-1, -2, 2,-4, 4, -8, 8, -16, 16] and 2*a*b % k == 0:
            #a2,b2,k2 = (a*a + n*b*b), (a*b+a*b), (k**2)
            a,b,k = (a*a + n*b*b)/abs(k), 2*a*b/abs(k), 1
            #print "C) %d^2 - %dx%d^2 = %d" % (a, n, b, k)
            break

        #Now uses Bhaskara's Lemma that given a triple and "m", we can feed them into the following formula to get new triples
        # new_a = (a*m+n*b)/abs(k)   new_b = (a+b*m)/abs(k)   new_k = (m*m-n)/k
        # ref: http://en.wikipedia.org/wiki/Bhaskara%27s_lemma
        #Now we need to decide the best "m" that fulfil: new_b is integer, and new_k is "minimal" (as close to 1 as possible)

    
        m = 1
        t3 = candidate_m = None
        while True:
            #print "t1", t1, m, "abk", a,b,k
            if (a + b*m) % k == 0:
                t3 = (m*m-n)/k
                if candidate_m and abs(t3) > abs(candidate_t3):
                    m = candidate_m
                    break
                candidate_m, candidate_t3 = m, t3
            m += 1    
        a,b,k = (a*m+n*b)/abs(k), (a + b*m)/abs(k), (m*m-n)/k
        #print "L) %s^2 - %dx%s^2 = %d (m=%d)" % (a, n, b, k, m)
        #a1,b1,k1 = (a*a + n*b*b)/float(abs(k)), (a*b), 1
        #print "2b) %d^2 - %dx%d^2 = %d (m=%d)" % (a1, n, b1, k1, m)
        
        assert (a*a-n*b*b) == k, "1) %d should be %d for %s,%s" % (a*a-n*b*b, k, a, b)

    #print "solution) %d^2 - %dx%d^2 = %d" % (a, n, b, k)
    
    if n <= 102:
        assert a == xsols[n], "%s vs %s" % (a, xsols[n])
    
    #otherwise, cycle to bhaskara's lemma method until solution is found (k=1)
    a,b = int(a), int(b)
    assert (a*a-n*b*b) == 1, "2) %s should be 1 for %s,%s,%s" % (a*a-n*b*b, a, b, n)
    return a,b

def try1():
    #SLOW!!
    max_x = max_D = 0
    for D in xrange(1,1000+1):
    #     print "D=",D
        if (D**0.5) % 1 == 0:
            continue
    
        #i think y must not be 0, otherwise, minimum x will always be achieved when y is 0
        #for a solution, y must be whole number
        x = yy = 0
        min61 = 10
        while yy == 0 or yy % 1 != 0 or yy**0.5 % 1 != 0:
            x += 1
            yy = (x*x - 1.0)/D
            
            if x > 10000000:
                print "BIGX AT D", D
                break
            
    #         print x, yy, yy 
    #         y = yy**0.5
    #         if D == 61 and x == 1849678:
    #             print x, yy, y
    
        #by this time, x is minimal. so let's record the LARGEST x for all D
        if x > max_x:
            max_x = x
            max_D = D
    #     print "%d^2 - %dx%d^2 = 1" % (x, D, y)
    print "ans:", max_D
    
    
def try2():    
    max_x = max_D = 0
    for D in xrange(1,1000+1):
        if (D**0.5) % 1 == 0:
            continue
        #print "D=",D
        x,y = chakravala(D)
        #print "x",x
        if x > max_x:
            max_x = x
            max_D = D

    print "ans:", max_D
    
try2()
print time.time() - st