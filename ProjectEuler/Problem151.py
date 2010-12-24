def cut(anum):
    global A
    if A[anum] == 0:
        cut(anum-1)
    A[anum] -= 1
    A[anum+1] += 2

def pick(anum):
    global A
    if A[anum] == 0:
        cut(anum-1)
    A[anum] -= 1

A = [0,1,0,0,0,0]

#firstjob
pick(5)
print A

#simulate 14 times
chance = 0
for i in xrange(14):
    chance += A[5] / float(sum(A))
    pick(5)
    print A
print chance