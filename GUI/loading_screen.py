import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import * 
from math import cos, sin, pi
from OpenGL.GLUT import *
from pygame import mixer


# Pantalla de carga 
def loading_screen_with_image(width, height, margin):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    loading = True
    progress = 0

    # Cargar la imagen
    logo = pygame.image.load("assets/logo.png")
    logo = pygame.transform.scale(logo, (200, 200))  # Ajustar el tamaño de la imagen si es necesario
    logo_rect = logo.get_rect(center=(width // 2, height // 2 - 50))

    while loading:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((0, 0, 0))  # Fondo negro

        # Mostrar la imagen centrada
        screen.blit(logo, logo_rect)

        # Dibujar la barra de carga con esquinas redondeadas
        bar_width = width  # Ancho total de la pantalla
        bar_height = 15  # Altura de la barra
        bar_x = 0  # Iniciar en el borde izquierdo
        bar_y = height - bar_height - 10  # Situar cerca del borde inferior con un margen de 10px
        border_radius = 5  # Radio para esquinas redondeadas

        # Fondo de la barra
        # Fondo marron 193, 188, 174
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), border_radius=border_radius)

        # Progreso de la barra
        #rojo - 196, 83, 72
        # marron - 109, 84, 77
        pygame.draw.rect(
            screen,
            (196, 83, 72),
            (bar_x, bar_y, progress * bar_width // 500, bar_height),
            border_radius=border_radius,
        )


        pygame.display.flip()
        clock.tick(500)

        progress += 1  # Incrementar progreso
        if progress > 500:  # Finalizar cuando llega al 100%
            loading = False

    # Esperar un momento antes de continuar
    pygame.time.wait(50)