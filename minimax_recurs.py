# реализация на рекурсиях
# не работает из-за ограничения python
# если убрать ограничение
# sys.setrecursionlimit(1000000)
# то возникает segmentation fault

import copy

from typing import Tuple
from functools import cache

import numpy_functions as np_f
import python_functions as py_f

import constants

# Функция для выбора оптимального хода для ИИ
@cache
def get_best_move_recurs(board: Tuple[Tuple[int, ...], ...]):
    available_moves = py_f.get_available_moves(board)
    print("AI calculating best move...")
    best_move, best_eval = evaluate_moves_first(board, available_moves)
    print("AI best move", best_move, "eval", best_eval)
    return tuple(best_move)


@cache
def evaluate_moves_first(board, moves, best_eval=float("-inf"), best_move=None):
    if not moves:
        return best_move, best_eval
    else:
        move = moves[0]
        row, col = move
        alpha = float("-inf")
        beta = float("inf")
        new_board = copy.deepcopy(board)

        print("Checking move", move)
        new_board = py_f.transform_board(new_board, row, col, constants.PLAYER_O)

        eval = minimax(new_board, constants.MAX_DEPTH, constants.PLAYER_X, alpha, beta)

        new_board = py_f.transform_board(new_board, row, col, constants.EMPTY)
        print("eval", eval)
        if eval > best_eval:
            best_eval = eval
            best_move = move
        return evaluate_moves_first(new_board, moves[1:], best_eval, best_move)


@cache
def minimax(
    board: Tuple[Tuple[int, ...], ...],
    depth: int,
    maximizing_player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
    alpha: float,
    beta: float,
):
    # print(minimax.cache_info())
    if depth == 0 or game_over(board):
        return evaluate(board)

    if maximizing_player == constants.PLAYER_O:
        best_eval = float("-inf")
    else:
        best_eval = float("inf")

    available_moves = py_f.get_available_moves(board)

    return evaluate_moves(board, available_moves, depth, maximizing_player, best_eval, alpha, beta)


@cache
def evaluate_moves(board, moves, depth, maximizing_player, best_eval, alpha, beta):
    if not moves:
        return best_eval

    move = moves[0]
    remaining_moves = moves[1:]

    board, eval, new_alpha, new_beta = evaluate_move(
        board, move, depth, maximizing_player, best_eval, alpha, beta
    )

    if maximizing_player == constants.PLAYER_O:
        best_eval = max(best_eval, eval)
        alpha = max(new_alpha, best_eval)
        if beta <= alpha:
            return best_eval
    else:
        best_eval = min(best_eval, eval)
        beta = min(new_beta, best_eval)
        if beta <= alpha:
            return best_eval

    return evaluate_moves(board, remaining_moves, depth, maximizing_player, best_eval, alpha, beta)


@cache
def evaluate_move(board, move, depth, maximizing_player, best_eval, alpha, beta):
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
    return board, best_eval, alpha, beta


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
