"""

S(A) = sum(A), A = set(), n = len(A)
B - C = empty


special sum set:
S(B) != S(C)
if len(B) > len(C), S(B) > S(C)

Example
n=1, (1) = 1
n=2, (1,2) = 3
    1,2
n=3, (2,3,4) = 9
    2v3 2v4 3v4
    23v4 24v3 34v2
    mycheck
    2v3 2v4 2v34
    3v2 3v4 3v24
    (4v2) (4v3) 4v23
    (23v4)
    (24v3)
    (34v2)
n=4, (3,5,6,7) = 21
    .3v5 .3v6 .3v7 .5v6 .5v7 .6v7
    .35v6 .35v7 35v67
    36v5 36v7 36v57
    37v5 37v6 37v56
    56v3 56v7
    57v3 57v6
    67v3 67v5
    356v7
    357v6
    367v5
    567v3
    ==
    3v5 3v6 3v7
    3v56 3v57 3v67
    3v567
    
    5v6 5v7
    5v36 5v37 5v67
    5v367
    
    6v7
    6v35 6v37 6v57
    6v357
    
    7v35 7v36 7v56
    7v356
    
    35v67
    36v57
    37v56
    ===

    3v56 3v57 3v67
    3v567    
    5v36 5v37 5v67
    5v367
    6v35 6v37 6v57
    6v357
    7v35 7v36 7v56
    7v356
    35v67
    36v57
    37v56

n=5, (6,9,11,12,13) = 51
"""
from itertools import combinations, count
from time import time

st = time()

def is_special_sum_set(A):
    """
    - no need to test 1v1 because the sum is different, and len is equal
    - 
    """
    len_A = len(A)
    for len_B in xrange(1,len_A/2 + 1):
        for B in combinations(A, len_B):
            sum_B = sum(B)
            A_comp_B = A - set(B)
            for len_C in xrange(2,len_A - len_B + 1):
                for C in combinations(A_comp_B, len_C):
                    sum_C = sum(C)
                    #rule2: if len(B) > len(C), then sum(B) > sum(C)
                    if (len_B > len_C and sum_B <= sum_C):
                        return False
                    if (len_C > len_B and sum_C <= sum_B):
                        return False

                    #rule1: for any 2 subsets (disjoint--no element is shared, and nonempty) called B C, sum(B) != sum(C)
                    if sum_B == sum_C:
                        print sorted(list(A)), B, C, "fail"
                        return False


    return True
    
    
for A in combinations(range(1,10),4):
    if is_special_sum_set(set(A)):
        print A, sum(A)
                                    
print time() - st