#!/usr/bin/env python3 
# Python3 version used: 3.9.10
from itertools import count
import random as rn
import numpy as np

# pattern for a baseline valid solution
# determines location value that is determined to be
# a valid number solution for its location on the grid
def pattern(row,col, base, dim): 
    return (base*(row%base)+row//base+col)%dim

#randomize rows, columns and numbers (of valid base pattern)
def randomize(s): 
    return rn.sample(s,len(s)) 

def rc_pattern(rbase, base):
    result = []
    for i in randomize(rbase):
        for j in randomize(rbase):
            #print(i*base+j)
            result.append(i*base + j)
    return result

def solution_generator():    
    base  = 3 #Alter if want a bigger board
    dim   = base*base
    rBase = range(base) 
    rows = rc_pattern(rBase, base)
    cols = rc_pattern(rBase, base)
    nums = randomize(range(1,dim+1))
    
    #nested for loops to produce the board with
    #no duplicated numbers in each row, col, and box
    puzzle = [ [nums[pattern(r,c, base, dim)] for r in rows] for c in cols ]
    return puzzle #np.asarray(puzzle) 

def remove_number(matrix, number):
    counter = number
    copy = matrix.copy()
    while counter != 0:
        for r in range(9):
            for c in range(9): 
                if copy[r][c] != 0:
                    if rn.randint(0, 2) == 0 and counter > 0:
                        copy[r][c] = 0
                        counter -= 1
        if counter == 0:
            break
    return copy

#NOTE: Wierd Bullshit occurred when using .copy() on the sol causing
#      variable overwrite elsewhere, but using np.copy() prevents this
#      so funct temporarily converts list to ndarray then back to list
def sudoku_generator(sol, level):
    solu = np.copy(sol)
    if level == 1:   #Easy Mode
        return np.ndarray.tolist(remove_number(solu, rn.randint(33,43)))
    elif level == 2: #Normal Mode
        return np.ndarray.tolist(remove_number(solu, rn.randint(44,53)))
    elif level == 3: #Hard Mode
        return np.ndarray.tolist(remove_number(solu, rn.randint(54,60)))
    elif level == 4: #Random Mode
        return np.ndarray.tolist(remove_number(solu, rn.randint(33,60)))
    else: #Precaution for anything odd
        return 0


#Test Code
# solution = solution_generator()
# puzzle = sudoku_generator(np.copy(solution), 2)

# print(type(solution))
# print(type(puzzle))


# print("Puzzle")
# for line in puzzle: print(line)
# print("Solution")
# for line in solution: print(line)