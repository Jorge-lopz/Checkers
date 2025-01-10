import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import cos, sin

# Dimensiones del tablero
BOARD_SIZE = 8
SQUARE_SIZE = 1
THICKNESS = 0.3  # Grosor del tablero
BORDER_SIZE = 0.7  # Tamaño del borde

# Colores
LIGHT_BROWN = (0.980, 0.886, 0.651)  # Marrón claro
DARK_BROWN = (0.368, 0.220, 0.071)  # Marrón oscuro
BLACK = (0.0, 0.0, 0.0)
WHITE = (1, 1, 1)
RED = (0.7, 0.0, 0.0)  # Rojo para las piezas de damas
BASE_COLOR = (0.3, 0.2, 0.1)  # Color del grosor del tablero
BORDER_COLOR = (0.3, 0.2, 0.1)  # Color del borde

# Crear el tablero
def create_board():
    board = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Usamos marrón claro para las casillas blancas y marrón oscuro para las negras
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            board.append((row, col, color))
    return board

# Dibujar una casilla con cara inferior y contorno
def draw_square(row, col, color):
    # Casilla (cara superior)
    glColor3fv(color)
    glBegin(GL_QUADS)
    glVertex3f(col * SQUARE_SIZE, 0.001, row * SQUARE_SIZE)
    glVertex3f((col + 1) * SQUARE_SIZE, 0.001, row * SQUARE_SIZE)
    glVertex3f((col + 1) * SQUARE_SIZE, 0.001, (row + 1) * SQUARE_SIZE)
    glVertex3f(col * SQUARE_SIZE, 0.001, (row + 1) * SQUARE_SIZE)
    glEnd()

    # Cara inferior de la casilla
    glColor3fv(BASE_COLOR)
    glBegin(GL_QUADS)
    glVertex3f(col * SQUARE_SIZE, -THICKNESS, row * SQUARE_SIZE)
    glVertex3f((col + 1) * SQUARE_SIZE, -THICKNESS, row * SQUARE_SIZE)
    glVertex3f((col + 1) * SQUARE_SIZE, -THICKNESS, (row + 1) * SQUARE_SIZE)
    glVertex3f(col * SQUARE_SIZE, -THICKNESS, (row + 1) * SQUARE_SIZE)
    glEnd()

    # Contorno negro
    glColor3fv(BLACK)
    glBegin(GL_LINE_LOOP)
    glVertex3f(col * SQUARE_SIZE, 0, row * SQUARE_SIZE)
    glVertex3f((col + 1) * SQUARE_SIZE, 0, row * SQUARE_SIZE)
    glVertex3f((col + 1) * SQUARE_SIZE, 0, (row + 1) * SQUARE_SIZE)
    glVertex3f(col * SQUARE_SIZE, 0, (row + 1) * SQUARE_SIZE)
    glEnd()

# Dibujar una pieza de dama (cilindro de altura 0.15) con contorno
def draw_checker(row, col, color):
    glPushMatrix()
    # Posicionar la pieza en el centro de la casilla
    glTranslatef(col * SQUARE_SIZE + 0.5, 0, row * SQUARE_SIZE + 0.5)
    glColor3fv(color)

    # Crear un cilindro usando gluCylinder
    quadric = gluNewQuadric()
    glRotatef(-90, 1, 0, 0)  # Rotar para que el cilindro esté tumbado
    gluCylinder(quadric, 0.45, 0.45, 0.15, 32, 1)  # Cilindro con altura 0.15

    # Tapa superior
    glPushMatrix()
    glTranslatef(0, 0, 0.15)  # Subir la tapa a la parte superior del cilindro
    gluDisk(quadric, 0, 0.45, 32, 1)  # Dibujar disco superior
    glPopMatrix()

    # Tapa inferior
    gluDisk(quadric, 0, 0.45, 32, 1)  # Dibujar disco inferior

    # Contorno negro
    glColor3fv(BLACK)

    # Contorno superior (tumbado en el tablero)
    glBegin(GL_LINE_LOOP)
    for angle in range(0, 360, 5):
        rad = angle * 3.14159 / 180
        glVertex3f(0.45 * cos(rad), 0.45 * sin(rad), 0.15)  # Intercambiamos Y y Z y ajustamos la altura
    glEnd()

    glPopMatrix()

# Dibujar el tablero
def draw_board(board):
    draw_board_base()
    for row, col, color in board:
        draw_square(row, col, color)

# Dibujar la base del tablero
def draw_board_base():
    # Parte superior del borde
    glColor3fv(BORDER_COLOR)
    glBegin(GL_QUADS)
    glVertex3f(-BORDER_SIZE, 0, -BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, 0, -BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, 0, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(-BORDER_SIZE, 0, BOARD_SIZE + BORDER_SIZE)
    glEnd()

    # Parte inferior del borde
    glColor3fv(BASE_COLOR)
    glBegin(GL_QUADS)
    glVertex3f(-BORDER_SIZE, -THICKNESS, -BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, -THICKNESS, -BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, -THICKNESS, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(-BORDER_SIZE, -THICKNESS, BOARD_SIZE + BORDER_SIZE)
    glEnd()

    # Lados del borde
    glColor3fv(BORDER_COLOR)
    glBegin(GL_QUADS)
    # Lado frontal
    glVertex3f(-BORDER_SIZE, 0, -BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, 0, -BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, -THICKNESS, -BORDER_SIZE)
    glVertex3f(-BORDER_SIZE, -THICKNESS, -BORDER_SIZE)
    # Lado trasero
    glVertex3f(-BORDER_SIZE, 0, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, 0, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, -THICKNESS, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(-BORDER_SIZE, -THICKNESS, BOARD_SIZE + BORDER_SIZE)
    # Lado izquierdo
    glVertex3f(-BORDER_SIZE, 0, -BORDER_SIZE)
    glVertex3f(-BORDER_SIZE, 0, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(-BORDER_SIZE, -THICKNESS, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(-BORDER_SIZE, -THICKNESS, -BORDER_SIZE)
    # Lado derecho
    glVertex3f(BOARD_SIZE + BORDER_SIZE, 0, -BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, 0, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, -THICKNESS, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, -THICKNESS, -BORDER_SIZE)
    glEnd()

    # Contornos negros para el tablero y los laterales
    glColor3fv(BLACK)
    glBegin(GL_LINES)
    # Contorno superior
    glVertex3f(-BORDER_SIZE, 0, -BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, 0, -BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, 0, -BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, 0, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, 0, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(-BORDER_SIZE, 0, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(-BORDER_SIZE, 0, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(-BORDER_SIZE, 0, -BORDER_SIZE)

    # Contorno inferior
    glVertex3f(-BORDER_SIZE, -THICKNESS, -BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, -THICKNESS, -BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, -THICKNESS, -BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, -THICKNESS, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, -THICKNESS, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(-BORDER_SIZE, -THICKNESS, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(-BORDER_SIZE, -THICKNESS, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(-BORDER_SIZE, -THICKNESS, -BORDER_SIZE)

    # Contornos verticales (aristas de los laterales)
    glVertex3f(-BORDER_SIZE, 0, -BORDER_SIZE)
    glVertex3f(-BORDER_SIZE, -THICKNESS, -BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, 0, -BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, -THICKNESS, -BORDER_SIZE)
    glVertex3f(-BORDER_SIZE, 0, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(-BORDER_SIZE, -THICKNESS, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, 0, BOARD_SIZE + BORDER_SIZE)
    glVertex3f(BOARD_SIZE + BORDER_SIZE, -THICKNESS, BOARD_SIZE + BORDER_SIZE)
    glEnd()

# Configuración principal
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(30, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(-0.5, 0, -20)

    board = create_board()

    # Piezas de damas rojas y negras
    red_checkers = [(row, col) for row in range(0, 2) for col in range(row % 2, BOARD_SIZE, 2)]
    black_checkers = [(row, col) for row in range(6, 8) for col in range(row % 2, BOARD_SIZE, 2)]

    glEnable(GL_DEPTH_TEST)  # Activar prueba de profundidad para manejar correctamente las caras
    glDisable(GL_CULL_FACE)  # Desactivar el culling para que se vean todas las caras

    rotate_x, rotate_y = 35, 45
    mouse_down = False
    last_mouse_pos = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
                    last_mouse_pos = pygame.mouse.get_pos()

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False

            if event.type == MOUSEMOTION and mouse_down:
                current_mouse_pos = pygame.mouse.get_pos()
                dx = current_mouse_pos[0] - last_mouse_pos[0]
                dy = current_mouse_pos[1] - last_mouse_pos[1]
                rotate_x += dy * 0.5
                rotate_y += dx * 0.5
                last_mouse_pos = current_mouse_pos

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glTranslatef(BOARD_SIZE / 15, 0, BOARD_SIZE / 10)
        glRotatef(rotate_x, 1, 0, 0)
        glRotatef(rotate_y, 0, 1, 0)
        glTranslatef(-BOARD_SIZE / 2, 0, -BOARD_SIZE / 2)

        draw_board(board)

        # Dibujar las piezas de damas
        for row, col in red_checkers:
            draw_checker(row, col, RED)
        for row, col in black_checkers:
            draw_checker(row, col, BLACK)

        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
