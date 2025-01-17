# Importar las librerías necesarias
import pygame
import random
from pygame.locals import *  # Importar constantes de eventos y teclas
import subprocess  # Para ejecutar el archivo 'main.py'
from time import sleep  # Para pausas en el código si es necesario

# Dimensiones de la ventana de juego
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

# Definición de colores utilizando el formato RGB
WHITE = (255, 255, 255)
HIGHLIGHT = (255, 215, 0)  # Color para resaltar elementos
BACKGROUND = (20, 20, 40)  # Color de fondo oscuro
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BOARD_COLOR_1 = (240, 217, 181)  # Color claro para las casillas del tablero
BOARD_COLOR_2 = (181, 136, 99)   # Color oscuro para las casillas del tablero
GRAY = (30, 30, 30)
BAR_COLOR = (70, 130, 180)  # Color de la barra de progreso

# Función para cargar los sonidos de la aplicación
def load_sounds():
    pygame.mixer.init()  # Inicializar el mezclador de sonidos
    pygame.mixer.music.load("assets/menu_music.mp3")  # Cargar música de fondo
    pygame.mixer.music.set_volume(0.5)  # Establecer el volumen de la música de fondo
    select_sound = pygame.mixer.Sound("assets/select.wav")  # Sonido de selección de opción
    move_sound = pygame.mixer.Sound("assets/navigate.wav")  # Sonido de navegación entre opciones
    return select_sound, move_sound  # Retornar los sonidos para ser usados en el menú

# Clase para crear partículas que simulan un fondo dinámico
class Particle:
    def __init__(self, x, y, size, color, speed):
        self.x = x  # Coordenada X de la partícula
        self.y = y  # Coordenada Y de la partícula
        self.size = size  # Tamaño de la partícula
        self.color = color  # Color de la partícula
        self.speed = speed  # Velocidad de movimiento de la partícula

    def update(self):
        # Actualizar la posición de la partícula (mueve hacia abajo)
        self.y += self.speed
        if self.y > DISPLAY_HEIGHT:  # Si la partícula se sale de la pantalla, se reinicia en la parte superior
            self.y = -self.size
            self.x = random.randint(0, DISPLAY_WIDTH)  # Posicionar en una posición aleatoria en X

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)  # Dibujar la partícula

# Función para mostrar la pantalla de carga con un logo
def show_loading_screen(logo_path):
    pygame.display.set_caption("Cargando Damas...")  # Establecer el título de la ventana
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))  # Crear la ventana
    clock = pygame.time.Clock()  # Controlar el tiempo de refresco de la pantalla

    # Cargar el logo y redimensionarlo
    logo = pygame.image.load(logo_path)
    logo = pygame.transform.scale(logo, (300, 300))

    progress = 0  # Progreso inicial
    max_progress = 100  # El progreso máximo será 100%
    bar_width = 400  # Ancho de la barra de progreso
    bar_height = 20  # Alto de la barra de progreso
    bar_x = (DISPLAY_WIDTH - bar_width) // 2  # Centrar la barra en X
    bar_y = DISPLAY_HEIGHT - 100  # Posicionar la barra cerca del fondo de la pantalla
    alpha_direction = 1  # Dirección de la transparencia
    alpha = 0  # Transparencia inicial

    # Colores de gradiente para el fondo
    gradient_start = (30, 30, 30)
    gradient_end = (70, 130, 180)

    # Bucle de carga
    while progress < max_progress:
        for event in pygame.event.get():  # Comprobar eventos
            if event.type == QUIT:
                pygame.quit()
                quit()

        # Crear un fondo de gradiente
        gradient_colors = [
            [
                gradient_start[i] + (gradient_end[i] - gradient_start[i]) * y // DISPLAY_HEIGHT
                for i in range(3)
            ]
            for y in range(DISPLAY_HEIGHT)
        ]
        for y, color in enumerate(gradient_colors):
            pygame.draw.line(screen, color, (0, y), (DISPLAY_WIDTH, y))

        # Mostrar el logo
        screen.blit(logo, (DISPLAY_WIDTH // 2 - 150, DISPLAY_HEIGHT // 2 - 200))

        # Animar la transparencia del texto "Cargando..."
        alpha += alpha_direction * 5
        if alpha >= 255 or alpha <= 0:
            alpha_direction *= -1
        font = pygame.font.SysFont("Arial", 30, bold=True)
        text_surface = font.render("Cargando...", True, WHITE)
        text_surface.set_alpha(alpha)
        screen.blit(text_surface, (DISPLAY_WIDTH // 2 - text_surface.get_width() // 2, DISPLAY_HEIGHT - 150))

        # Dibujar la barra de progreso
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, BAR_COLOR, (bar_x, bar_y, (progress / max_progress) * bar_width, bar_height))

        progress += 1  # Aumentar el progreso
        pygame.display.flip()  # Actualizar la pantalla
        clock.tick(60)  # Limitar el refresco a 60 FPS

    fade_out(screen, clock)  # Desvanecer la pantalla al terminar la carga

# Función para realizar un desvanecimiento de la pantalla
def fade_out(screen, clock):
    fade_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))  # Crear una superficie para el desvanecimiento
    fade_surface.fill(BLACK)  # Rellenarla de negro
    for alpha in range(0, 255, 5):  # Incrementar la transparencia en pasos
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))  # Dibujar la superficie sobre la pantalla
        pygame.display.flip()
        clock.tick(30)  # Limitar el refresco a 30 FPS

# Función para dibujar el tablero de damas
def draw_checkers_board(screen):
    tile_size = DISPLAY_WIDTH // 8  # Calcular el tamaño de cada casilla
    for row in range(8):  # Recorrer filas
        for col in range(8):  # Recorrer columnas
            # Determinar el color de la casilla en base a su posición
            color = BOARD_COLOR_1 if (row + col) % 2 == 0 else BOARD_COLOR_2
            pygame.draw.rect(screen, color, (col * tile_size, row * tile_size, tile_size, tile_size))  # Dibujar la casilla

# Función para mostrar el menú principal
def show_menu():
    pygame.display.set_caption("Menú Principal")  # Establecer el título de la ventana
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))  # Crear la ventana
    clock = pygame.time.Clock()  # Controlar el tiempo de refresco

    pygame.font.init()  # Inicializar las fuentes
    title_font = pygame.font.SysFont("Arial", 60, bold=True)  # Fuente para el título
    option_font = pygame.font.SysFont("Arial", 40)  # Fuente para las opciones
    small_option_font = pygame.font.SysFont("Arial", 30)  # Fuente para las opciones pequeñas

    selected = 0  # Opción seleccionada por defecto
    options = ["Jugador 1 vs Jugador 2", "Jugador 1 vs IA", "Salir"]  # Opciones del menú

    select_sound, move_sound = load_sounds()  # Cargar los sonidos
    pygame.mixer.music.play(-1)  # Reproducir la música de fondo de forma continua

    # Crear partículas para el fondo dinámico
    particles = [Particle(random.randint(0, DISPLAY_WIDTH), random.randint(0, DISPLAY_HEIGHT),
                          random.randint(10, 15), random.choice([RED, BLACK]), random.uniform(1, 3)) for _ in range(30)]

    while True:  # Bucle principal del menú
        for event in pygame.event.get():  # Comprobar eventos
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:  # Comprobar las teclas presionadas
                if event.key == K_UP:  # Mover hacia arriba
                    selected = (selected - 1) % len(options)
                    move_sound.play()  # Reproducir sonido de movimiento
                elif event.key == K_DOWN:  # Mover hacia abajo
                    selected = (selected + 1) % len(options)
                    move_sound.play()  # Reproducir sonido de movimiento
                elif event.key == K_RETURN:  # Seleccionar opción
                    select_sound.play()  # Reproducir sonido de selección
                    if selected == 0 or selected == 1:  # Si se selecciona una opción de juego, ejecutar 'main.py'
                        subprocess.run(["python", "main.py"])
                    elif selected == 2:  # Si se selecciona "Salir", cerrar el juego
                        pygame.quit()
                        quit()

        draw_checkers_board(screen)  # Dibujar el tablero de damas

        for particle in particles:  # Actualizar y dibujar las partículas
            particle.update()
            particle.draw(screen)

        title_surface = title_font.render("¡Bienvenido a Damas!", True, HIGHLIGHT)  # Renderizar el título
        screen.blit(title_surface, (DISPLAY_WIDTH // 2 - title_surface.get_width() // 2, 50))  # Dibujar el título

        # Dibujar las opciones del menú
        for i, option in enumerate(options):
            color = HIGHLIGHT if i == selected else WHITE  # Resaltar la opción seleccionada
            font = option_font if i == selected else small_option_font  # Cambiar la fuente si está seleccionada
            text_surface = font.render(option, True, color)
            screen.blit(text_surface, (DISPLAY_WIDTH // 2 - text_surface.get_width() // 2, 200 + i * 80))

        pygame.display.flip()  # Actualizar la pantalla
        clock.tick(60)  # Limitar el refresco a 60 FPS

# Función principal que inicializa el juego
def main():
    pygame.init()  # Inicializar pygame
    show_loading_screen("assets/logo.png")  # Mostrar la pantalla de carga
    show_menu()  # Mostrar el menú principal

# Si el script se ejecuta directamente, ejecutar la función main
if __name__ == "__main__":
    main()
