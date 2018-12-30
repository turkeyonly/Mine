import random

class Cell:
    def __init__(self, b_mine, near_mines_number):
        self.b_mine = b_mine
        self.near_mines = near_mines_number

class GameBoard:
    def __init__(self, mines_num):
        self.mines_num = mines_num
        width = 2 # the smallest width
        while width * width <= mines_num :
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
        mine_ratio = mines_num / (width * width)
        while mine_created < mines_num:            
            for i in range(width):
                for j in range(width):         
                    if mine_created < mines_num and random.random() >= mine_ratio:
                        self.cell[i][j].b_mine = True
                        mine_created = mine_created + 1            

        # generate the number around mines
        near_idx = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]] # near index offset, [row, col]
        for row in range(len(self.cell)):
            for col in range(len(self.cell[row])):
                if self.cell[row][col].b_mine == False:
                    near_mines = 0
                    for offset in near_idx:
                        row_tmp = row + offset[0]
                        col_tmp = col + offset[1]
                        if self.IsInBoard(row_tmp, col_tmp) == True and self.cell[row_tmp][col_tmp].b_mine == True:
                            near_mines = near_mines + 1
                    self.cell[row][col].near_mines = near_mines
    
    def IsInBoard(self, row, col):
        if row >= 0 and row < self.width and col >= 0 and col < self.width :
            return True
        else :
            return False

    def Print(self):
        for row in self.cell:
            for col in row:
                if col.b_mine == True:
                    print('*', end=' ')
                else:
                    print(col.near_mines, end=' ')
            print('')

GameBoard(50).Print()