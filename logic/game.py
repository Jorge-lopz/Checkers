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
            for dy in  (-1, 1):
                current_length = length[0] # Starts at min (2)
                while current_length in range(length[0], length[1] + 1):  # Between min and max length
                    destiny = (self.x + dx * current_length, self.y + dy * current_length)
                    # CHECK BOUNDS, VALID, AND CATCH
                    if not check_bounds(*destiny): break
                    elif not empty_cell(*destiny): continue
                    # Check if it is an actual catch
                    catch_cell = board[destiny[0] - 1][destiny[1] - 1]
                    if catch_cell != 0 and catch_cell % 2 == (0 if not self.player.opponent else 1): # Uses odd or even operations to check piece owner (1-3 / 2-4)
                        catches.append((destiny, catch_cell)) # Appends both the destiny position and the caught piece position
                    current_length += 1
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
                    elif not empty_cell(*destiny): continue  
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

G_PLAYERS = []


