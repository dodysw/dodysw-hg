"""
By starting at the top of the triangle below and moving to adjacent numbers on the row below, the maximum total from top to bottom is 23.

3
7 4
2 4 6
8 5 9 3

That is, 3 + 7 + 4 + 9 = 23.

Find the maximum total from top to bottom in triangle.txt (right click and 'Save Link/Target As...'), a 15K text file containing a triangle with one-hundred rows.

NOTE: This is a much more difficult version of Problem 18. It is not possible to try every route to solve this problem, as there are 2^(99) altogether! If you could check one trillion (10^(12)) routes every second it would take over twenty billion years to check them all. There is an efficient algorithm to solve it. ;o)
"""

data = []
def init_data():
    global data
    data = []
    raw = file("triangle.txt").read()
    for line in raw.split("\n"):
        if line != "":
            data.append([int(n) for n in line.split()])
    
def reduction():
    """reduce 100 rows tree by going from the bottom, adding the maximum element of the pair beneath. The largest sum will be found on the top.
    """
    for level in xrange(98,-1,-1):
        for n in xrange(len(data[level])):
            data[level][n] += max(data[level+1][n], data[level+1][n+1])
    print data[0][0]

if __name__ == "__main__":
    init_data()
    reduction()