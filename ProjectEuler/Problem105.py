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
                    #rule1: for any 2 subsets (disjoint--no element is shared, and nonempty) called B C, sum(B) != sum(C)
                    if sum_B == sum_C:
                        return False
                    #rule2: if len(B) > len(C), then sum(B) > sum(C)
                    if (len_B > len_C and sum_B <= sum_C):
                        return False
                    if (len_C > len_B and sum_C <= sum_B):
                        return False

    return True

sets = [map(int,line.split(",")) for line in file("sets.txt").read().split("\n")]
print "ans:", sum([sum(A) for A in sets if is_special_sum_set(set(A))])
print time() - st