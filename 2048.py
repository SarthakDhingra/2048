import random as rnd
import os
import sys

class Grid():
    def __init__(self, row=4, col=4, initial=2):
        self.row = row                              # number of rows in grid
        self.col = col                              # number of columns in grid
        self.initial = initial                      # number of initial cells filled
        self.score = 0

        self.grid = self.createGrid(row, col)       # creates the grid specified above

        self.emptiesSet = []                        # list of empty cells
        self.updateEmptiesSet()

        for _ in range(self.initial):               # assign two random cells
            self.assignRandCell(init=True)


    def createGrid(self, row, col):             #Creates the grid, where there are a row number of lists, each with a length of col.All elements of the data structure are 0
        return [col*[0] for x in range(row)]    

    def assignRandCell(self, init=False):
        if len(self.emptiesSet):
            cell = rnd.sample(self.emptiesSet, 1)[0]
            if init:
                self.grid[cell[0]][cell[1]] = 2
            else:
                cdf = rnd.random()
                if cdf > 0.75:
                    self.grid[cell[0]][cell[1]] = 4
                else:
                    self.grid[cell[0]][cell[1]] = 2
            self.emptiesSet.remove(cell)


    def drawGrid(self):
        for row_index in range(self.row):
            line = '\t|'
            for col_index in range(self.col):
                if not self.grid[row_index][col_index]:
                    line += ' '.center(5) + '|'
                else:
                    line += str(self.grid[row_index][col_index]).center(5) + '|'
            print(line)
        print()


    def updateEmptiesSet(self): #Method updates the emptiesSet list to contain the new set of empty tiles after a collapse
        self.emptiesSet = []
        for values in range(self.col*self.row):
            row_num = values // self.row
            col_num = values % self.col
            if self.grid[row_num][col_num] == 0:
                self.emptiesSet.append([row_num,col_num])

    def collapsible(self): #This method returns True if the grid can be collapsed in any of the four directions. Otherwise, False will be returned
        collapse = False
        
        for values in range(self.col*self.row):  
            row_num = values // self.row           #finds the row index and column index of a tile based of the tiles value (value is a number between 0 and (self.col*self.row - 1)) 
            col_num = values % self.col            
            tile = self.grid[row_num][col_num]
            
            col_next = col_num + 1                 #finds the next column and row indeces of tiles current column and row indeces
            row_next = row_num + 1
                        
            if self.grid[row_num][col_num] == 0:   #grid is collapsable if a tile in the grid has the value 0
                collapse = True
            
            elif (col_num < self.col - 1 and self.grid[row_num][col_next] == tile): #grid is collapsable if two consecutive horizontal tiles have the same value 
                collapse = True                                                    
                
            elif (row_num < self.row - 1 and self.grid[row_next][col_num] == tile): #grid is collapsable if two consecutive vertical tiles have the same value 
                collapse = True                                                     
                collapse = True
            
        return collapse                          

    def collapseRow(self, lst):     #This method returns a LEFT-collapsed list. It also returns True if the list was collapsed or False if it was not.
        collapse = False
        temp_lst = []       
        original_len = len(lst)     #records the original length of list
        
        for value in lst:           #creates a new list called temp_lst identical to lst
            temp_lst.append(value)
        
        while 0 in lst:             #removes all the 0s in lst
            lst.remove(0)
            
        new_len = len(lst)          #records the length of lst after the 0s have been removed
    
        for value in range(new_len):# If two tiles beside each other are equivalent, the value of the leftmost of the two tiles becomes the addition of the two tiles, and the rightmost tile becomes 0
            cell_next = value + 1
            if value < new_len - 1:
                if lst[value] == lst[cell_next]: 
                    collapse = True
                    lst[value] += lst[cell_next]
                    lst[cell_next] = 0
                    self.score = self.score + lst[value]    #increments the score by a number equivalent to the addition of two equivalent added cells
        
        while 0 in lst:             #removes all 0s in lst
            lst.remove(0)
        
        add_len = original_len - len(lst) #finds difference in length between original lst and current lst
        
        for values in range(add_len):#appends 0s to lst until lst has the same length has it originally did
            lst.append(0)  
        
        if temp_lst != lst:  #determines if the list was collapsed
            collapse = True
        
        return lst,collapse
    
    def collapseLeft(self): #This method collapses the grid to the left, and returns True if the grid was collapsed or False if it was not.
        collapse = False
        new_grid = []
        
        for values in self.grid:    #creates a new grid with all rows collapsed to the left using collapseRow()
            new_lst,collapse = self.collapseRow(values)
            new_grid.append(new_lst)
            
        self.grid = new_grid #assigns self.grid to new_grid
            
        return collapse

    def collapseRight(self): #This method collapses the grid to the right, and returns True if the grid was collapsed or False if it was not.
        collapse = False
        new_grid = []
        
        for values in self.grid:
            values.reverse()                            #reverses rows in self.grid
            new_lst,collapse = self.collapseRow(values) #collapses rows to the left using self.grid
            new_lst.reverse()                           #reverses rows again
            new_grid.append(new_lst)                    #appends collapsed rows to a new grid
            
        
        self.grid = new_grid #assigns self.grid to new_grid
        
        return collapse

    def collapseUp(self): #This method collapses the grid upwards, and returns True if the grid was collapsed or False if it was not.
        new_grid = []
        count = 0
        
        for value in range(self.row): #creates lists of all the columns in the grid and appends to new_grid
            temp_grid = []
            for value in self.grid:             
                temp_grid.append(value[count])
            count += 1
            new_grid.append(temp_grid)          
        
        intermediate_grid = []
        
        for values in new_grid: #collapses the columns using collapseRow() and appends the collapses column lists to intermediate_grid
            temp_lst, collapse = self.collapseRow(values)
            intermediate_grid.append(temp_lst)
    
        count = 0
        final_grid = []
        
        for items in range(self.row): #transforms collapsed column lists back into original grid format using final_grid
            temp_lst = []
            for values in intermediate_grid: 
                temp_lst.append(values[count])
            final_grid.append(temp_lst)      
            count += 1
        
        self.grid = final_grid #assigns self.grid to final_grid
        
        return collapse

    def collapseDown(self): #This method collapses the grid downards, and returns True if the grid was collapsed or False if it was not.
        new_grid = []
        count = 0
        
        for value in range(self.row): #creates lists of all the columns in the grid and appends to new_grid
            temp_grid = []
            for value in self.grid:
                temp_grid.append(value[count])
            count += 1
            new_grid.append(temp_grid) 
        
        intermediate_grid = []
        
        for values in new_grid: #collapses the columns using collapseRow() and appends the collapses column lists to intermediate_grid
            temp_lst, collapse = self.collapseRow(values)
            intermediate_grid.append(temp_lst)
            
        for values in intermediate_grid: #removes 0s from end of lists, and inserts them at beginning of lists
            while 0 in values:
                values.remove(0)
            while len(values) < self.col:
                values.insert(0,0)
    
        count = 0
        final_grid = []
        
        for items in range(self.row): #transforms collapsed column lists back into original grid format using final_grid
            temp_lst = []
            for values in intermediate_grid:
                temp_lst.append(values[count])
            final_grid.append(temp_lst)
            count += 1
        
        self.grid = final_grid #assigns self.grid to final_grid
        return collapse        

class Game():
    def __init__(self, row=4, col=4, initial=2):
        self.game = Grid(row, col, initial)
        self.play()

    def printPrompt(self): #The first 4 lines of this function were commented out upon the discretion of a TA to address the error: "TERM environment variable not set."
        #if sys.platform == 'win32':
            #os.system("cls")
        #else:
            #os.system("clear")
        print('Press "w", "a", "s", or "d" to move Up, Left, Down or Right respectively.')
        print('Enter "p" to quit.\n')
        self.game.drawGrid()
        print('\nScore: ' + str(self.game.score))

    def play(self):

        moves = {'w' : 'Up',
                 'a' : 'Left',
                 's' : 'Down',
                 'd' : 'Right'}

        stop = False
        collapsible = True

        while not stop and collapsible:
            self.printPrompt()
            key = input('\nEnter a move: ')

            while not key in list(moves.keys()) + ['p']:
                self.printPrompt()
                key = input('\nEnter a move: ')

            if key == 'p':
                stop = True
            else:
                move = getattr(self.game, 'collapse' + moves[key])
                collapsed = move()

                if collapsed:
                    self.game.updateEmptiesSet()
                    self.game.assignRandCell()

                collapsible = self.game.collapsible()

        if not collapsible:
            if sys.platform == 'win32':
                os.system("cls")
            else:
                os.system("clear")
            print()
            self.game.drawGrid()
            print('\nScore: ' + str(self.game.score))
            print('No more legal moves.')


# -----------------------------------------------------------------------------
# Main Function ---------------------------------------------------------------
# -----------------------------------------------------------------------------


# This condition ensures that the game isn't run if the file is loaded as
# a module. Will only run if the file is executed.

if __name__ == '__main__':
    game = Game()
