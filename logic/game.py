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

import ai
from copy import deepcopy
from colorama import init, Fore

init(autoreset=True)

# X (Fila - números), Y (Columnas - letras)

class Player:

    pieces = []

    def __init__(self, opponent: bool, ia: bool = False):
        if ia and not opponent:
            raise Exception("IA has to be opponent")
        self.opponent: bool = opponent
        self.ia: bool = ia

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
    direction_x: tuple | int
    move_length: tuple = (1, 1)
    catch_length: tuple = (2, 2)
    symbol: str

    def __init__(self, player: Player, x: int, y: int):
        self.player = player
        self.x = x
        self.y = y
        # Other variables
        
        self.symbol = "2" if player.opponent else "1"
        self.direction_x = 1 if self.player.opponent else -1

    def set_queen(self):
        self.queen = True
        self.symbol = str(int(self.symbol) + 2)
        self.direction_x = (1, -1)
        self.move_length = (1, 7)
        self.catch_length = (2, 7)
        
    def get_catches(self, board: list, alt_origin = ()) -> list:
        """
        Returns a list of valid catches (x [destiny], y [destiny]) -> [(),(),(),()]
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
                    elif not empty_cell(*destiny, board): continue
                    # Check if it is an actual catch
                    catch_cell = board[destiny[0] - 1][destiny[1] - 1]
                    if catch_cell != 0 and catch_cell % 2 == (0 if not self.player.opponent else 1): # Uses odd or even operations to check piece owner (1-3 / 2-4)
                        catches.append((destiny, catch_cell)) # Appends both the destiny position and the caught piece position
                    current_length += 1

                    # TODO - Jorge - If a catch is found with a vector, skip to the next vector
                    # Recursive call

        return catches
                        
    def get_ai_moves(self, board: list) -> list | None:
        """
        Returns a list of valid moves for the AI piece (x [destiny], y [destiny]) -> [(),(),(),()]
        """
        if not self.player.ia:
            raise Exception("Should only be used for AI")
        
        length = self.move_length
        
        moves = []
        for dx in self.direction_x:
            for dy in (-1, 1):
                current_length = length[0] # Starts at min (2)
                while current_length in range(length[0], length[1] + 1):  # Between min and max length
                    destiny = (self.x + dx * current_length, self.y + dy * current_length)
                    # CHECK BOUNDS AND EMPTY
                    if not check_bounds(*destiny): break 
                    elif not empty_cell(*destiny, board): continue  
                    moves.append(destiny)
                    current_length += 1

        return moves if len(moves) > 0 else None
                    
        # TODO - HUGO - Generate all possible moves and checks bounds and valid

    def move(self, destiny: (int)):
        """
        Just moves without any check
        """
        global g_board
        g_board[destiny[0]][destiny[1]] = self.symbol
        g_board[self.x][self.y] = 0
        self.x, self.y = destiny
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

def to_logic(visual_row: int) -> int:
    if not(1 <= visual_row <= 8):
        raise ValueError("")
    return 8- visual_row

def to_visual(logical_row: int) -> int:
      
    if not (0 <= logical_row < 7):
        raise ValueError("")
    return logical_row

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
    #A  B  C  D  E  F  G  H   # INDEX     VISUAL [abs(index - 7)]
    [0, 2, 0, 2, 0, 2, 0, 2], #   0    ->   7 
    [2, 0, 2, 0, 2, 0, 2, 0], #   1    ->   6
    [0, 0, 0, 0, 0, 0, 0, 0], #   2    ->   5
    [0, 0, 0, 0, 0, 0, 0, 0], #   3    ->   4
    [0, 0, 0, 0, 0, 0, 0, 0], #   4    ->   3
    [0, 0, 0, 0, 0, 0, 0, 0], #   5    ->   2
    [0, 1, 0, 1, 0, 1, 0, 1], #   6    ->   1
    [1, 0, 1, 0, 1, 0, 1, 0]  #   7    ->   0
]

printBoard(g_board)

G_PLAYERS = {"player": Player(False)}

G_PLAYERS["opponent"] = Player(True, True) # Opeonent and IA

# AI #

DEPTH_LIMIT = 3
# ROOT is 0, so odd depth nodes are generates by a IA move (and even by player move)

class Node:

    children = []

    def __init__(self, board, last_move, depth, pieces_player: list, pieces_opponent: list):
        # TODO - Also needs to receive an array of player and oponnents pieces, that will then be modified on every nodo (after every movement)
        self.board = board
        self.last_move = last_move
        self.depth = depth
        self.pieces_player = deepcopy(pieces_player)
        self.pieces_opponent = deepcopy(pieces_opponent)
        
        # If depth is DEPTH_LIMIT, it is a leaf node (and dooesn't call the get_children funtion)

    def get_catches(self) -> dict | None:
        # TODO - Jesus - Get all possible catches (already existing functions)
        """
        Obtiene los movimientos de captura disponibles en el nodo actual.
        Retorna un diccionario donde la clave es la posicion final de la pieza y
        el valor es la posicion de la pieza capturada.
        """
        captures = {}  
        # Seleccionamos las piezas del jugador según el nivel de profundidad
        pieces = self.pieces_player if (self.depth % 2 == 1) else self.pieces_opponent

    # Itera sobre las piezas 
        for piece in pieces:
            # Si hay capturas válidas, las añade al diccionario
            for catch in piece.get_catches(self.board):
                captures[(piece.x, piece.y)] = catch  
    
    # Si no hay capturas válidas, devuelve None
        return captures if captures else None
            
    def get_moves(self) -> dict:
        # TODO - Get all possible moves (already existing functions)
        pass

    def get_children(self):
    
        # TODO - Call catches, if none, call moves
        # NOTE - For every possible move or catch, a new child node is created
        if self.get_catches() == None:
           children = self.get_moves()
           for move in children:
                new_board = self.board.copy()
                new_board[move[1][0]][move[1][1]] = new_board[move[0][0]][move[0][1]]
                new_board[move[0][0]][move[0][1]] = 0
                new_node = Node(new_board, move, self.depth + 1, self.pieces_player, self.pieces_opponent)
                self.children.append(new_node)
        else:
           children=self.get_catches()
    pass
    
        
        
        
            
            
g_tree: Node

def ai():
    global g_tree
    g_tree = Node(g_board, None, 0, G_PLAYERS["player"].pieces, G_PLAYERS["opponent"].pieces)
    return minimax()

def minimax():
    pass

def evaluate():
    pass
    # TODO - Evaluate the state of the game based on the current board, the remaining pieces and their positions... (COPY FROM AN AI OR EXISTING ALGORITHM)
