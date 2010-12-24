"""
Utk sqr(2)
1/1, 3/2, 7/5, 17/12, dst...
d2 = n1+d1
n2 = d2+d1


2/1, 3/1, 8/3, 11/4, 19/7, 87/32, 106/39, 193/71, 1264/465, 1457/536

2/1, 3/1, 8/3, [11/4, 19/7, x/32],  [106/39, 193/71, 1264/465], 1457/536
n2 = n1*d2/n2
d2 = x*d1+y*d0

d2 = 6*d1 + 1*d0
106 = 87*7+19


Known, the CF for e is:
[2; 1,2,1, 1,4,1, 1,6,1 , ... , 1,2k,1, ...]
so the 100th sequence is...
http://www.maths.surrey.ac.uk/hosted-sites/R.Knott/Fibonacci/cfINTRO.html#730

"""

def a():
    limit = 100
    seq = [2]
    k = 1
    while len(seq) < limit:
        seq += [1, 2*k, 1]
        k += 1
    #fold from right end
    seq = seq[limit-1::-1]
    n,d = 1,0
    for i in xrange(limit):
        n, d = n*seq[i]+d, n
    return sum(map(int, str(n)))
        

print "ans:", a()