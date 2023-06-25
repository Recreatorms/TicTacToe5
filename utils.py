import numpy as np
from typing import Tuple
from functools import cache
import constants
from numba import jit
from timeit import timeit


@jit(nopython=True)
def print_board(board):
    print("board:")
    for row in board:
        print(row)


@jit(nopython=True)
def getRelativePos(x, y):
    i = y // constants.CELL_SIZE
    j = x // constants.CELL_SIZE
    return i, j


# @cache
# def undo_move(
#     board: Tuple[Tuple[int, ...], ...],
#     move,
# ):
#     row, col = move
#     new_board = copy.deepcopy(board)  # Создаем копию доски
#     # Проверяем, что указанный ход допустим
#     if new_board[row][col] != constants.EMPTY:
#         raise ValueError("Invalid move: position already occupied")
#     new_board = np_f.transform_board(new_board, row, col, constants.EMPTY)
#     return new_board
