# реализация на итерации
#

from typing import Tuple
from functools import cache

import numpy_functions as np_f
import python_functions as py_f

import constants

# Функция оценки текущего состояния игры
@cache
def evaluate(board: Tuple[Tuple[int, ...], ...]):
    # print("Evaluating...")
    board_size = constants.BOARD_SIZE
    win_condition = constants.WIN_CONDITION
    if py_f.check_win(board, constants.PLAYER_X, board_size, win_condition):
        return -1
    elif py_f.check_win(board, constants.PLAYER_O, board_size, win_condition):
        return 1
    else:
        return 0


# Проверка наличия победителя или ничью
@cache
def game_over(board: Tuple[Tuple[int, ...], ...]):
    board_size = constants.BOARD_SIZE
    win_condition = constants.WIN_CONDITION
    # print("Game over?")

    if py_f.check_win(board, constants.PLAYER_X, board_size, win_condition):

        # print("Player X won")
        return True
    if py_f.check_win(board, constants.PLAYER_O, board_size, win_condition):

        # print("Player O won")
        return True
    if np_f.is_board_full(board):

        # print("Draw")
        return True
    return False


@cache
def minimax(
    board: Tuple[Tuple[int, ...], ...],
    depth: int,
    player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
    alpha: float,
    beta: float,
):
    if game_over(board):
        evaluated = evaluate(board)
        return evaluated
    if depth == 0:
        return evaluate(board)

    if player == constants.PLAYER_O:
        best_eval = float("-inf")
    else:
        best_eval = float("inf")

    available_moves = py_f.get_available_moves(board)

    for move in available_moves:
        row, col = move
        print("Player", player, "Checking move", move)

        board = py_f.transform_board(board, row, col, player)

        if player == constants.PLAYER_O:
            eval = minimax(board, depth - 1, constants.PLAYER_X, alpha, beta)
            best_eval = max(best_eval, eval)
            alpha = max(alpha, best_eval)
            if beta <= alpha:
                # print("Alpha beta cut")
                break
        else:
            eval = minimax(board, depth - 1, constants.PLAYER_O, alpha, beta)
            best_eval = min(best_eval, eval)
            beta = min(beta, best_eval)
            if beta <= alpha:
                # print("Alpha beta cut")
                break
        board = py_f.transform_board(board, row, col, constants.EMPTY)

    return best_eval
