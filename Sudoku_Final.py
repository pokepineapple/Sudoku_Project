# pattern for a baseline valid solution
# determines location value that is determined to be
# a valid number solution for its location on the grid
def pattern(row,col, base, dim): 
    return (base*(row%base)+row//base+col)%dim

#randomize rows, columns and numbers (of valid base pattern)
import random as rn
def randomize(s): 
    return rn.sample(s,len(s)) 

def rc_pattern(rbase, base):
    result = []
    for i in randomize(rbase):
        for j in randomize(rbase):
            #print(i*base+j)
            result.append(i*base + j)
    return result

def sudoku_generator():    
    base  = 3 #Alter if want a bigger board
    dim   = base*base
    rBase = range(base) 
    rows = rc_pattern(rBase, base)
    cols = rc_pattern(rBase, base)
    nums = randomize(range(1,dim+1))
    
    #nested for loops to produce the board with
    #no duplicated numbers in each row, col, and box
    puzzle = [ [nums[pattern(r,c, base, dim)] for r in rows] for c in cols ]
    return puzzle

# solution = sudoku_generator()
# for line in solution: print(line)