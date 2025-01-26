import math

G_TABLERO = []
G_POSICIONES_JUGADOR = []
G_POSICIONES_IA = []

IA = (2, 4)
JUGADOR = (1, 3)

G_COLUMNAS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# Representación del tablero
def preparar_juego() -> None:
    global G_TABLERO, G_POSICIONES_JUGADOR, G_POSICIONES_IA

    G_POSICIONES_JUGADOR = [
        ('A', 0, False),
        ('C', 0, False),
        ('E', 0, False),
        ('G', 0, False),
        ('B', 1, False),
        ('D', 1, False),
        ('F', 1, False),
        ('H', 1, False)]

    G_POSICIONES_IA = [
        ('B', 7, False),
        ('D', 7, False),
        ('F', 7, False),
        ('H', 7, False),
        ('A', 6, False),
        ('C', 6, False),
        ('E', 6, False),
        ('G', 6, False)]

    G_TABLERO = [
        # A B  C  D  E  F  G  H
        [1, 0, 1, 0, 1, 0, 1, 0],  # 0
        [0, 1, 0, 1, 0, 1, 0, 1],  # 1
        [0, 0, 0, 0, 0, 0, 0, 0],  # 2
        [0, 0, 0, 0, 0, 0, 0, 0],  # 3
        [0, 0, 0, 0, 0, 0, 0, 0],  # 4
        [0, 0, 0, 0, 0, 0, 0, 0],  # 5
        [2, 0, 2, 0, 2, 0, 2, 0],  # 6
        [0, 2, 0, 2, 0, 2, 0, 2],  # 7
    ]

# Imprimir el tablero con las coordenadas correspondientes (1-8 para las filas y a-h para las columnas)
def imprimir_tablero(ultimo_movimiento=None):
    print()
    for x in range(7, -1, -1):  # Filas de abajo hacia arriba (1 a 8)
        fila_str = f"\033[0m\033[90m{x + 1} \033[0m\033[1m"  # Etiqueta de fila (1 a 8)
        for y in range(8):  # Columnas de izquierda a derecha (a a h)
            if ultimo_movimiento and (x, y) == ultimo_movimiento[1]:
                # Resaltar el último movimiento en verde
                fila_str += f"\033[92m{str(G_TABLERO[x][y])}\033[0m\033[1m "
            elif G_TABLERO[x][y] == 1:
                # Ficha del jugador en rojo
                fila_str += f"\033[91m{str(G_TABLERO[x][y])}\033[0m\033[1m "
            elif G_TABLERO[x][y] == 2:
                # Ficha de la IA en azul
                fila_str += f"\033[94m{str(G_TABLERO[x][y])}\033[0m\033[1m "
            else:
                fila_str += str(G_TABLERO[x][y]) + " "
        print(fila_str)
    print("\033[0m\033[90m  A B C D E F G H\033[0m\n")  # Imprimir etiquetas de columnas (horizontal)

# Obtener coordenada en formato 'letra, número'
def obtener_coordenada(x, y):
    return f"({G_COLUMNAS[y]},{x + 1})"

# Movimiento válido
# TODO - Modificar el movimiento válido para permitir movimiento hacia atrás si es una reina
def movimiento_valido(tablero, origen, destino):
    x1, y1 = origen
    x2, y2 = destino
    if x2 < 0 or x2 >= 8 or y2 < 0 or y2 >= 8:
        return False
    if tablero[x2][y2] != 0:  # No se puede mover a una casilla ocupada
        return False

    dx, dy = abs(x2 - x1), abs(y2 - y1)

    # Si es una reina, puede moverse hacia atrás (jugador 1 tiene reina en valor 3 y jugador 2 en valor 4)
    if tablero[x1][y1] in (3, 4):  # Reina
        if dx == dy:  # Las reinas se mueven en diagonal, sin importar la dirección
            return True

    # Si no es una reina, solo se puede mover hacia adelante
    if tablero[x1][y1] == 1 and x2 > x1:  # Jugador 1 solo se mueve hacia abajo
        if dx == 1 and dy == 1:  # Movimiento simple
            return True
        if dx == 2 and dy == 2:  # Captura
            x_medio, y_medio = (x1 + x2) // 2, (y1 + y2) // 2
            if tablero[x_medio][y_medio] == 2:  # El enemigo está en la casilla intermedia
                return True
    elif tablero[x1][y1] == 2 and x2 < x1:  # Jugador 2 solo se mueve hacia arriba
        if dx == 1 and dy == 1:  # Movimiento simple
            return True
        if dx == 2 and dy == 2:  # Captura
            x_medio, y_medio = (x1 + x2) // 2, (y1 + y2) // 2
            if tablero[x_medio][y_medio] == 1:  # El enemigo está en la casilla intermedia
                return True

    return False

# Convertir a reina si llega a la última fila
def convertir_a_reina(tablero, x, y):
    if tablero[x][y] == 1 and x == 7:  # Jugador 1 llega a la fila 7
        tablero[x][y] = 3  # Marca la pieza como reina
    elif tablero[x][y] == 2 and x == 0:  # Jugador 2 llega a la fila 0
        tablero[x][y] = 4  # Marca la pieza como reina-

# Generar movimientos válidos
# TODO - Generar movimientos válidos, teniendo en cuenta si es una reina
def generar_movimientos(tablero, jugador):
    movimientos = []
    for x in range(8):
        for y in range(8):
            if tablero[x][y] == jugador or tablero[x][y] == (jugador + 2):  # Verifica si es una pieza o una reina
                for dx in [-1, 1]:  # Dirección en Y
                    for dy in [-1, 1]:  # Dirección en X
                        destino = (x + dx, y + dy)
                        if movimiento_valido(tablero, (x, y), destino):
                            movimientos.append(((x, y), destino))
                        # Añadir captura
                        captura = (x + 2 * dx, y + 2 * dy)
                        if movimiento_valido(tablero, (x, y), captura):
                            movimientos.append(((x, y), captura))
    return movimientos

# Aplicar movimiento y convertir a reina si corresponde
def hacer_movimiento(tablero, origen, destino):
    x1, y1 = origen
    x2, y2 = destino
    tablero[x2][y2] = tablero[x1][y1]
    tablero[x1][y1] = 0
    if abs(x2 - x1) == 2:  # Si es una captura, eliminar pieza
        x_medio, y_medio = (x1 + x2) // 2, (y1 + y2) // 2
        tablero[x_medio][y_medio] = 0

    # Convertir a reina si llega a la última fila
    convertir_a_reina(tablero, x2, y2)

# Evaluación del tablero
def evaluar_tablero(tablero):
    jugador_piezas = sum(fila.count(1) for fila in tablero)
    ia_piezas = sum(fila.count(2) for fila in tablero)
    return ia_piezas - jugador_piezas

# Minimax con poda alfa-beta
def minimax(tablero, profundidad, alfa, beta, maximizando):
    if profundidad == 0:
        return evaluar_tablero(tablero), None
    jugador = 2 if maximizando else 1
    movimientos = generar_movimientos(tablero, jugador)
    if not movimientos:
        return evaluar_tablero(tablero), None

    mejor_movimiento = None
    if maximizando:
        max_eval = -math.inf
        for movimiento in movimientos:
            nuevo_tablero = [fila[:] for fila in tablero]
            hacer_movimiento(nuevo_tablero, *movimiento)
            eval_actual, _ = minimax(nuevo_tablero, profundidad - 1, alfa, beta, False)
            if eval_actual > max_eval:
                max_eval = eval_actual
                mejor_movimiento = movimiento
            alfa = max(alfa, eval_actual)
            if beta <= alfa:
                break
        return max_eval, mejor_movimiento
    else:
        min_eval = math.inf
        for movimiento in movimientos:
            nuevo_tablero = [fila[:] for fila in tablero]
            hacer_movimiento(nuevo_tablero, *movimiento)
            eval_actual, _ = minimax(nuevo_tablero, profundidad - 1, alfa, beta, True)
            if eval_actual < min_eval:
                min_eval = eval_actual
                mejor_movimiento = movimiento
            beta = min(beta, eval_actual)
            if beta <= alfa:
                break
        return min_eval, mejor_movimiento

def es_valido(tablero, destino):
    x, y = destino
    return x in range(0, 8) and y in range(0, 8) and tablero[x][y] == 0  # Dentro del tablero y a una casilla vacía

def es_captura(tablero, turno, destino, vector) -> bool:
    # La posición anterior (según el vector de movimiento) debe ser del oponente
    return tablero[destino[0] - vector[0]][destino[1] - vector[1]] in JUGADOR if turno == IA else IA

# Filtrar movimientos de captura

def obtener_capturas(tablero, turno):  # Jugador = IA / JUGADOR

    # X es fila

    fichas = G_POSICIONES_JUGADOR if turno == JUGADOR else G_POSICIONES_IA
    opciones_x = [1] if turno == JUGADOR else [-1]  # Vertical (el horizontal siempre es -1 o 1)
    longitud = (2, 2)  # Min - max

    capturas = []

    for x_letra, y, reina in fichas:
        if reina:
            longitud = (2, 7)  # Min - max
            opciones_x = [1, -1]

        x = G_COLUMNAS.index(x_letra)
        print(x_letra, y, tablero[x][y])
        for dx in opciones_x:
            for dy in [-1, 1]:
                longitud_actual = longitud[0]
                while longitud_actual in range(longitud[0], longitud[1] + 1):  # Entre min y max longitud
                    destino = (x + (dx * longitud_actual), y + (dy * longitud_actual))
                    if es_valido(tablero, destino) and es_captura(tablero, turno, destino, (dx, dy)):
                        capturas.append(((y, x), destino))
                    longitud_actual += 1

    # TODO - Si se detectan varias capturas, ver si alguna de ellas lleva a otra
    return capturas

# Juego principal modificado
def jugar():
    preparar_juego()  # Y lo guarda en G_TABLERO
    turno_jugador = True
    ultimo_movimiento = None

    while True:
        imprimir_tablero(ultimo_movimiento)

        # Generar capturas prioritarias
        if turno_jugador:
            capturas = obtener_capturas(G_TABLERO, 1)
            if capturas:  # Si hay capturas, obligar al jugador a comer
                print("Tienes que capturar una pieza enemiga.")
                movimientos = capturas
            else:
                movimientos = generar_movimientos(G_TABLERO, 1)
        else:
            capturas = obtener_capturas(G_TABLERO, 2)
            if capturas:  # Si hay capturas, la IA debe comer
                movimientos = capturas
            else:
                movimientos = generar_movimientos(G_TABLERO, 2)

        # Fin del juego si no hay movimientos
        if not movimientos:
            ganador = "Jugador" if not turno_jugador else "IA"
            print(f"¡El juego ha terminado! Ganador: {ganador}")
            break

        # Turno del jugador
        if turno_jugador:
            print("Tu turno:")
            for i, mov in enumerate(movimientos):
                print(f"{i + 1}: {obtener_coordenada(*mov[0])} a {obtener_coordenada(*mov[1])}")
            eleccion = int(input("Selecciona tu movimiento: ")) - 1
            if eleccion < 0 or eleccion >= len(movimientos):
                print("Movimiento inválido, intenta de nuevo.")
                continue
            ultimo_movimiento = movimientos[eleccion]
            hacer_movimiento(G_TABLERO, *movimientos[eleccion])
        else:
            print("Turno de la IA:")
            _, mejor_movimiento = minimax(G_TABLERO, 3, -math.inf, math.inf, True)
            print(
                f"IA mueve de {obtener_coordenada(*mejor_movimiento[0])} a {obtener_coordenada(*mejor_movimiento[1])}")
            ultimo_movimiento = mejor_movimiento
            hacer_movimiento(G_TABLERO, *mejor_movimiento)

        turno_jugador = not turno_jugador

# Iniciar el juego
jugar()
