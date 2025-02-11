import pygame
import sys
import math
import subprocess

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pantalla Final - Juego de Damas")

# Colores
NEGRO = (10, 10, 30)
AZUL_OSCURO = (30, 100, 200)
GLOW = (100, 180, 255)
BLANCO = (255, 255, 255)

# Fuente personalizada
fuente_ganador = pygame.font.Font(None, 74)
fuente_boton = pygame.font.Font(None, 40)

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Variables para el efecto de gradiente animado
desplazamiento_gradiente = 0

# Variables para el efecto de luz dinámica
luz_radio = 50  # Radio del efecto de luz (reducido)
luz_intensidad = 50  # Intensidad del efecto de luz (reducido)

# Variables para el efecto de ondas
onda_amplitud = 20  # Altura de las ondas
onda_longitud = 100  # Longitud de onda
onda_velocidad = 2  # Velocidad de la animación
onda_desplazamiento = 0  # Desplazamiento de la onda

def dibujar_fondo_animado(mouse_x, mouse_y):
    """Dibuja un fondo con gradiente animado, ondas y un efecto de luz dinámica."""
    global desplazamiento_gradiente, onda_desplazamiento
    desplazamiento_gradiente += 0.5  # Velocidad del desplazamiento
    onda_desplazamiento += onda_velocidad  # Animación de las ondas

    # Dibujar gradiente animado
    for y in range(ALTO):
        factor = (y + desplazamiento_gradiente) % ALTO / ALTO
        r = int(10 + 20 * math.sin(factor * math.pi))  # Usar seno para variación suave
        g = int(10 + 20 * math.cos(factor * math.pi))
        b = int(30 + 50 * math.sin(factor * math.pi))

        # Asegurar que los valores estén dentro del rango 0-255
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))

        color = (r, g, b)
        pygame.draw.line(ventana, color, (0, y), (ANCHO, y))

    # Dibujar ondas animadas
    for x in range(0, ANCHO, 5):  # Dibujar líneas verticales cada 5 píxeles
        y_onda = ALTO // 2 + onda_amplitud * math.sin((x + onda_desplazamiento) / onda_longitud * 2 * math.pi)
        pygame.draw.line(ventana, GLOW, (x, y_onda), (x, ALTO), 2)

    # Efecto de luz dinámica que sigue al mouse
    for i in range(luz_intensidad):
        alpha = int(255 * (1 - i / luz_intensidad))  # Transparencia decreciente
        radio = luz_radio * (i / luz_intensidad)
        superficie_luz = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
        pygame.draw.circle(superficie_luz, (255, 255, 255, alpha), (radio, radio), radio)
        ventana.blit(superficie_luz, (mouse_x - radio, mouse_y - radio))

def mostrar_pantalla_final(ganador):
    """Pantalla final con diseño moderno y efectos espectaculares."""
    esperando = True

    while esperando:
        clock.tick(60)  # FPS altos para animaciones suaves

        # Obtener la posición del mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Actualizar fondo con gradiente animado, ondas y efecto de luz
        dibujar_fondo_animado(mouse_x, mouse_y)

        # Texto de victoria con efecto de resplandor sutil
        texto_ganador = fuente_ganador.render(f"¡{ganador} ha ganado!", True, GLOW)
        sombra_ganador = fuente_ganador.render(f"¡{ganador} ha ganado!", True, BLANCO)
        ventana.blit(sombra_ganador, (ANCHO // 2 - sombra_ganador.get_width() // 2 + 3, ALTO // 2 - 100 + 3))
        ventana.blit(texto_ganador, (ANCHO // 2 - texto_ganador.get_width() // 2, ALTO // 2 - 100))

        # Dibujar botón con efecto hover minimalista
        boton_x, boton_y, boton_ancho, boton_alto = ANCHO // 2 - 100, ALTO // 2 + 50, 200, 60

        # Animación del botón (hover y click)
        color_boton = AZUL_OSCURO if (boton_x <= mouse_x <= boton_x + boton_ancho and boton_y <= mouse_y <= boton_y + boton_alto) else GLOW
        pygame.draw.rect(ventana, color_boton, (boton_x, boton_y, boton_ancho, boton_alto), border_radius=15)

        # Texto del botón
        texto_boton = fuente_boton.render("Volver", True, BLANCO)
        ventana.blit(texto_boton, (boton_x + boton_ancho // 2 - texto_boton.get_width() // 2, boton_y + boton_alto // 2 - texto_boton.get_height() // 2))

        pygame.display.flip()  # Actualizar la pantalla

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_x <= mouse_x <= boton_x + boton_ancho and boton_y <= mouse_y <= boton_y + boton_alto:
                    esperando = False  # Salir del bucle y "volver al menú"

    subprocess.run(["python", "menu.py"])

# Ejecutar el código
if __name__ == "__main__":
    mostrar_pantalla_final("Jugador 1")
    pygame.quit()