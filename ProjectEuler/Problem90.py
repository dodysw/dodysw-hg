from time import time
from itertools import combinations, izip
st = time()

#since 6 = 9 for the purpose of testing, change all 9 to 6
squares = "01","04","06","16","25","36","46","64","81"
def test(sqa, sqb):
    assert len(sqa) == len(sqb) == 6
    sqa = sqa.replace("9","6")
    sqb = sqb.replace("9","6")
    for sq in squares:
        if not ((sq[0] in sqa and sq[1] in sqb) or (sq[1] in sqa and sq[0] in sqb)):
            return False
    return True

def try1():
    #brute force
    distincts = set()
    add = distincts.add
    tuple2string = ''.join
    for cube_a in combinations("0123456789",6):
        for cube_b in combinations("0123456789",6):
            if test(tuple2string(cube_a), tuple2string(cube_b)):
                add(cube_a + cube_b if cube_a <= cube_b else cube_b + cube_a)
    print "ans:", len(distincts)
    
try1()
print time() - st