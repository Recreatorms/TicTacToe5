import numpy as np
import pygame
import copy
from typing import Tuple
from functools import cache

import graphics
import constants
import utils

from minimax_iter import game_over, minimax
import python_functions as py_f

# import recursive_functions as recursive_f


# Функция для выбора оптимального хода для ИИ
@cache
def get_best_move(board: Tuple[Tuple[int, ...], ...]):
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
            newBoard = make_move(newBoard, move, constants.PLAYER_X)
        else:
            print("pos is blocked", (i, j))
    return newBoard


# Ход игрока
@cache
def player_move(board: Tuple[Tuple[int, ...], ...]):
    pygame.event.clear()
    event = pygame.event.wait()
    newBoard = board
    if event.type == pygame.K_ESCAPE:
        # print("player quitted")
        pass
    if event.type == pygame.MOUSEBUTTONDOWN:
        newBoard = handle_event(event, board)
    else:
        # print("waiting for player actions")
        pass
    if newBoard == board:
        newBoard = player_move(board)
    return newBoard


# Ход ИИ
@cache
def ai_move(board: Tuple[Tuple[int, ...], ...]):
    # Переключение на другого игрока
    tuple_board = tuple(map(tuple, board))  # Преобразование списка списков в кортеж
    best_move = get_best_move(tuple_board)
    # execution_time = timeit(lambda: get_best_move(tuple_board), globals=globals(), number=1)
    # print("AI: searching for bestmove took:", execution_time)
    newBoard = make_move(tuple_board, best_move, constants.PLAYER_O)
    return newBoard


# Рекурсивный игровой цикл
@cache
def game_loop_recursive(board: Tuple[Tuple[int, ...], ...]):
    print("player's turn")
    board = player_move(board)
    graphics.render_board(board)

    running = not game_over(board)
    print("Continue?", running)
    if running:
        print("ai's turn")
        board = ai_move(board)
        graphics.render_board(board)
        running = not game_over(board)
        print("Continue?", running)
        if running:
            return game_loop_recursive(board)

    return None


def main():
    # Инициализация Pygame и OpenGL
    graphics.setup()

    # Инициализация игрового поля
    board = np.full((constants.BOARD_SIZE, constants.BOARD_SIZE), constants.EMPTY)
    bufBoard = tuple(map(tuple, board))
    # initial board
    graphics.render_board(bufBoard)
    # Игровой цикл
    game_loop_recursive(bufBoard)
    # render game over window, retry button?
    pygame.quit()


if __name__ == "__main__":
    main()
