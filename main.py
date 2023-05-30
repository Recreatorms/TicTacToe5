import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Размер окна
WIDTH = 800
HEIGHT = 800

# Размер игрового поля
BOARD_SIZE = 10
CELL_SIZE = WIDTH // BOARD_SIZE

# Определение игроков
EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Функция для обновления игрового поля новым значением на заданной позиции
def update_board(board, i, j, value):
    if board[j][i] == EMPTY:
        return [[value if x == i and y == j else board[y][x] for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
    else:
        return board


# Функция для проверки победы игрока
def check_win(board, player):
    def check_horizontal():
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE - 4):
                if all(board[i][j + k] == player for k in range(5)):
                    return True
        return False

    def check_vertical():
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE - 4):
                if all(board[j + k][i] == player for k in range(5)):
                    return True
        return False

    def check_diagonal():
        for i in range(BOARD_SIZE - 4):
            for j in range(BOARD_SIZE - 4):
                if all(board[i + k][j + k] == player for k in range(5)):
                    return True
        return False

    def check_anti_diagonal():
        for i in range(BOARD_SIZE - 4):
            for j in range(BOARD_SIZE - 4):
                if all(board[i + k][j + 4 - k] == player for k in range(5)):
                    return True
        return False

    return check_horizontal() or check_vertical() or check_diagonal() or check_anti_diagonal()


# Функция для отрисовки игрового поля
def render_board(board):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            glColor3f(1.0, 1.0, 1.0)  # Белый цвет для пустых ячеек
            if board[j][i] != EMPTY:
                glColor3f(0.7, 0.7, 0.7)  # Светло-серый цвет для заполненных ячеек


            glBegin(GL_QUADS)
            glVertex2f(x, y)
            glVertex2f(x + CELL_SIZE, y)
            glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
            glVertex2f(x, y + CELL_SIZE)
            glEnd()

    draw_markers(board)
    draw_grid()
    pygame.display.flip()


# Функция для отрисовки X и O
def draw_markers(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[j][i] == PLAYER_X:
                draw_x(j, i)
            elif board[j][i] == PLAYER_O:
                draw_o(j, i)


# Функция для отрисовки X
def draw_x(i, j):
    glColor3f(0.8, 0.2, 0.2)  # Красный для X
    x = i * CELL_SIZE
    y = j * CELL_SIZE

    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(x + CELL_SIZE, y)
    glVertex2f(x, y + CELL_SIZE)
    glEnd()


# Функция для отрисовки O
def draw_o(i, j):
    glColor3f(0.2, 0.8, 0.2)  # Зелёный для O
    x = (i + 0.5) * CELL_SIZE
    y = (j + 0.5) * CELL_SIZE
    radius = CELL_SIZE / 2

    num_segments = 50
    theta = 2 * 3.1415926 / num_segments
    cos_theta = radius * math.cos(theta)
    sin_theta = radius * math.sin(theta)

    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)  # Центр
    for i in range(num_segments + 1):
        angle = i * theta
        px = x + radius * math.cos(angle)
        py = y + radius * math.sin(angle)
        glVertex2f(px, py)
    glEnd()


# Функция для отрисовки игровой сетки 
def draw_grid():
    glColor3f(0.5, 0.5, 0.5)  # серый для линий сетки

    # Отрисовка вертикальных линий
    for i in range(1, BOARD_SIZE):
        x = i * CELL_SIZE
        glBegin(GL_LINES)
        glVertex2f(x, 0)
        glVertex2f(x, HEIGHT)
        glEnd()

    # Отрисовка горизонтальных линий
    for j in range(1, BOARD_SIZE):
        y = j * CELL_SIZE
        glBegin(GL_LINES)
        glVertex2f(0, y)
        glVertex2f(WIDTH, y)
        glEnd()


# Игровой цикл
def game_loop(board, current_player, running):
    while running:
        render_board(board)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                i = x // CELL_SIZE
                j = y // CELL_SIZE
                # Обновление игрового поля в соответствии с текущей меткой игрока                
                if board[i][j] == EMPTY:
                    prevBoard = board
                    board = update_board(board, j, i, current_player)
                    

                    # Проверка на победу текущего игрока
                    if check_win(board, current_player):
                        print("Player", current_player, "wins!")
                        running = False
                    # Переключение на другого игрока
                    if prevBoard != board:
                        current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X


# Настройка OpenGL
def set_up_viewport():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, HEIGHT, 0)
    glMatrixMode(GL_MODELVIEW)


# Инициализация Pygame
pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
set_up_viewport()



# Инициализация игрового поля
board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
running = True
current_player = PLAYER_X

game_loop(board, PLAYER_X, running)

pygame.quit()
