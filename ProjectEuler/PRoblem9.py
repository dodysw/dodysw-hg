"""
a**2 + b**2 = c**2

sqrt(a**2 + b**2) = c = 1000 - a - b
sqrt(a**2 + b**2) + a + b = 1000
"""

for a in range(500):
    for b in range(500):
        delta = abs(((a**2 + b**2)**0.5 + a + b) - 1000)
        if delta < 0.001:
            print a,b, 1000-a-b, delta, a*b*(1000-a-b)
            
print 269**2 + 316**2, 415**2