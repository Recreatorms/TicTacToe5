# реализация на рекурсиях
# не работает из-за ограничения python

from typing import Callable, Tuple
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
        return find_best_move(board, depth, constants.PLAYER_X, alpha, beta, float("-inf"), max)
    else:
        return find_best_move(board, depth, constants.PLAYER_O, alpha, beta, float("inf"), min)


@cache
def find_best_move(
    board: Tuple[Tuple[int, ...], ...],
    depth: int,
    player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
    alpha: float,
    beta: float,
    best_eval: float,
    eval_func: Callable[[float, float], float],
):
    available_moves = py_f.get_available_moves(board)

    if not available_moves:
        return best_eval

    move = available_moves[0]
    row, col = move
    print("Player", player, "Checking move", move)

    board = py_f.transform_board(board, row, col, player)

    eval = minimax(board, depth - 1, get_opponent(player), alpha, beta)
    best_eval = eval_func(best_eval, eval)

    alpha = eval_func(alpha, best_eval)
    beta = eval_func(beta, best_eval)
    if beta <= alpha:
        return best_eval

    board = py_f.transform_board(board, row, col, constants.EMPTY)
    return find_best_move(board, depth, player, alpha, beta, best_eval, eval_func)


@cache
def get_opponent(player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY):
    if player == constants.PLAYER_X:
        return constants.PLAYER_O
    elif player == constants.PLAYER_O:
        return constants.PLAYER_X
    else:
        return constants.EMPTY
