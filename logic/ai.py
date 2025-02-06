
"""
def evaluar_estado(estado, jugador_actual, es_final, ganador, heuristica, todos_los_jugadores):
    
    Evalúa el estado del juego y devuelve un valor numérico que indica la ventaja para el jugador_actual.
    :param estado: Estado actual del juego.
    :param jugador_actual: Jugador para el cual se evalúa el estado.
    :param es_final: Función que determina si el estado es final.
    :param ganador: Función que indica si un jugador ha ganado.
    :param heuristica: Función heurística que estima la ventaja del estado.
    :param todos_los_jugadores: Lista de todos los jugadores.
    :return: math.inf si jugador_actual gana, -math.inf si pierde, 0 en empate, o heurística si el juego sigue.
   
    if es_final(estado):
        for jugador in todos_los_jugadores:
            if ganador(estado, jugador):
                return math.inf if jugador == jugador_actual else -math.inf
        return 0  # Empate o estado sin ganador

    return heuristica(estado, jugador_actual)


def minimax(estado, depth, movMax, jugadorMax, profundidadBusqueda, alpha, beta, estadosEvaluados,
            aplicar_movimiento, obtener_movimientos, es_estado_final, gana_jugador, heuristica, jugadores):
    
    movs = obtener_movimientos(estado)
    score = evaluar_estado(estado, jugadorMax, es_estado_final, gana_jugador, heuristica, jugadores)
    jugador = estado.jugadorActual
    newEstado = deepcopy(estado)

    if es_estado_final(estado):
        return (score - depth, movMax, estadosEvaluados)

    if depth <= profundidadBusqueda:
        if jugadorMax == jugador:  # Turno del jugador que maximiza
            best = -math.inf
            for mov in movs:
                s = aplicar_movimiento(newEstado, mov)
                value = minimax(s, depth + 1, movMax, jugadorMax, profundidadBusqueda, alpha, beta,
                                estadosEvaluados + 1, aplicar_movimiento, obtener_movimientos, 
                                es_estado_final, gana_jugador, heuristica, jugadores)
                
                if value[0] > best:
                    movMax = mov
                best = max(best, value[0])
                alpha = max(alpha, best)
                newEstado = deepcopy(estado)
                estadosEvaluados = value[2]
                
                if beta <= alpha:
                    break
            return (best, movMax, estadosEvaluados)
        else:  # Turno del jugador que minimiza
            best = math.inf
            for mov in movs:
                s = aplicar_movimiento(newEstado, mov)
                value = minimax(s, depth + 1, movMax, jugadorMax, profundidadBusqueda, alpha, beta,
                                estadosEvaluados + 1, aplicar_movimiento, obtener_movimientos, 
                                es_estado_final, gana_jugador, heuristica, jugadores)
                
                best = min(best, value[0])
                beta = min(beta, best)
                newEstado = deepcopy(estado)
                estadosEvaluados = value[2]
                
                if beta <= alpha:
                    break
            return (best, movMax, estadosEvaluados)
    else:
        return (score - depth, movMax, estadosEvaluados)

def ejecuta_minimax(estado, aplicar_movimiento, obtener_movimientos, es_estado_final, gana_jugador, heuristica,
                    numeroJugadores, profundidadBusqueda, estadisticas=False):
    
    t0 = time.time()
    alpha, beta = -math.inf, math.inf
    jugadorMax = estado.jugadorActual
    movs = obtener_movimientos(estado)
    newEstado = deepcopy(estado)
    jugadores = [i + 1 for i in range(numeroJugadores)]

    if len(movs) == 1:
        return movs[0]
    elif len(movs) == 0:
        return None
    else:
        valores = minimax(newEstado, 0, movs[0], jugadorMax, profundidadBusqueda, alpha, beta, 1,
                          aplicar_movimiento, obtener_movimientos, es_estado_final, gana_jugador, heuristica, jugadores)
        mov = valores[1]
        estadosEvaluados = valores[2]

    if estadisticas:
        print("\nTiempo de ejecución:", time.time() - t0)
        print("Número de estados evaluados:", estadosEvaluados)
    
    return mov
"""