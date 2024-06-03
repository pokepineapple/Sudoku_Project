import random as rn
import numpy as np

class sudoku:
    def __init__(self, level = 0):
        self.solution = []
        self.puzzle = []

        self.base = 3
        self.dim = self.base**2
        self.level = level
        return None

    def pattern(self, row,col) -> int: 
        return (self.base*(row%self.base)+row//self.base+col)%self.dim
    
    #randomize rows, columns and numbers (of valid base pattern)
    def randomize(self, s): 
        return rn.sample(s,len(s)) 

    def rc_pattern(self, rbase, base): #returns array
        result = []
        for i in self.randomize(rbase):
            for j in self.randomize(rbase):
                #print(i*base+j)
                result.append(i*base + j)
        return result
    
    def solution_generator(self):    
        rBase = range(self.base) 
        rows = self.rc_pattern(rBase, self.base)
        cols = self.rc_pattern(rBase, self.base)
        nums = self.randomize(range(1,self.dim+1))
        
        #nested for loops to produce the board with
        #no duplicated numbers in each row, col, and box
        temp = np.array([ [nums[self.pattern(r,c)] for r in rows] for c in cols ])
        self.puzzle = np.copy(temp)
        self.solution = temp
        return None
    
    #takes matrix and alters a set number of cells to 0/blank
    def remove_number(self, sol, number):
        while number > 0:
            for r in range(9):
                for c in range(9): 
                    if sol[r][c] != 0:
                        if rn.randint(0, 2) == 0 and number > 0:
                            sol[r][c] = 0
                            number -= 1
        return sol
    
    def sudoku_generator(self):
        removal = [[35,41], [42,51], [52,60], [35,60]]
        self.puzzle = self.remove_number(self.puzzle, rn.randint(removal[self.level][0], removal[self.level][1]))
        return None
    

    def main(self):
        self.solution_generator()
        print("Solution")
        for line in self.solution: print(line)

        print("Puzzle")
        self.sudoku_generator()
        for line in self.puzzle: print(line)

        # print("Check Solution")
        # for line in self.solution: print(line)
        return None


test = sudoku()
test.main()