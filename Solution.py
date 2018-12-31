from Mine import Cell, GameBoard
import random, math

board = GameBoard(20)

# start cell idx
row = math.floor(random.random() * board.GetWidth())
col = math.floor(random.random() * board.GetWidth())

board.Sweep(row, col)
if board.GetNearMineNumber(row, col) == board.GetKnownMinesAroundCell(row, col):
    board.Sweep(row, col)
else:
    row = math.floor(random.random() * board.GetWidth())
    col = math.floor(random.random() * board.GetWidth())