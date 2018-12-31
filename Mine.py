import random, sys, math

class Cell:
    def __init__(self, b_mine, near_mines_number):
        self.b_mine = b_mine
        self.b_opend = False
        self.near_mines = near_mines_number

class GameBoard:
    def __init__(self, mines_num):
        self.mines_num = mines_num
        width = 2 # the smallest width
        mines_num_tmp = mines_num / 0.5 # use to make sure the mines will not cover too much area
        while width * width <= mines_num_tmp:
            width = width + 1
        width = width + 1
        self.width = width
        self.cell_num = width * width        
        self.cell = []
        for i in range(width):
            self.cell.append([])
            for j in range(width):
                self.cell[i].append(Cell(False, 0))

        # generate the mines
        mine_created = 0
        while mine_created < mines_num:            
            ran_row = math.floor(random.random() * self.width)
            ran_col = math.floor(random.random() * self.width)
            self.cell[ran_row][ran_col].b_mine = True
            mine_created = mine_created + 1            

        # generate the number around mines
        self.near_idx = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)) # near index offset, [row, col]
        for row in range(len(self.cell)):
            for col in range(len(self.cell[row])):
                if self.cell[row][col].b_mine == False:
                    near_mines = 0
                    for offset in self.near_idx:
                        row_tmp = row + offset[0]
                        col_tmp = col + offset[1]
                        if self.IsInBoard(row_tmp, col_tmp) == True and self.cell[row_tmp][col_tmp].b_mine == True:
                            near_mines = near_mines + 1
                    self.cell[row][col].near_mines = near_mines

        print('Gameboard with ' + str(self.mines_num) + ' mines in ' + str(self.width) + 'x' + str(self.width) + ' size created!!!')
        self.PrintCovered()
    
    def IsInBoard(self, row, col):
        if row < 0 or row >= self.width or col < 0 or col >= self.width:
            return False
        else:
            return True        

    def PrintUncovered(self):
        for row in self.cell:
            for col in row:
                if col.b_mine == True:
                    print('*', end=' ')
                elif col.near_mines == 0:
                    print(' ', end=' ')
                else:
                    print(col.near_mines, end=' ')
            print('')

    def PrintCovered(self):
        for row in self.cell:
            for col in row:
                if col.b_opend == True:
                    if col.b_mine == True:
                        print('*', end=' ')
                    elif col.near_mines == 0:
                        print(' ', end=' ')
                    else:
                        print(col.near_mines, end=' ')
                else:
                    print('●', end=' ')
            print('')

    def Open(self, row, col):
        if self.IsInBoard(row, col) == True:
            self.cell[row][col].b_opend = True
            if self.cell[row][col].b_mine == True:
                print('Mine Hit!!! Game Over!!!')
                self.PrintUncovered()
                sys.exit(0)
            elif self.cell[row][col].near_mines == 0:
                for offset in self.near_idx:
                    row_tmp = row + offset[0]
                    col_tmp = col + offset[1]
                    self.Open(row_tmp, col_tmp)
                

    def Sweep(self, row, col):
        if self.IsInBoard(row, col) == True:
            print('Sweep mine at (' + str(row) + ',' + str(col) + ').')
            if self.cell[row][col].b_opend == False:
                self.Open(row, col)
            else:
                for offset in self.near_idx:
                    row_tmp = row + offset[0]
                    col_tmp = col + offset[1]
                    if self.IsInBoard(row_tmp, col_tmp) == True:
                        self.Open(row_tmp, col_tmp)
        self.PrintCovered()

    def GetCell(self, row, col):
        if self.IsInBoard(row, col) == True:
            if self.cell[row][col].b_opend == False:
                return Cell(False, 0)
            else:
                return self.cell[row][col]

    def GetWidth(self):
        return self.width

    def IsMine(self, row, col):
        if self.IsInBoard(row, col) == True and self.cell[row][col].b_opend == True and self.cell[row][col].b_mine == True:
            return True
        else:
            return False

    def GetNearMineNumber(self, row, col):
        if self.IsInBoard(row, col) == True and self.cell[row][col].b_opend == True:
            return self.cell[row][col].near_mines
        else:
            return 9 # a number that is impossible

    def GetNearOpenedCellNumber(self, row, col):        
        if self.IsInBoard(row, col) == True :
            result = 0
            for offset in self.near_idx:
                row_tmp = row + offset[0]
                col_tmp = col + offset[1]
                if self.IsInBoard(row_tmp, col_tmp) == True and self.cell[row_tmp][col_tmp].b_opend == True:
                    result = result + 1
            return result
        else:
            return 9 # a number that is impossible

    def GetKnownMinesAroundCell(self, row, col):
        if self.IsInBoard(row, col) == True:
            near_mines = 0
            for offset in self.near_idx:
                row_tmp = row + offset[0]
                col_tmp = col + offset[1]
                if self.IsMine(row_tmp, col_tmp) == True:
                    near_mines = near_mines + 1
            return near_mines
        else:
            return 9 # a number that is impossible