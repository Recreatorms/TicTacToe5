import numpy as np
from typing import Tuple
from functools import cache

import constants


@cache
def check_win(
    board: Tuple[Tuple[int, ...], ...],
    player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
    board_size: int,
    win_condition: int,
):

    print("Check win")

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
    board_array = np.array(board)  # Преобразование списка в массив NumPy
    for i in range(board_size):
        for j in range(board_size - (win_condition - 1)):
            if np.all(board_array[i, j : j + win_condition] == player):
                return True
    return False


@cache
def check_vertical(
    board: Tuple[Tuple[int, ...], ...],
    player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
    board_size: int,
    win_condition: int,
):
    board_array = np.array(board)  # Преобразование списка в массив NumPy
    for i in range(board_size):
        for j in range(board_size - (win_condition - 1)):
            if np.all(board_array[j : j + win_condition, i] == player):
                return True
    return False


@cache
def check_diagonal(
    board: Tuple[Tuple[int, ...], ...],
    player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
    board_size: int,
    win_condition: int,
):
    board_array = np.array(board)  # Преобразование списка в массив NumPy

    for i in range(board_size - (win_condition - 1)):
        for j in range(board_size - (win_condition - 1)):
            if np.all(np.diagonal(board_array, offset=i)[j : j + win_condition] == player):
                return True
    return False


@cache
def check_anti_diagonal(
    board: Tuple[Tuple[int, ...], ...],
    player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
    board_size: int,
    win_condition: int,
):
    board_array = np.array(board)  # Преобразование списка в массив NumPy

    for i in range(board_size - (win_condition - 1)):
        for j in range(board_size - (win_condition - 1)):
            if np.all(
                np.diagonal(np.fliplr(board_array), offset=i)[j : j + win_condition] == player
            ):
                return True
    return False


@cache
def is_board_full(board: Tuple[Tuple[int, ...], ...]):
    board_array = np.array(board)
    return np.all(board_array != constants.EMPTY)


# 0.55 секунд без кэша
# 0.015 секунд с кэшом
def transform_board(
    board: Tuple[Tuple[int, ...], ...],
    row: int,
    col: int,
    player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
):
    # Преобразование кортежа в массив NumPy
    board_array = np.array(board)

    # Обновление значения в позиции [row][col]
    board_array[row][col] = player

    # Преобразование массива NumPy обратно в кортеж
    board_tuple = tuple(map(tuple, board_array))

    return board_tuple


# Execution time: 1.9675756320011715
# Функция для получения всех возможных ходов
def get_available_moves(board: Tuple[Tuple[int, ...], ...]):
    board_array = np.array(board)
    available_moves = np.argwhere(board_array == constants.EMPTY)
    return tuple(map(tuple, available_moves))
