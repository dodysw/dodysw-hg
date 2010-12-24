from time import time
st = time()

matrix = [map(int, e.split(",")) for e in file("matrix.txt").read().split("\n")]

def scanner():
    #start from bottom right, and progressively right to left then bottom to top, sum element with its right or bottom element whichever is the smallest.
    #the solution will be found on top left
    max_y = len(matrix)-1
    max_x = len(matrix[0])-1
    for y in xrange(max_y,-1,-1):
        for x in xrange(max_x,-1,-1):
            adder = None
            if x < max_x:
                adder = matrix[y][x+1]
            if y < max_y:
                adder = matrix[y+1][x] if adder is None else min(adder, matrix[y+1][x])
            if adder is not None:
                matrix[y][x] += adder
    return matrix[0][0]
        
print "ans:", scanner()
print time()-st