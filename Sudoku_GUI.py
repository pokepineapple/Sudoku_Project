from msilib import text
from turtle import color
import numpy as np
import tkinter as tk
from Sudoku_Final import *

game = tk.Tk()  
game.title("Sudoku")  
game.geometry("900x550")  

sol = []     #Stores the solution
sudoku = []       #Stores the base puzzle keep to keep for resets
player_sudoku = []  #Copies the puzzle to allow edits

def display_button(xpos, ypos):
    global player_sudoku, sudoku
    
    #SCREAMS
    def update_text(button, x,y):
        list = [" ", 1, 2, 3, 4, 5, 6, 7, 8, 9]
        index = (list.index(button['text'])+1)%10
        button['text'] = list[index]
        if list[index] == " ":
            player_sudoku[x][y] = 0
        else:
            player_sudoku[x][y] = list[index]
                
    #note: will need to calculate matrix position for command
    X = int((xpos - 375)/56)
    Y = int((ypos - 25)/56)
    
    frame = tk.Frame(game, width=56, height=56, highlightbackground = "black", bg = "pink",
                         highlightthickness = 2, bd = 0) 
    #add command connecting to text_button()
    if sudoku[X][Y] != 0:
        button1 = tk.Button(frame, text= sudoku[X][Y],font = (("Arial"),20)) 
    else:
        button1 = tk.Button(frame, text= " ", font = (("Kristen ITC"),20)) 
        button1.config(command= lambda: update_text(button1, X, Y))
        
    frame.grid_propagate(False)         #disables resizing of frame
    frame.columnconfigure(0, weight=1)  #enables button to fill frame
    frame.rowconfigure(0,weight=1)      #any positive number would do the trick
    frame.place(x = xpos, y = ypos)     #put frame where the button should be
    button1.grid(sticky="wens")
    

def display_sudoku(level):
    global sol, sudoku, player_sudoku
    #Checks if theres a existing puzzle, and removes everything if True
    if sol != []:
        sol.clear()
        sudoku.clear()
        
    sol = solution_generator()
    sudoku   = sudoku_generator(sol, level)
    player_sudoku = np.ndarray.tolist(np.copy(sudoku))
    # #create a loop that creates a button
    for x in range(375, 879, 56):
        for y in range(25,529, 56):
            display_button(x, y)

#bttn = tk.Button(button_border, text = 'Submit', fg = 'black',
#                 bg = 'yellow',font = (("Times New Roman"),15))

easy = tk.Button(game, text = "Easy", height = 2, width= 10, command = lambda: display_sudoku(1)).place(x = 50, y = 150)
normal = tk.Button(game, text = "Normal", height = 2, width= 10, command = lambda: display_sudoku(2)).place(x = 50, y = 200)
hard = tk.Button(game, text = "Hard", height = 2, width= 10, command = lambda: display_sudoku(3)).place(x = 50, y = 250)
random = tk.Button(game, text = "Random", height = 2, width= 10, command = lambda: display_sudoku(4)).place(x = 50, y = 300)

game.mainloop()  