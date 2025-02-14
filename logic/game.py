# --------------------------------------------------------------------------- #
#                                                                             #
#     game.py                                             +#######+           #
#                                                       +###########+         #
#     PROJECT: Checkers                       ·''''''''·#############         #
#     AUTHOR(S): IA Team                     '''''''''''+###########+         #
#                                            '''''''''''' +#######+           #
#     CREATED DATE: 30/01/2025               ''''''''''''                     #
#     LAST UPDATE: 30/01/2025                 `''''''''´                      #
#                                                                             #
# --------------------------------------------------------------------------- #

from copy import deepcopy
from colorama import init, Fore

init(autoreset=True)

# X (Fila - números), Y (Columnas - letras)
# Minimax tree root is 0, so odd depth nodes are generates by a IA move (and even by player move)

class Player:

    def __init__(self, opponent: bool, ia: bool = False):
        if ia and not opponent:
            raise Exception("IA has to be opponent")
        self.opponent: bool = opponent
        self.ia: bool = ia
        self.pieces = []

        if opponent:
            self.pieces = [
                Piece(self, 0, 1), 
                Piece(self, 0, 3),
                Piece(self, 0, 5),
                Piece(self, 0, 7),
                Piece(self, 1, 0),
                Piece(self, 1, 2),
                Piece(self, 1, 4),
                Piece(self, 1, 6)]
        else:
            self.pieces = [
                Piece(self, 7, 0),
                Piece(self, 7, 2),
                Piece(self, 7, 4),
                Piece(self, 7, 6),
                Piece(self, 6, 1),
                Piece(self, 6, 3),
                Piece(self, 6, 5),
                Piece(self, 6, 7)]

class Piece:

    queen: bool = False
    direction_x: tuple
    move_length: tuple = (1, 1)
    catch_length: tuple = (2, 2)
    symbol: str

    def __init__(self, player: Player, x: int, y: int):
        self.player = player
        self.x = x
        self.y = y
        # Other variables
        
        self.symbol = "2" if player.opponent else "1"
        self.direction_x = (1,) if self.player.opponent else (-1,)

    def set_queen(self):
        self.queen = True
        self.symbol = str(int(self.symbol) + 2)
        self.direction_x = (1, -1)
        self.move_length = (1, 7)
        self.catch_length = (2, 7)
        
    def get_catches(self, board: list, alt_origin = ()) -> list:
        """
        Returns a list of valid catches -> [((x_destiny, y_destiny), (x_catched, y_catched)),...]
        In case multiple pieces are caught consecutively, it will return a tuple with the concatenated catches
        [Recursive]
        """

        length = self.catch_length

        catches = []
        for dx in self.direction_x:
            for dy in (-1, 1):
                current_length = length[0] # Starts at min (2)
                while current_length in range(length[0], length[1] + 1):  # Between min and max length
                    destiny = (self.x + dx * current_length, self.y + dy * current_length)
                    # CHECK BOUNDS, VALID, AND CATCH
                    if not check_bounds(*destiny): break
                    if empty_cell(*destiny, board): 
                        # Check if it is an actual catch
                        catch_cell = (destiny[0] - 1 * dx, destiny[1] - 1 * dy)
                        catch_cell_piece = int(board[catch_cell[0]][catch_cell[1]])
                        if catch_cell_piece != 0 and catch_cell_piece % 2 == (0 if not self.player.opponent else 1): # Uses odd or even operations to check piece owner (1-3 / 2-4)
                            catches.append((destiny, catch_cell)) # Appends both the destiny position and the caught piece position
                        break
                    current_length += 1

        return catches if len(catches) > 0 else None
                        
    def get_moves(self, board: list) -> list | None:
        """
        Returns a list of valid moves for the piece -> [(x_destiny, y_destiny),...]
        """
        
        length = self.move_length
        
        moves = []
        for dx in self.direction_x:
            for dy in (-1, 1):
                current_length = length[0] # Starts at min (2)
                while current_length in range(length[0], length[1] + 1):  # Between min and max length
                    destiny = (self.x + dx * current_length, self.y + dy * current_length)
                    # CHECK BOUNDS AND EMPTY
                    if not check_bounds(*destiny): break 
                    if not empty_cell(*destiny, board): break
                    moves.append(destiny)
                    current_length += 1

        return moves if len(moves) > 0 else None

    def move(self, destiny: (int), catch: (int) = None):
        """
        Just moves without any check
        """
        global g_board

        # Board
        g_board[destiny[0]][destiny[1]] = self.symbol
        g_board[self.x][self.y] = 0
        if catch:
            g_board[catch[0]][catch[1]] = 0

        # Pieces
        self.x, self.y = destiny
        if catch:
            for piece in self.player.pieces:
                if (piece.x, piece.y) == catch:
                    del piece

        # Check if it's a queen after moving
        if (self.x == 0 and not self.player.opponent) or (self.x == 7 and self.player.opponent):
            self.set_queen()
   
# CHECKS #
def check_bounds(x: int, y: int) -> bool:
    """
    Check if coords are inside the board. 
    Returns True if inside the board, False otherwise
    """
    return 0 <= x < 8 and 0 <= y < 8

def empty_cell(x: int, y: int, board: list = None) -> bool:
    """
    Überprüfen Sie, ob die Zielzelle leer ist / check if the destination cell is empty
    """
    if(board == None):
        board = g_board
    return board[x][y] == 0

# UTILS #

def to_logic(coord, col: bool) -> int:
    return "ABCDEFGH".index(coord) if col else 8 - int(coord)

def to_visual(coord, col: bool) -> int:
    return "ABCDEFGH"[coord] if col else abs(coord - 8)

def printBoard(board):
    print(f"\n{Fore.LIGHTBLACK_EX}  + — — — — — — — — +")
    for fila in range(8):
        print(str(8 - fila) + f"{Fore.LIGHTBLACK_EX} |", end=" ")
        for columna in range(8):
            print(str(board[fila][columna])
                  .replace("0", "·")
                  .replace("1", f"{Fore.LIGHTCYAN_EX}○")
                  .replace("3", f"{Fore.LIGHTCYAN_EX}●")
                  .replace("2", f"{Fore.RED}○")
                  .replace("4", f"{Fore.RED}●")
                    + " ", end="")
        print(f"{Fore.LIGHTBLACK_EX}|")  
    print(f"{Fore.LIGHTBLACK_EX}  + — — — — — — — — +")
    print("    A B C D E F G H  \n")

g_board = [
    #A  B  C  D  E  F  G  H   # INDEX     VISUAL [abs(index - 8)]
    [0, 2, 0, 2, 0, 2, 0, 2], #   0    ->   8
    [2, 0, 2, 0, 2, 0, 2, 0], #   1    ->   7
    [0, 0, 0, 0, 0, 0, 0, 0], #   2    ->   6
    [0, 0, 0, 0, 0, 0, 0, 0], #   3    ->   5
    [0, 0, 0, 0, 0, 0, 0, 0], #   4    ->   4
    [0, 0, 0, 0, 0, 0, 0, 0], #   5    ->   3
    [0, 1, 0, 1, 0, 1, 0, 1], #   6    ->   2
    [1, 0, 1, 0, 1, 0, 1, 0]  #   7    ->   1
]

G_PLAYERS = {"player": Player(False)}

G_PLAYERS["opponent"] = Player(True, True) # Opponent and IA

# AI #

DEPTH_LIMIT = 1

class Node:

    def __init__(self, board, last_move, last_catch, depth, pieces_player: list, pieces_opponent: list):
        self.board = board
        self.last_move = last_move
        self.last_catch = last_catch
        self.depth = depth
        self.pieces_player = deepcopy(pieces_player)
        self.pieces_opponent = deepcopy(pieces_opponent)
        self.children = []
        
        # If depth is DEPTH_LIMIT, it is a leaf node (and dooesn't call the get_children funtion)
        if depth < DEPTH_LIMIT:
            self.get_children()

    def get_catches(self) -> dict | None:
        captures = {}  
        # Seleccionamos las piezas del jugador según el nivel de profundidad
        pieces = self.pieces_player if (self.depth % 2 == 1) else self.pieces_opponent

        # Itera sobre las piezas 
        for piece in pieces:
            # Si hay capturas válidas, las añade al diccionario
            moves = piece.get_catches(self.board)  
            if moves:
                captures[(piece.x, piece.y)] = piece.get_catches(self.board)  
    
        # Si no hay capturas válidas, devuelve None
        return captures if captures != {} else None  # {((x, y), (catched_x, catched_y)), ...}
            
    def get_moves(self) -> dict | None:
        moves = {}
        pieces = self.pieces_player if (self.depth % 2 == 1) else self.pieces_opponent
    
        for piece in pieces:
            if check_bounds(piece.x, piece.y):
                possible_moves = piece.get_moves(self.board)
                if possible_moves:
                    moves[(piece.x, piece.y)] = possible_moves
                    
        # Devuelve el diccionario o None si no hay movimientos
        return moves if moves !=  {} else None  # [(x, y), ...]

    def create_node(self, origin: (int), destiny: (int), capture: (int) = None):

        # Modify the board
        new_board = deepcopy(self.board)
        new_board[destiny[0]][destiny[1]] = new_board[origin[0]][origin[1]]
        new_board[origin[0]][origin[1]] = 0

        if capture:
            new_board[capture[0]][capture[1]] = 0

        pieces_player = deepcopy(self.pieces_player)
        pieces_opponent = deepcopy(self.pieces_opponent)

        # Modify the pieces
        pieces = self.pieces_player if (self.depth % 2 == 1) else self.pieces_opponent
        for piece in pieces: # Modify the correct piece
            if (piece.x, piece.y) == origin:
                piece.x = destiny[0]
                piece.y = destiny[1]
                if destiny[1] == 0 or destiny[1] == 7:  # If queen position
                    piece.set_queen()
                if not capture:
                    break
            if capture and (piece.x, piece.y) == capture:
                del piece
                capture = None
        return Node(new_board, (origin, destiny), capture, self.depth + 1, pieces_player, pieces_opponent) # Create a new node

    def get_children(self):
        childs = self.get_catches()
        if childs == None: # If no catches, call moves
            childs = self.get_moves()
            for origin, moves in childs.items():
                for move in moves:
                    self.children.append(self.create_node(origin, move))
        else:
            for origin, catches in childs.items():
                for catch in catches:
                    self.children.append(self.create_node(origin, catch[0], catch[1]))

g_tree: Node

def ai():
    global g_tree
    g_tree = Node(g_board, None, None, 0, G_PLAYERS["player"].pieces, G_PLAYERS["opponent"].pieces)
    return minimax()

def minimax():
    import random
    return g_tree.children[random.randint(0, len(g_tree.children) - 1)]

#evaluar el estado actual del tablero
def evaluate_score(node: Node):
    player_score = 0  #puntos totales del jugador
    opponent_score = 0  #puntos totales de oponente

    piece_value = 1  #valor de pieza normal  
    queen_value = 5  #valor de reina

    # Evaluar las piezas del jugador
    for piece in node.pieces_player:
        if piece.queen:  
            player_score += queen_value
        else: 
            player_score += piece_value


        #sumamos las puntos de la posicion
        player_score += evaluate_position(piece, player=True)
    
    for piece in node.pieces_opponent:
        if piece.queen:
            opponent_score += queen_value
        else: 
            opponent_score += piece_value

        
        opponent_score += evaluate_position(piece, player=False)

    #aqui sumamos puntos si el jugador  captura pieza
    for piece in node.pieces_player:

        catches = piece.get_catches(node.board)  #ver cuantas capturas puede hacer

        player_score += len(catches) * 2  #sumamos la cantidad de capturas por  2 puntos

    for piece in node.pieces_opponent:
        catches = piece.get_catches(node.board)  

        opponent_score += len(catches) * 2  

    #aqui devolvemos la deferencia entre el jugador y el oponente
    return player_score - opponent_score

def evaluate_position(piece, player=True):

    x, y = piece.x, piece.y  #cogemos la posicion de la pieza

    cell_value = 0 

    #aqui evaluamos la fila donde una pieza se convierte en riena
    if player:
        cell_value += ((10 - y) / 10) * 10 
          #cuanto mas adelante (fila 0), gana mas puntos
    else:
        cell_value -= (y / 10) * 10
         #cuanto mas atras (fila 7), pierde mas puntos

    # Evaluar cercanía a los bordes laterales
    side_edge_value = (1 - (0.5 / abs(x - 5.5))) * 20 if abs(x - 5.5) != 0 else 0
    if player:
        cell_value += side_edge_value  #sumamos si es el jugador 
    else:
        cell_value -= side_edge_value #restamos si es el oponente

    return cell_value  #devolver el valor calculado

# GAME #

def game():
    turn = 0
    while True:
        printBoard(g_board)
        if turn % 2 == 0:
            if not player_turn():
                continue
        else:
            if not ai_turn():
                continue
        turn += 1

def parse_coordinates(coord: str) -> tuple[int, int]:
    return (to_logic(coord[0], True), to_logic(coord[1], False)) if coord[0].isalpha() else (to_logic(coord[1], True), to_logic(coord[0], False))

def player_turn():
    originY, originX = parse_coordinates(input("Origin: ").upper())
    for piece in G_PLAYERS["player"].pieces:
        if (piece.x, piece.y) == (originX, originY):
            """ options = piece.get_catches(g_board)
            if options:
                print("Catches:")
                for option in options:
                    print(f"{option[0]}{option[1]}")
            else:
                moves = piece.get_moves(g_board)
                if moves:
                    for move in moves:
                        print(f"{move[0]}{move[1]}")
                else:
                    print("No moves available")
                    exit(0) """
            destinyY, destinyX = parse_coordinates(input("Destiny: ").upper())
            piece.move((destinyX, destinyY))
            return True
    
    print("No piece found")
    return False

def ai_turn():
    move = ai()
    origin, destiny = move.last_move
    for piece in G_PLAYERS["opponent"].pieces:
        if (piece.x, piece.y) == (origin[0], origin[1]):
            piece.move((destiny[0], destiny[1]), move.last_catch)
            return True
    
    print("No piece found")
    return False

game()