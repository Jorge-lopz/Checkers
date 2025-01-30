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
    symbol: str

    def __init__(self, player: Player, x: int, y: int):
        self.player = player
        self.x = x
        self.y = y
        self.symbol = "2" if player.opponent else "1"

    def set_queen(self):
        self.queen = True
        self.symbol = str(int(self.symbol) + 2)

    def get_catches(self, board: list, alt_origin = ()) -> list:
        """
        Returns a list of valid catches (x [destiny], y [destiny]) -> [(),(),(),()]
        In case multiple pieces are caught consecutively, it will return a tuple with the concatenated catches
        [Recursive]
        """
        direction_x = (-1, 1) if self.queen else 1 if self.player.opponent else -1
        direction_y = (-1, 1)
        length = (2, 7) if self.queen else (2, 2)

        for dx in direction_x:
            for dy in direction_y:
                current_length = length[0] # Starts at min (2)
                while current_length in range(length[0], length[1] + 1):  # Between min and max length
                    destiny = (self.x + dx, self.y + dy)
                    # CHECK BOUNDS, VALID, AND CATCH

    def get_ai_moves(self, board: list) -> list:
        """
        Returns a list of valid moves for the AI piece (x [destiny], y [destiny]) -> [(),(),(),()]
        """
        if not self.player.ia:
            raise Exception("Should only be used for AI")
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
            
def check_bounds(x: int, y: int)-> bool:
    """
    Verificar que las coordenadas estan dentro del tablero. 
    Retorna True si esta dentro y False si esta fuera
    """
    return 0 <= x < 8 and 0 <= y < 8 
    
    
    
                 
# TODO - Jesús - FUNCTION TO CHECK OFF-BOUNDS -> check_bounds()       
# TODO - Isra - FUNCTION TO CHECK EMPTY CELL () -> empty_cell()
# TODO - Hanan - TURN VISUAL COORDS INTO LOGIC COORDS AND VICE VERSA -> to_logic(), to_visual()

g_board = [
    #A  B  C  D  E  F  G  H  (índice) (visual abs(índice - 7))
    [0, 2, 0, 2, 0, 2, 0, 2], # 0   ->   7 
    [2, 0, 2, 0, 2, 0, 2, 0], # 1   ->   6
    [0, 0, 0, 0, 0, 0, 0, 0], # 2   ->   5
    [0, 0, 0, 0, 0, 0, 0, 0], # 3   ->   4
    [0, 0, 0, 0, 0, 0, 0, 0], # 4   ->   3
    [0, 0, 0, 0, 0, 0, 0, 0], # 5   ->   2
    [0, 1, 0, 1, 0, 1, 0, 1], # 6   ->   1
    [1, 0, 1, 0, 1, 0, 1, 0]  # 7   ->   0
]

G_PLAYERS = []

