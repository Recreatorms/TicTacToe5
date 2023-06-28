import numpy as np
import pygame
import copy
from typing import Tuple
from functools import cache

import graphics
import constants
import utils

# from minimax_iter import game_over, get_best_move_iter
from minimax_recurs import game_over, get_best_move_recurs

import python_functions as py_f

# import recursive_functions as recursive_f

aiPlayer = constants.PLAYER_X


@cache
def make_move(
    board: Tuple[Tuple[int, ...], ...], move, player: constants.PLAYER_X | constants.PLAYER_O
):
    row, col = move
    new_board = copy.deepcopy(board)  # Создаем копию доски
    # Проверяем, что указанный ход допустим
    if new_board[row][col] != constants.EMPTY:
        raise ValueError("Invalid move: position already occupied")
    new_board = py_f.transform_board(new_board, row, col, player)
    return new_board


# Обработка событий
def handle_event(event, board: Tuple[Tuple[int, ...], ...]):
    newBoard = board
    if event.type == pygame.QUIT:
        return None, False
    elif event.type == pygame.MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        i, j = utils.getRelativePos(x, y)
        # Обновление игрового поля в соответствии с текущей меткой игрока
        if newBoard[i][j] == constants.EMPTY:
            move = (i, j)
            print("player clicked at", move)
            newBoard = make_move(newBoard, move, utils.getOppositePlayer(aiPlayer))
        else:
            print("pos is blocked", (i, j))
    return newBoard


# Ход игрока
@cache
def player_move_recursive(board: Tuple[Tuple[int, ...], ...]):
    pygame.event.clear()
    event = pygame.event.wait()
    newBoard = board
    if event.type == pygame.K_ESCAPE:
        return None
    if event.type == pygame.MOUSEBUTTONDOWN:
        newBoard = handle_event(event, board)
    else:
        # print("waiting for player actions")
        pass
    if newBoard == board:
        newBoard = player_move_recursive(board)
    return newBoard


def player_move_iterative(board: Tuple[Tuple[int, ...], ...]):
    newBoard = copy.deepcopy(board)
    while newBoard == board:
        pygame.event.clear()
        event = pygame.event.wait()
        if event.type == pygame.K_ESCAPE:
            return None
        if event.type == pygame.MOUSEBUTTONDOWN:
            newBoard = handle_event(event, board)
        else:
            # print("waiting for player actions")
            pass
    return newBoard


# Ход ИИ
@cache
def ai_move(board: Tuple[Tuple[int, ...], ...]):
    # Переключение на другого игрока
    tuple_board = tuple(map(tuple, board))  # Преобразование списка списков в кортеж
    # best_move = get_best_move_iter(tuple_board)
    best_move = get_best_move_recurs(tuple_board, aiPlayer)

    newBoard = make_move(tuple_board, best_move, aiPlayer)
    return newBoard


# Рекурсивный игровой цикл
@cache
def game_loop_recursive(board: Tuple[Tuple[int, ...], ...]):

    if aiPlayer == constants.PLAYER_O:
        print("player's turn")
        board = player_move_iterative(board)
        if board == None:  # player pressed esc
            return None
    else:
        print("ai's turn")
        board = ai_move(board)
    graphics.render_board(board)

    running = not game_over(board)
    print("Continue?", running)
    if running:
        if aiPlayer == constants.PLAYER_O:
            print("ai's turn")
            board = ai_move(board)
        else:
            print("player's turn")
            board = player_move_iterative(board)
            if board == None:  # player pressed esc
                return None
        graphics.render_board(board)
        running = not game_over(board)
        print("Continue?", running)
        if running:
            return game_loop_recursive(board)

    return None


def main():
    # Инициализация Pygame и OpenGL
    graphics.setup()
    # sys.setrecursionlimit(10000000)
    # Инициализация игрового поля
    board = np.full((constants.BOARD_SIZE, constants.BOARD_SIZE), constants.EMPTY)
    bufBoard = tuple(map(tuple, board))
    # initial board
    graphics.render_board(bufBoard)
    # Игровой цикл
    game_loop_recursive(bufBoard)
    print("Game ended")
    # render game over window, retry button?
    pygame.quit()


if __name__ == "__main__":
    main()
