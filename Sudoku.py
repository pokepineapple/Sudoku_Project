from asyncio.windows_events import NULL
from matplotlib.style import use
import numpy as np
import random as rn


def number_list():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    return numbers

#Checks if number can be used at location by checking
#Row, Column, and box to see if the number exists
def valid_location(matrix, row, col, number, banned):
    #matrix2 = np.transpose(matrix)
    #checks already used numbers in the 3x3 box
    if number in banned:
        return False
    elif number in matrix[row]:
        return False
    elif number in np.transpose(matrix)[col]:
        return False
    else:
        return True

#Insert [1:9] values into 3 by 3 box in the matrix
def number_box(matrix, row, col):
    num_list = number_list()
    banned = []
    rn.shuffle(num_list)
    for r in np.arange(row,row+3):              #Iterate Rows
        for c in np.arange(col, col+3):         #Iterate Columns
            #print("AVAILABLE NUMBERS", unused_num)
            for number in num_list:             #Iterate through 1 to 9
                #Check if the number for [r,c] position is allowed
                if valid_location(matrix, r, c, number, banned) == True:
                    #Stores the approve number
                    matrix[r][c] = number
                    #Keeps track of used numbers
                    banned.append(number)
                if matrix[r][c] != 0:
                    break

    #CHeck if the number_box has any 0s at all
    #if yes, reset the box to 0 and rerun function
    #else nothing happens
                
    return matrix


#Creates a 9x9 Sudoku puzzle
def puzzle_generate():
    puzzle = np.zeros((9,9))
    for i in np.arange(0,9,3):
        for j in np.arange(0,9,3):
            number_box(puzzle, i, j)
    return puzzle
    
    
sudoku = puzzle_generate()
for line in sudoku: print(line)

# Tested Box functionality for 3x3 grind
#Still need to test it in a 9x9 grid
# box = np.zeros((3,3))
# print(number_box(box, 0, 0))