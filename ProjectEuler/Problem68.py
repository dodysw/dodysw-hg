"""
3-gon ring
- working clockwise
- starting from the group of three 
- with the numerically lowest external node (4,3,2 in this example)
- each solution can be described uniquely
- For example, the above solution can be described by the set: 4,3,2; 6,2,1; 5,1,3.
Total	Solution Set
9	4,2,3; 5,3,1; 6,1,2  -> 4 << 5,6
9	4,3,2; 6,2,1; 5,1,3
10	2,3,5; 4,5,1; 6,1,3  -> 5 << 4+5 or 6
10	2,5,3; 6,3,1; 4,1,5
11	1,4,6; 3,6,2; 5,2,4  -> 6+4 << 6, or 5+4???
11	1,6,4; 5,4,2; 3,2,6
12	1,5,6; 2,6,4; 3,4,5
12	1,6,5; 3,5,4; 2,4,6

"""
# from itertools import permutations, chain
# 
# def ngon_naive(n):
#     for gon in permutations(range(1,n*2 + 1)):
#         outer = gon[:n]
#         inner = gon[n:]
             
        
        

from itertools import combinations, chain
from pprint import pprint
sums = {}
for e in combinations(range(1,11), 3):
    sum_e = sum(e)
    sums.setdefault(sum_e, [])
    sums[sum_e].append(list(e))

#for maximum, outer must be 6 to 9, 10 is included because max digits is 16
expected_outer = set(range(6,11))
expected_inner = set(range(1,6))
for s in sums:
    groups = []    
    #group must be 1 outer, and 2 inner
    for group in sums[s]:
        group.sort()
        if group[0] in expected_inner and group[1] in expected_inner and group[2] in expected_outer:
            groups.append(group)
    #group must composed all numbers 1 to 10
    #flatten
    flat = ''.join(map(str, chain(*groups)))
    if len(set(flat)) != 10:
        continue
    
    #first number must be minimum of outer, so it must start with 6
    
    
    
#     for group in [g for g in groups if g[2] == 6]:
#         i1,i2 = group[:2]
#         #the next group's inner 1 must equal to current inner 2
#         for group2 in [
    
    
    #possible candidate        
    print "sum",s,"len",len(flat), flat, groups
    
    #the rest is done through pencil and paper...