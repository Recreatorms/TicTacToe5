import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import constants
from typing import Tuple

# Настройка OpenGL
def setup():
    pygame.init()
    pygame.display.set_mode((constants.WIDTH, constants.HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Tic Tac Toe")
    glViewport(0, 0, constants.WIDTH, constants.HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, constants.WIDTH, constants.HEIGHT, 0)
    glMatrixMode(GL_MODELVIEW)
    glLineWidth(5)  # Толщина линии
    glEnable(GL_LINE_SMOOTH)  # Включение сглаживания линий
    glLineStipple(1, 0xAAAA)  # Закругление концов линий
    glEnable(GL_LINE_STIPPLE)  # Включение пунктирного стиля линий


# Функция для отрисовки игрового поля
def render_board(board: Tuple[Tuple[int, ...], ...]):
    print("rendering board")
    for row in board:
        print(row)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    for i in range(constants.BOARD_SIZE):
        for j in range(constants.BOARD_SIZE):
            x = j * constants.CELL_SIZE
            y = i * constants.CELL_SIZE
            glColor3f(1.0, 1.0, 1.0)  # Белый цвет для пустых ячеек
            if board[i][j] != constants.EMPTY:
                glColor3f(0.9, 0.9, 0.9)  # Светло-серый цвет для заполненных ячеек

            draw_square(x, y)

    draw_markers(board)
    draw_grid()
    pygame.display.flip()


def draw_square(x, y):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + constants.CELL_SIZE, y)
    glVertex2f(x + constants.CELL_SIZE, y + constants.CELL_SIZE)
    glVertex2f(x, y + constants.CELL_SIZE)
    glEnd()


# Функция для отрисовки X и O
def draw_markers(board):
    for i in range(constants.BOARD_SIZE):
        for j in range(constants.BOARD_SIZE):
            if board[i][j] == constants.PLAYER_X:
                draw_x(i, j)
            elif board[i][j] == constants.PLAYER_O:
                draw_o(i, j)


# Функция для отрисовки X
def draw_x(i, j):
    x = (j + 0.5) * constants.CELL_SIZE
    y = (i + 0.5) * constants.CELL_SIZE
    size = constants.CELL_SIZE * 0.8

    glColor3f(1.0, 0.0, 0.0)  # Красный цвет
    glBegin(GL_LINES)
    glVertex2f(x - size / 2, y - size / 2)
    glVertex2f(x + size / 2, y + size / 2)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(x + size / 2, y - size / 2)
    glVertex2f(x - size / 2, y + size / 2)
    glEnd()


# Функция для отрисовки O
def draw_o(i, j):
    x = (j + 0.5) * constants.CELL_SIZE
    y = (i + 0.5) * constants.CELL_SIZE
    radius = constants.CELL_SIZE / 2
    radius_inner = 0.6 * radius
    radius_outer = 0.8 * radius
    sides = 100

    glBegin(GL_TRIANGLE_STRIP)
    glColor3f(0.2, 0.7, 0.2)  # Yellow color
    for i in range(sides + 1):
        angle = 2.0 * 3.1415926 * i / sides
        inner_x = x + radius_inner * math.cos(angle)
        inner_y = y + radius_inner * math.sin(angle)
        outer_x = x + radius_outer * math.cos(angle)
        outer_y = y + radius_outer * math.sin(angle)
        glVertex2f(inner_x, inner_y)
        glVertex2f(outer_x, outer_y)
    glEnd()


# Функция для отрисовки игровой сетки
def draw_grid():
    glColor3f(0.5, 0.5, 0.5)  # серый для линий сетки

    # Отрисовка вертикальных линий
    for i in range(1, constants.BOARD_SIZE):
        x = i * constants.CELL_SIZE
        glBegin(GL_LINES)
        glVertex2f(x, 0)
        glVertex2f(x, constants.HEIGHT)
        glEnd()

    # Отрисовка горизонтальных линий
    for j in range(1, constants.BOARD_SIZE):
        y = j * constants.CELL_SIZE
        glBegin(GL_LINES)
        glVertex2f(0, y)
        glVertex2f(constants.WIDTH, y)
        glEnd()
