"""
If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are exactly three solutions for p = 120.

{20,48,52}, {24,45,51}, {30,40,50}

For which value of p <= 1000, is the number of solutions maximised?

"""

#brute force
import math
last_max_sol = [0,0]
for i in xrange(3,1001):
    last_found_b = 0
    sol_num = 0
    for a in xrange(1,i/2):
        if a == last_found_b:
            break
        for b in xrange(1,i/2):
            c = math.sqrt(a**2+b**2)
            if a + b + c == i:
                last_found_b = b    # optimization
                sol_num += 1
                #solutions.append("{%s, %s, %s}" % (a,b,c))
    
    if sol_num > last_max_sol[0]:
        last_max_sol = [sol_num, i]
        print last_max_sol
        
print last_max_sol