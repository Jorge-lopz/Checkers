import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import * 
from math import cos, sin, pi
from OpenGL.GLUT import *
from pygame import mixer

#Crear menu
def show_menu():
    pygame.init()
    display = (640, 640)
    screen = pygame.display.set_mode(display)
    pygame.display.set_caption("Menú Principal")
    font = pygame.font.SysFont("Impact", 36)
    small_font = pygame.font.Font(None, 28)
    clock = pygame.time.Clock()

    # Colores
    bg_color = (20, 20, 20)
    button_color = (196, 83, 72)
    text_color = (255, 255, 255)
    
    # Cargar imágenes
    asset_path = "assets"  # Carpeta donde están las imágenes
    
    info_icon = pygame.image.load(os.path.join(asset_path, "informacion.png"))  # Icono de información
    info_icon = pygame.transform.scale(info_icon, (30, 30))  # Ajustar tamaño
    info_icon2 = pygame.image.load(os.path.join(asset_path, "negra.png"))  # Icono de información
    info_icon2 = pygame.transform.scale(info_icon2, (30, 30))  # Ajustar tamaño

    top_images = ["robot_rojo.png", "usuario_rojo.png"]  # Lista de imágenes
    bottom_image = pygame.image.load(os.path.join(asset_path, "usuario_blanco.png"))
    left_arrow = pygame.image.load(os.path.join(asset_path, "flecha_izq.png"))
    right_arrow = pygame.image.load(os.path.join(asset_path, "flecha.png"))
    
    # Redimensionar imágenes
    image_size = (150, 150)
    arrow_size = (50, 50)
    bottom_image = pygame.transform.scale(bottom_image, image_size)
    left_arrow = pygame.transform.scale(left_arrow, arrow_size)
    right_arrow = pygame.transform.scale(right_arrow, arrow_size)
    
    top_images = [pygame.transform.scale(pygame.image.load(os.path.join(asset_path, img)), image_size) for img in top_images]
    top_image_index = 0

    # Posición del icono de información
    info_icon_rect = info_icon.get_rect(topright=(display[0] - 20, 20))
    info_icon_rect2 = info_icon2.get_rect(topright=(display[0] - 20, 80))
    show_info_box = False  # Controlar la visibilidad del cuadro de información


    opacity = 255
    left_arrow_opacity = 255
    right_arrow_opacity = 255
    fading = False
    fade_direction = 0
    
    running = True
    while running:
        screen.fill(bg_color)

        # Dibujar el icono de información
        screen.blit(info_icon, info_icon_rect.topleft)
        screen.blit(info_icon2, info_icon_rect2.topleft)

        # Si el cursor está sobre el icono, mostrar el cuadro de información
        if show_info_box:
            draw_info_box(screen, small_font, info_icon_rect, "Spacebar  -  Pause")
            draw_info_box(screen, small_font, info_icon_rect2, "S  -  Mute")
        
        # Manejar animación de opacidad
        if fading:
            opacity -= 25
            if fade_direction == -1:
                left_arrow_opacity -= 25
            elif fade_direction == 1:
                right_arrow_opacity -= 25
            
            if opacity <= 0:
                opacity = 0
                if fade_direction == -1:
                    left_arrow_opacity = 0
                elif fade_direction == 1:
                    right_arrow_opacity = 0
                fading = False
                top_image_index = (top_image_index + fade_direction) % len(top_images)
        
        elif opacity < 255:
            opacity += 25
            if fade_direction == -1:
                left_arrow_opacity += 25
            elif fade_direction == 1:
                right_arrow_opacity += 25
            
            if opacity > 255:
                opacity = 255
                left_arrow_opacity = 255
                right_arrow_opacity = 255
        
        # Posicionar la imagen superior (centrada arriba)
        top_x = (display[0] - top_images[top_image_index].get_width()) // 2
        top_image = top_images[top_image_index].copy()
        top_image.fill((255, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(top_image, (top_x, 50))
        
        # Posicionar flechas a izquierda y derecha de la imagen superior con opacidad animada
        left_arrow_faded = left_arrow.copy()
        right_arrow_faded = right_arrow.copy()
        left_arrow_faded.fill((255, 255, 255, left_arrow_opacity), special_flags=pygame.BLEND_RGBA_MULT)
        right_arrow_faded.fill((255, 255, 255, right_arrow_opacity), special_flags=pygame.BLEND_RGBA_MULT)
        
        screen.blit(left_arrow_faded, (top_x - left_arrow.get_width() - 10, 50 + (top_images[top_image_index].get_height() // 2 - left_arrow.get_height() // 2)))
        screen.blit(right_arrow_faded, (top_x + top_images[top_image_index].get_width() + 10, 50 + (top_images[top_image_index].get_height() // 2 - right_arrow.get_height() // 2)))
        
        # Dibujar botón "Start"
        button_rect = pygame.Rect(display[0] // 2 - 100, display[1] // 2 - 30, 200, 60)
        pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
        text_surface = font.render("Start", True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
        
        # Posicionar la imagen inferior (centrada abajo)
        screen.blit(bottom_image, ((display[0] - bottom_image.get_width()) // 2, display[1] - bottom_image.get_height() - 50))
        
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEMOTION:
                # Comprobar si el cursor está sobre el icono de información
                show_info_box = info_icon_rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not fading:
                    fading = True
                    fade_direction = -1
                if event.key == pygame.K_RIGHT and not fading:
                    fading = True
                    fade_direction = 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):  # Si se hace clic en "Start"
                    if(top_image_index == 0): #Jugador vs IA
                        G_OPONENTE = 0
                    elif(top_image_index == 1): #Jugador vs Jugador
                        G_OPONENTE = 1
                    
                    running = False  # Sal del bucle para continuar
        
        pygame.display.flip()
        clock.tick(60)

    return "PVP" if G_OPONENTE == 1 else "PVC"

def draw_info_box(screen, font, icon_rect, info_text):
    """Dibuja un cuadro de información al pasar el ratón sobre el icono."""
    
    
    # Definir dimensiones del cuadro
    box_width, box_height = 200, 60
    box_x = icon_rect.x - box_width
    box_y = icon_rect.y + 10

    # Fondo del cuadro
    pygame.draw.rect(screen, (50, 50, 50), (box_x, box_y, box_width, box_height), border_radius=8)
    pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2, border_radius=8)

    # Dibujar texto
    text_surface = font.render(info_text, True, (255, 255, 255))
    screen.blit(text_surface, (box_x + 10, box_y + 15))
