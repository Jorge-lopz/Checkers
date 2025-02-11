import pygame

# Configuración inicial
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
MARGIN = 40  # Margen para etiquetas

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
DARK_BROWN = (101, 67, 33)
LIGHT_BROWN = (222, 184, 135)
YELLOW = (255, 255, 0)
CROWN_COLOR = (255, 255, 255)

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH + MARGIN, HEIGHT + MARGIN))
pygame.display.set_caption("Checkers")
font = pygame.font.SysFont(None, 30)

selected_piece = None
pieces = {}
original_colors = {}
kings = set()

# Función para dibujar el tablero
def draw_board():
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE + MARGIN, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    # Dibujar etiquetas de coordenadas
    letters = "ABCDEFGH"
    for i in range(COLS):
        text = font.render(letters[i], True, BLACK)
        screen.blit(text, (i * SQUARE_SIZE + MARGIN + SQUARE_SIZE//2 - text.get_width()//2, HEIGHT))
    for i in range(ROWS):
        text = font.render(str(ROWS - i), True, BLACK)
        screen.blit(text, (5, i * SQUARE_SIZE + SQUARE_SIZE//2 - text.get_height()//2))

# Función para dibujar las fichas
def draw_pieces():
    for (row, col), color in pieces.items():
        pygame.draw.circle(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE//2 + MARGIN, row * SQUARE_SIZE + SQUARE_SIZE//2), SQUARE_SIZE//3)
        if (row, col) in kings:
            pygame.draw.circle(screen, CROWN_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE//2 + MARGIN, row * SQUARE_SIZE + SQUARE_SIZE//2), SQUARE_SIZE//6)

# Inicializar piezas
def initialize_pieces():
    global pieces, original_colors
    for row in range(2):
        for col in range(COLS):
            if (row + col) % 2 == 1:
                pieces[(row, col)] = RED
                original_colors[(row, col)] = RED
    for row in range(ROWS-2, ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 1:
                pieces[(row, col)] = BLACK
                original_colors[(row, col)] = BLACK

# Manejo de clics
def handle_click(pos):
    global selected_piece
    x, y = pos
    col, row = (x - MARGIN) // SQUARE_SIZE, y // SQUARE_SIZE
    letters = "ABCDEFGH"
    
    if selected_piece:
        # Restaurar color de la pieza previamente seleccionada
        pieces[selected_piece] = original_colors[selected_piece]
        
    if (row, col) in pieces:
        selected_piece = (row, col)
        pieces[selected_piece] = YELLOW
    elif selected_piece:
        if abs(selected_piece[0] - row) == abs(selected_piece[1] - col):  # Movimiento diagonal libre
            pieces[row, col] = pieces.pop(selected_piece)
            original_colors[row, col] = original_colors.pop(selected_piece)
            
            # Imprimir el movimiento en consola
            start_pos = f"{letters[selected_piece[1]]}{ROWS - selected_piece[0]}"
            end_pos = f"{letters[col]}{ROWS - row}"
            print(f"Movimiento: {start_pos} -> {end_pos}")
            
            # Mantener la ficha como reina si ya era reina o si llega al otro extremo
            if selected_piece in kings or row == 0 or row == ROWS - 1:
                kings.add((row, col))
                print("se ha convertido en reina")
        selected_piece = None

initialize_pieces()

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())
    
    draw_board()
    draw_pieces()
    pygame.display.flip()

pygame.quit()