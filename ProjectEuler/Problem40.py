"""
An irrational decimal fraction is created by concatenating the positive integers:

0.123456789101112131415161718192021...

It can be seen that the 12^(th) digit of the fractional part is 1.

d_(1) x d_(10) x d_(100) x d_(1000) x d_(10000) x d_(100000) x d_(100000)

d1 = 1
d10 = 1
d30 = 2
d50 = 3
d70 = 4
d90 = 5
d100 = 5
d400 = 2
"""
# build string
n = 0   #start from zero so that the index is 1-based
d = ""
while len(d) <= 1000000 :
    d += str(n)
    n += 1
    
print int(d[1])*int(d[10])*int(d[100])*int(d[1000])*int(d[10000])*int(d[100000])*int(d[1000000])