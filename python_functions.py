from typing import Tuple
import constants
from functools import cache


# Функция для проверки победы игрока
@cache
def check_win(
    board: Tuple[Tuple[int, ...], ...],
    player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
    board_size: int,
    win_condition: int,
):
    return (
        check_horizontal(board, player, board_size, win_condition)
        or check_vertical(board, player, board_size, win_condition)
        or check_diagonal(board, player, board_size, win_condition)
        or check_anti_diagonal(board, player, board_size, win_condition)
    )


@cache
def check_horizontal(
    board: Tuple[Tuple[int, ...], ...],
    player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
    board_size: int,
    win_condition: int,
):
    for i in range(board_size):
        for j in range(board_size - (win_condition - 1)):
            if all(board[i][j + k] == player for k in range(win_condition)):
                return True
    return False


@cache
def check_vertical(
    board: Tuple[Tuple[int, ...], ...],
    player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
    board_size: int,
    win_condition: int,
):
    for i in range(board_size):
        for j in range(board_size - (win_condition - 1)):
            if all(board[j + k][i] == player for k in range(win_condition)):
                return True
    return False


@cache
def check_diagonal(
    board: Tuple[Tuple[int, ...], ...],
    player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
    board_size: int,
    win_condition: int,
):
    for i in range(board_size - (win_condition - 1)):
        for j in range(board_size - (win_condition - 1)):
            if all(board[i + k][j + k] == player for k in range(win_condition)):
                return True
    return False


@cache
def check_anti_diagonal(
    board: Tuple[Tuple[int, ...], ...],
    player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
    board_size: int,
    win_condition: int,
):
    for i in range(board_size - (win_condition - 1)):
        for j in range(board_size - (win_condition - 1)):
            if all(
                board[i + k][j + ((win_condition - 1) - k)] == player for k in range(win_condition)
            ):
                return True
    return False


# Функция для проверки заполненности игрового поля
@cache
def is_board_full(board: Tuple[Tuple[int, ...], ...]):
    for row in board:
        for cell in row:
            if cell == constants.EMPTY:
                return False
    return True


# 0.07 секунд без кэша
# 0.015 секунд с кэшом
@cache
def transform_board(board, row, col, player):
    board = list(map(list, board))  # Преобразование кортежа в список списков
    board[row][col] = player
    board = tuple(map(tuple, board))  # Преобразование списка списков обратно в кортеж
    return board


# Execution time: 0.2114115460008179
# быстрее чем реализация с NumPy
@cache
def get_available_moves(board: Tuple[Tuple[int, ...], ...]):
    available_moves = []
    for i in range(constants.BOARD_SIZE):
        for j in range(constants.BOARD_SIZE):
            if board[i][j] == constants.EMPTY:
                available_moves.append((i, j))
    return tuple(available_moves)
