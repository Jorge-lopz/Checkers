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

# Pantalla de carga
def loading_screen_with_image():
    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display)
    clock = pygame.time.Clock()
    loading = True
    progress = 0

    # Cargar la imagen
    logo = pygame.image.load("assets/logo.png")
    logo = pygame.transform.scale(logo, (200, 200))  # Ajustar el tamaño de la imagen si es necesario
    logo_rect = logo.get_rect(center=(display[0] // 2, display[1] // 2 - 50))

    while loading:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((0, 0, 0))  # Fondo negro

        # Mostrar la imagen centrada
        screen.blit(logo, logo_rect)

        # Dibujar la barra de carga con esquinas redondeadas
        bar_width = display[0]  # Ancho total de la pantalla
        bar_height = 15  # Altura de la barra
        bar_x = 0  # Iniciar en el borde izquierdo
        bar_y = display[1] - bar_height - 10  # Situar cerca del borde inferior con un margen de 10px
        border_radius = 5  # Radio para esquinas redondeadas

        # Fondo de la barra
        # Fondo marron 193, 188, 174
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), border_radius=border_radius)

        # Progreso de la barra
        # rojo - 196, 83, 72
        # marron - 109, 84, 77
        pygame.draw.rect(
            screen,
            (196, 83, 72),
            (bar_x, bar_y, progress * bar_width // 100, bar_height),
            border_radius=border_radius,
        )

        pygame.display.flip()
        clock.tick(30)

        progress += 1  # Incrementar progreso
        if progress > 100:  # Finalizar cuando llega al 100%
            loading = False

    # Esperar un momento antes de continuar
    pygame.time.wait(300)

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

# Restauracion suave
def lerp(current, target, t):
    return current + (target - current) * t

# Configuración principal
def main():
    loading_screen_with_image()
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(30, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(-0.5, 0, -20)

    board = create_board()

    # Piezas de damas rojas y negras
    red_checkers = [(row, col) for row in range(0, 2) for col in range((row + 1) % 2, BOARD_SIZE, 2)]
    black_checkers = [(row, col) for row in range(6, 8) for col in range((row + 1) % 2, BOARD_SIZE, 2)]


    glEnable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)

    rotate_x, rotate_y = 90, 0
    target_rotate_x, target_rotate_y = rotate_x, rotate_y
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
                    target_rotate_x, target_rotate_y = 90, 0

            if event.type == MOUSEMOTION and mouse_down:
                current_mouse_pos = pygame.mouse.get_pos()
                dx = current_mouse_pos[0] - last_mouse_pos[0]
                dy = current_mouse_pos[1] - last_mouse_pos[1]

                rotate_x += dy * 0.5
                rotate_x = max(-90, min(90, rotate_x))
                rotate_y += dx * 0.5

                last_mouse_pos = current_mouse_pos
                target_rotate_x, target_rotate_y = rotate_x, rotate_y

        if not mouse_down:
            rotate_x = lerp(rotate_x, target_rotate_x, 0.1)
            rotate_y = lerp(rotate_y, target_rotate_y, 0.1)

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