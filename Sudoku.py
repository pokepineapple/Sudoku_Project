from asyncio.windows_events import NULL
from matplotlib.style import use
import numpy as np
import random as rn

#Modified to make it more simplistic/readable
#However, the main issue lies with the problem of 
#conflicting numbers and checking if a number 
#needs to be used in X row or Y column would produce
#a multitude of issues leaving a 0 beahind,
#so this code will be left as it is

def number_list():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    return numbers

#True = Number has been Used
#False = Number not been Used
def used_row(matrix, row, number):
    for col in np.arange(0, len(matrix[0])):
        if matrix[row][col] == number:
            return True
    return False

def used_col(matrix, col, number):
    for row in np.arange(0,len(matrix[0])):
        if matrix[row][col] == number:
            return True
    return False

def used_box(matrix, row, col, number):
    for r in np.arange(row, row+3):
        for c in np.arange(col, col+3):
            if matrix[r][c] == number:
                return True
    return False

def must_use_number():
    return

def number_box(matrix, row, col):
    #Skips over the Boxes that were filled diagonally
    if matrix[row][col] != 0:
        return matrix
    
    num_list = number_list()
    rn.shuffle(num_list)
        
    for r in np.arange(row,row+3):              
        for c in np.arange(col, col+3):  
            for number in num_list:
                if (used_box(matrix, row, col, number) or 
                    used_col(matrix, c, number) or 
                    used_row(matrix, r, number)) == False:
                    matrix[r][c] = number
                    
                if matrix[r][c] != 0:
                    break
    return matrix

#Fill 3 boxes diagonally as they do not influence each other
def fill_dia(matrix):
    col = 0
    for row in np.arange(0,9,3):
        list = number_list()
        rn.shuffle(list)
        for r in np.arange(row, row+3):              
            for c in np.arange(col, col+3):
                number = rn.choice(list)
                matrix[r][c] = number
                list.remove(number)
        col += 3
    return matrix

#Remember to change it back to 9
def puzzle_generate():
    puzzle = np.zeros((9,9))
    fill_dia(puzzle)
    
    for i in np.arange(0,9,3):
        for j in np.arange(0,9,3):
            number_box(puzzle, i, j)
    
    return puzzle
    
    
sudoku = puzzle_generate()
for line in sudoku: print(line)