import numpy as np
import tkinter as tk
from tkinter import messagebox
from Sudoku_Final import *
from Sudoku_GUI import solution_check, button_list


##BACKTRACKING ALGORITHM WORKS BUT IT NEEDS TO UPDATE THE BUTTON DISPLAY NEXT
def solve(sudoku, row, col):
    if row == 8 and col == 9:
        return True
    
    if col == 9:
        row += 1
        col = 0

    if sudoku[row][col] != 0:
        return solve(sudoku, row, col+1)
    else:
        for num in range(10):
            if options(sudoku, row, col, num) == True:
                butt = button_list[row][col]     #updates the button_list
                butt['text'] = num
                butt['bg'] = 'light blue'
                button_list[row][col] = butt
                sudoku[row][col] = num
                if solve(sudoku, row, col+1) == True:
                    return True
                else:
                    sudoku[row][col] = 0

    return False

def options(sudoku, row, col, num):
    for i in range(9):
        if sudoku[row][i] == num or sudoku[i][col] == num:
            return False

    r = int(row/3)*3
    c = int(col/3)*3

    for i in range(3):
        for j in range(3):
            if sudoku[r+i][c+j] == num:
                return False

    return True


# solution = solution_generator()
# puzzle = sudoku_generator(np.copy(solution), 2)

# for line in puzzle: print(line)

# print("\n")
# solve(puzzle, 0, 0)

# for line in puzzle: print(line)

# print(solution == puzzle)
# print(solution_check(puzzle))

# for line in solution: print(line)
