import tkinter as tk
from Sudoku_Final import sudoku_generator

#window = tk.Tk()


#solution = sudoku_generator()
# for line in solution: print(line)s


obj=tk.Tk()  
obj.title("c# corner")  
obj.geometry("500x500")  


exit_button = tk.Button(
    obj,
    text='Button Orgasm',
    command=lambda: obj.quit()
)

exit_button.pack(ipadx=5,ipady=5,expand=True)

#wintext = tk.Text(obj)  
#wintext.pack()  
obj.mainloop()  