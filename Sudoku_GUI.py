from turtle import color
import numpy as np
import tkinter as tk
from tkinter import messagebox
from Sudoku_Final import *
# from ai_sudoku import *
#from PIL import Image, ImageTk

game = tk.Tk()  
game.title("Sudoku")  
game.geometry("900x550")  
game['background'] = "purple"

#game.wm_attributes("-alpha", 0.5)

sol = []            #Stores the solution
sudoku = []         #Stores the original puzzle
player_sudoku = []  #Copies the puzzle to allow edits
hcounter = 3        #Number of hints per sudoku puzzle

button_list = [[0 for x in range(9)] for y in range(9)]     #Stores array of the buttons to access it

#Setups how 81 buttons are numbered and placed 
def display_button(xpos, ypos):
    global player_sudoku, sudoku, button_list
    
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
    
    frame = tk.Frame(game, width=56, height=56, highlightbackground = "black", 
                         highlightthickness = 2, bd = 1) 
    
    if sudoku[X][Y] != 0:
        button1 = tk.Button(frame, text= sudoku[X][Y],font = (("Arial"),24), relief= tk.FLAT, bg = "lime green") 
        
        button_list[X][Y] = 0
    else: ##THIS LETS ME ALTER BUTTON TEXT 
        button1 = tk.Button(frame, text= " ", font = (("Kristen ITC"),24)) 
        button1.config(command= lambda: update_text(button1, X, Y))
        
        button_list[X][Y] = button1 #Do i even need to?
        
    frame.grid_propagate(False)         #disables resizing of frame
    frame.columnconfigure(0, weight=1)  #enables button to fill frame
    frame.rowconfigure(0,weight=1)      #any positive number would do the trick
    frame.place(x = xpos, y = ypos)     #put frame where the button should be
    button1.grid(sticky="wens")
    
#Setups up the placement of the board
def display_sudoku(level):
    global sol, sudoku, player_sudoku, hcounter
    #Checks if theres a existing puzzle, and removes everything if True
    if sol != []:
        sol.clear()
        sudoku.clear()
        
    sol = solution_generator()
    sudoku   = sudoku_generator(sol, level)
    player_sudoku = np.ndarray.tolist(np.copy(sudoku))
    hcounter = 3    #resets counter for hints available
    # #create a loop that creates a button
    for x in range(375, 879, 56):
        for y in range(25,529, 56):
            display_button(x, y)

def hint_button():
    global sol, player_sudoku, hcounter, button_list
    if sudoku == []:
        messagebox.showwarning("Hint Error",  "Please select a game first.")
    else:
        if hcounter > 0:
            hcounter -=1            
            x, y = rn.randint(0,8), rn.randint(0,8)
            while (sol[x][y] == player_sudoku[x][y]): #if they match dont provide a hint at the location
                x, y = rn.randint(0,8), rn.randint(0,8)
            
            player_sudoku[x][y] = sol[x][y]    #copies the answer over
            reset_butt = button_list[x][y]     #updates the button_list
            reset_butt['text'] = sol[x][y]
            reset_butt['bg']   = "pink"
            button_list[x][y] = reset_butt
        else:
            messagebox.showinfo("Hint", "No more hints left")

        mess = ['       Hint Used\n', 'Remaining Hints: ', str(hcounter) ]
        messagebox.showinfo("Hint", "".join(mess))        

##NEED TO COMPLETE THIS
def solution_check(answer):
    temp = np.array(answer)
    for i in range(9):
        if np.unique(temp[i,:]).size < 9 or np.unique(temp[:,i]).size < 9:
            print("row ", i,  " ", temp[i,:])
            print("col", i, " ", temp[:,i])
            return False

    row, col, i = 0, 0, 0
    while row < 9:
        if np.unique(temp[row:row+3, col:col+3]).size < 9:
            print("box\n", i, " ", temp[row:row+3, col:col+3], " ", row, col)
            return False
        col += 3
        i +=1

        if i%3 and i > 0:
            row += 3
            col = 0
    return True


#need to check if the player found an alternative solution
def submit_button():
    global sol, player_sudoku    
    if sol == []:
        messagebox.showwarning("Submit Error",  "Please select a game mode first.")
    else:
        if sol == player_sudoku or solution_check(player_sudoku) == True:  #if the arrays are a match
            messagebox.showinfo("Congrats.",  "You won the game!!!")
        else: #if they are not a match
            messagebox.showinfo("Oh No...",  "You made a mistake somewhere. Keep Trying!")

def reset_button():
    global button_list, player_sudoku, sudoku    
    if sudoku == []:
        messagebox.showwarning("Reset Error",  "Please select a game first.")
    else:
        for i in range(9):
            for j in range(9):
                if sudoku[i][j] == 0:
                    player_sudoku[i][j] = 0  #resets what ever number stored to 0
                    reset_butt = button_list[i][j]
                    reset_butt['text'] = " "
                    reset_butt['bg']   = "light gray"
                    button_list[i][j] = reset_butt
###NEED TO COMPLETE
def ai_button():
    global button_list, sudoku, player_sudoku

    if sudoku == []:
        messagebox.showwarning("AI Error",  "Please select a game first.")
    else:
        solve(player_sudoku, 0, 0)

def solve(sudo, row, col):
    global button_list, player_sudoku
    if row == 8 and col == 9:
        player_sudoku = sudo
        return True
    
    if col == 9:
        row += 1
        col = 0

    if sudo[row][col] != 0:
        return solve(sudo, row, col+1)
    else:
        for num in range(10):
            if options(sudo, row, col, num) == True:

                butt = button_list[row][col]     #updates the button_list
                butt['text'] = num
                butt['bg'] = 'light blue'
                button_list[row][col] = butt

                sudo[row][col] = num
                if solve(sudo, row, col+1) == True:
                    return True
                else:
                    sudo[row][col] = 0

    return False

def options(sudo, row, col, num):
    for i in range(9):
        if sudo[row][i] == num or sudo[i][col] == num:
            return False

    r = int(row/3)*3
    c = int(col/3)*3

    for i in range(3):
        for j in range(3):
            if sudo[r+i][c+j] == num:
                return False

    return True





easy = tk.Button(game, text = "Easy", height = 2, width= 10, command = lambda: display_sudoku(0)).place(x = 50, y = 150)
normal = tk.Button(game, text = "Normal", height = 2, width= 10, command = lambda: display_sudoku(1)).place(x = 50, y = 200)
hard = tk.Button(game, text = "Hard", height = 2, width= 10, command = lambda: display_sudoku(2)).place(x = 50, y = 250)
random = tk.Button(game, text = "Random", height = 2, width= 10, command = lambda: display_sudoku(3)).place(x = 50, y = 300)

AI = tk.Button(game, text = "AI Solver", height = 2, width= 10, command = lambda: ai_button()).place(x = 150, y = 150)
hint = tk.Button(game, text = "Hint", height = 2, width= 10, command = lambda: hint_button()).place(x = 150, y = 200)
reset = tk.Button(game, text = "Reset", height = 2, width= 10,command = lambda: reset_button()).place(x = 150, y = 250)
submit = tk.Button(game, text = "Submit", height = 2, width= 10, command= lambda: submit_button()).place(x = 150, y = 300)

#Testing the borders
# load = Image.open("SquareB.png")
# render = ImageTk.PhotoImage(load)
# img = tk.Label(image=render)
# img.image = render
# img.place(x=400, y=300)

#bttn = tk.Button(button_border, text = 'Submit', fg = 'black',
#                 bg = 'yellow',font = (("Times New Roman"),15))

game.mainloop()  