from pprint import pprint
from copy import deepcopy
from itertools import product
from time import time


st = time()

correct_sequence = range(1,10)
MAX_LEVEL = 2

def check_consistency(grid):
    all_horiz_correct = len([row for row in grid if row.count(0) == 0 and sorted(row) != correct_sequence]) == 0
    all_vert_correct = len([row for row in map(None, grid) if row.count(0) == 0 and sorted(row) != correct_sequence]) == 0
    all_box_correct = True
    for boxnum in xrange(9):
        offsety, offsetx = divmod(boxnum, 3)
        boxdata = [grid[y][x] for y in xrange(offsety*3,offsety*3+3) for x in xrange(offsetx*3,offsetx*3+3)]
        if boxdata.count(0) == 0 and sorted(boxdata) != correct_sequence:
            all_box_correct = False
            break
    return all_horiz_correct and all_vert_correct and all_box_correct

def is_grid_solved(grid):
    if len([row for row in grid if row.count(0) > 0]) > 0:
        return False
    return check_consistency(grid)
        
def solve_sudoku(grid, level=1):
    gridguess = deepcopy(grid)
    redo = True
    while redo:
        redo = False
        if not check_consistency(grid):
            return False
        
        #algo1: slice and dice
        for y,x in product(range(9),range(9)):
            n = grid[y][x]
            if n != 0:
                continue

            options = set(correct_sequence)  
            options -= set(grid[y])
            options -= set([line[x] for line in grid])
            options -= set([grid[y2][x2] for y2 in range(y-y%3, y-y%3 + 3) for x2 in range(x-x%3, x-x%3 + 3) ])
            
            gridguess[y][x] = options
            if len(options) == 1:
                grid[y][x] = gridguess[y][x] = options.pop()
                redo = True
        if redo:
            continue
        
        #single square candidate
        #horiz
        for y in xrange(9):
            #combine sets into single list
            row = [n for candidate in gridguess[y] if type(candidate) == set for n in candidate]
            #look for single number
            singles = [n for n in row if row.count(n) == 1]
            #trace back to its square, and upgrade to answer
            for single in singles:
                for x in xrange(9):
                    if type(gridguess[y][x]) != set:
                        continue
                    if single in gridguess[y][x]:
                        grid[y][x] = gridguess[y][x] = single
                        redo = True
        
        if redo:
            continue
        
        #vertical
        for x in xrange(9):
            #combine sets into single list
            col = [row[x] for row in gridguess if type(row[x]) == set]
            #look for single number
            singles = [n for n in col if col.count(n) == 1]
            #trace back to its square, and upgrade to answer
            for single in singles:
                for y in xrange(9):
                    if type(gridguess[y][x]) != set:
                        continue
                    if single in gridguess[y][x]:
                        grid[y][x] = gridguess[y][x] = single
                        redo = True
        
        if redo:
            continue
        
        #box
        for boxnum in xrange(9):
            offsety, offsetx = divmod(boxnum, 3)
            #combine sets into single list
            box = [gridguess[y][x] for y in xrange((offsety)*3,(offsety)*3+3) for x in xrange((offsetx)*3,(offsetx)*3+3) if type(gridguess[y][x]) == set]
            #look for single number
            singles = [n for n in box if box.count(n) == 1]
            #trace back to its square, and upgrade to answer
            for single in singles:
                for y in xrange(9):
                    if type(gridguess[y][x]) != set:
                        continue
                    if single in gridguess[y][x]:
                        grid[y][x] = gridguess[y][x] = single
                        redo = True
        
        if redo:
            continue

    if level <= MAX_LEVEL:
        #final algo: guess.
        #loop through all sets
        for y,x in product(range(9),range(9)):
            if grid[y][x] != 0:
                continue
            for candidate in gridguess[y][x]:
                guessed_grid = deepcopy(grid)
                guessed_grid[y][x] = candidate
                res = solve_sudoku(guessed_grid, level+1)
                if res:
                    return res

    if is_grid_solved(grid):
        return grid
    else:
        return False
                
grids = [[[int(c) for c in line] for line in file("sudoku.txt").read().split("\n")[10*i+1:10*i+10]] for i in xrange(50)]
total = 0
for grid in grids:
    solvedgrid = solve_sudoku(grid)
    frow = solvedgrid[0]
    topleft_digit = 100*frow[0] + 10*frow[1] + frow[2]
    total += topleft_digit
    
print "ans:", total
#24702
print time() - st