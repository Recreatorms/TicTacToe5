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

@cache
def getOppositePlayer(aiPlayer):
    if aiPlayer == constants.PLAYER_O:
        return constants.PLAYER_X
    else:
        return constants.PLAYER_O
