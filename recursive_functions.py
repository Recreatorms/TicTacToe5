# import numpy as np
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

    ok = check_horizontal(board, player, board_size, win_condition)
    if ok:
        print("Horizontal")
        return True
    ok = check_vertical(board, player, board_size, win_condition)
    if ok:
        print("Vertical")
        return True
    ok = check_diagonal(board, player, board_size, win_condition)
    if ok:
        print("Diagonal")
        return True
    ok = check_anti_diagonal(board, player, board_size, win_condition)
    if ok:
        print("AntiDiagonal")
        return True
    return False


@cache
def check_horizontal(
    board: Tuple[Tuple[int, ...], ...],
    player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
    board_size: int,
    win_condition: int,
    row: int = 0,
    col: int = 0,
    consecutive_count: int = 0,
) -> bool:
    if consecutive_count == win_condition:
        return True

    if col > board_size - win_condition:
        return False

    if row < board_size:
        if board[row][col] == player:
            consecutive_count += 1
        else:
            consecutive_count = 0
        return check_horizontal(
            board, player, board_size, win_condition, row, col + 1, consecutive_count
        )

    return check_horizontal(board, player, board_size, win_condition, 0, col + 1, consecutive_count)


@cache
def check_vertical(
    board: Tuple[Tuple[int, ...], ...],
    player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
    board_size: int,
    win_condition: int,
    row: int = 0,
    col: int = 0,
    consecutive_count: int = 0,
) -> bool:
    if consecutive_count == win_condition:
        return True

    if row > board_size - win_condition:
        return False

    if col < board_size:
        if board[row][col] == player:
            consecutive_count += 1
        else:
            consecutive_count = 0
        return check_vertical(
            board, player, board_size, win_condition, row, col + 1, consecutive_count
        )

    return check_vertical(board, player, board_size, win_condition, row + 1, 0, consecutive_count)


@cache
def check_diagonal(
    board: Tuple[Tuple[int, ...], ...],
    player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
    board_size: int,
    win_condition: int,
    row: int = 0,
    col: int = 0,
    consecutive_count: int = 0,
) -> bool:
    if consecutive_count == win_condition:
        return True

    if row > board_size - win_condition or col > board_size - win_condition:
        return False

    if row < board_size and col < board_size:
        if board[row][col] == player:
            consecutive_count += 1
        else:
            consecutive_count = 0
        return check_diagonal(
            board, player, board_size, win_condition, row + 1, col + 1, consecutive_count
        )

    return check_diagonal(board, player, board_size, win_condition, row + 1, 0, consecutive_count)


@cache
def check_anti_diagonal(
    board: Tuple[Tuple[int, ...], ...],
    player: constants.PLAYER_X | constants.PLAYER_O | constants.EMPTY,
    board_size: int,
    win_condition: int,
    row: int = 0,
    col: int = 0,
    consecutive_count: int = 0,
) -> bool:
    if consecutive_count == win_condition:
        return True

    if row > board_size - win_condition or col > board_size - win_condition:
        return False

    if row < board_size and col < board_size:
        if board[row][col + (win_condition - 1) - row] == player:
            consecutive_count += 1
        else:
            consecutive_count = 0
        return check_anti_diagonal(
            board, player, board_size, win_condition, row + 1, col + 1, consecutive_count
        )

    return check_anti_diagonal(
        board, player, board_size, win_condition, row + 1, 0, consecutive_count
    )
