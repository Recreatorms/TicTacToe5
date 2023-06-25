# реализация на итерации
#
#
#
#

import copy

from typing import Tuple
from functools import cache

import numpy_functions as np_f
import python_functions as py_f

import constants

# Функция для выбора оптимального хода для ИИ
@cache
def get_best_move_iter(board: Tuple[Tuple[int, ...], ...]):
    best_eval = float("-inf")
    best_move = None

    available_moves = py_f.get_available_moves(board)

    print("AI calculating best move...")
    for move in available_moves:
        row, col = move
        alpha = float("-inf")
        beta = float("inf")
        print("Checking move", move)
        new_board = copy.deepcopy(board)
        new_board = py_f.transform_board(new_board, row, col, constants.PLAYER_O)
        eval = minimax(new_board, constants.MAX_DEPTH, constants.PLAYER_X, alpha, beta)
        print("eval", eval)
        # new_board = py_f.transform_board(new_board, row, col, constants.EMPTY)
        if eval > best_eval:
            best_eval = eval
            best_move = move

    print("AI best move", best_move, "eval", best_eval)
    return tuple(best_move)


@cache
def minimax(
    board: Tuple[Tuple[int, ...], ...],
    depth: int,
    maximizing_player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
    alpha: float,
    beta: float,
):
    if depth == 0 or game_over(board):
        return evaluate(board)

    if maximizing_player == constants.PLAYER_O:
        best_eval = float("-inf")
    else:
        best_eval = float("inf")

    available_moves = py_f.get_available_moves(board)

    for move in available_moves:
        row, col = move

        # make move
        board = py_f.transform_board(board, row, col, maximizing_player)

        if maximizing_player == constants.PLAYER_O:
            eval = minimax(board, depth - 1, constants.PLAYER_X, alpha, beta)
            best_eval = max(best_eval, eval)
            alpha = max(alpha, best_eval)

        else:
            eval = minimax(board, depth - 1, constants.PLAYER_O, alpha, beta)
            best_eval = min(best_eval, eval)
            beta = min(beta, best_eval)

        # undo move
        board = py_f.transform_board(board, row, col, constants.EMPTY)
        if beta <= alpha:
            break

    return best_eval


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
