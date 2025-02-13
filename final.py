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

import pygame
import random
import time
from copy import deepcopy

from GUI.loading_screen import loading_screen_with_image
from GUI.menu import show_menu

game_over = False
winner = None

def check_bounds(x: int, y: int) -> bool:
    return 0 <= x < 8 and 0 <= y < 8

def empty_cell(x: int, y: int, board: list = None) -> bool:
    if board is None:
        board = g_board
    return board[x][y] == 0

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
                Piece(self, 1, 6)
            ]
        else:
            self.pieces = [
                Piece(self, 7, 0),
                Piece(self, 7, 2),
                Piece(self, 7, 4),
                Piece(self, 7, 6),
                Piece(self, 6, 1),
                Piece(self, 6, 3),
                Piece(self, 6, 5),
                Piece(self, 6, 7)
            ]

class Piece:
    move_length: tuple = (1, 1)
    catch_length: tuple = (2, 2)

    def __init__(self, player: Player, x: int, y: int):
        self.player = player
        self.x = x
        self.y = y
        self.queen = False
        self.symbol = 2 if player.opponent else 1
        self.direction_x = (1,) if self.player.opponent else (-1,)

    def set_queen(self, board=None):
        # Only promote if not already a queen.
        if self.queen:
            return
        self.queen = True
        self.symbol += 2  # 1 -> 3 for player, 2 -> 4 for opponent.
        self.direction_x = (1, -1)
        self.move_length = (1, 7)
        self.catch_length = (2, 7)
        # Update the given board (simulation) or the global board (actual game).
        if board is not None:
            board[self.x][self.y] = self.symbol
        else:
            global g_board
            g_board[self.x][self.y] = self.symbol

    def get_catches(self, board: list, alt_piece=None, caught_cells=tuple()) -> list:
        piece = alt_piece if alt_piece != None else self
        length = piece.catch_length
        catches = []
        for dx in piece.direction_x:
            for dy in (-1, 1):
                current_length = length[0]
                current_caught_cells = caught_cells
                while current_length in range(length[0], length[1] + 1):
                    destiny = (piece.x + dx * current_length, piece.y + dy * current_length)
                    if not check_bounds(*destiny):
                        break
                    board_destiny = int(board[destiny[0]][destiny[1]])
                    if board_destiny != 0 and board_destiny % 2 == (1 if not self.player.opponent else 0):
                        break
                    if board_destiny != 0 and board_destiny % 2 == (0 if not self.player.opponent else 1) and \
                        check_bounds(destiny[0] + dx, destiny[1] + dy) and int(board[destiny[0] + dx][destiny[1] + dy]) != 0:
                        break
                    if empty_cell(*destiny, board):
                        # The piece to capture is the cell immediately before the destination.
                        catch_cell = (destiny[0] - dx, destiny[1] - dy)
                        catch_cell_piece = int(board[catch_cell[0]][catch_cell[1]])
                        # Check that the piece in catch_cell belongs to the opponent.
                        if catch_cell_piece != 0 and (catch_cell_piece % 2 == (0 if not self.player.opponent else 1)):
                            # Before actually adding the capture to the list, recursive call to check for further captures.
                            copy_board = deepcopy(board)
                            copy_board[catch_cell[0]][catch_cell[1]] = 0
                            copy_board[destiny[0]][destiny[1]] = piece.symbol
                            copy_piece = Piece(self.player, destiny[0], destiny[1])
                            # Check if the destiny turns the piece into a queen.
                            if destiny[1] == 0 or destiny[1] == 7:
                                copy_piece.set_queen(copy_board)
                            current_caught_cells += catch_cell
                            result = self.get_catches(copy_board, copy_piece, current_caught_cells)
                            if result == None: # If no further captures are possible
                                catches.append((destiny, current_caught_cells))
                                break
                            else:
                                for catch in result:
                                    catches.append(catch)
                                break
                    current_length += 1
        return catches if catches else None

    def get_moves(self, board: list) -> list | None:
        length = self.move_length
        moves = []
        for dx in self.direction_x:
            for dy in (-1, 1):
                current_length = length[0]
                while current_length in range(length[0], length[1] + 1):
                    destiny = (self.x + dx * current_length, self.y + dy * current_length)
                    if not check_bounds(*destiny):
                        break
                    if not empty_cell(*destiny, board):
                        break
                    moves.append(destiny)
                    current_length += 1
        return moves if moves else None

    def move(self, destiny: tuple[int, int], catch: tuple[int] = None):
        global g_board
        # Update board: set destination to the piece's symbol and clear the origin.
        g_board[destiny[0]][destiny[1]] = self.symbol
        g_board[self.x][self.y] = 0
        if catch:
            for num in range(0, len(catch) - 1, 2):
                g_board[catch[num]][catch[num + 1]] = 0
                # Remove the captured piece from the opponent’s list.
                opponent = G_PLAYERS["opponent"] if not self.player.opponent else G_PLAYERS["player"]
                opponent.pieces = [p for p in opponent.pieces if (p.x, p.y) != (catch[num], catch[num + 1])]
        self.x, self.y = destiny
        # Correct promotion check: player pieces promote when reaching row 0; opponent pieces when reaching row 7.
        if (self.x == 0 and not self.player.opponent) or (self.x == 7 and self.player.opponent):
            self.set_queen()

DEPTH_LIMIT = 3

class Node:
    def __init__(self, board, last_move, last_catch, depth, pieces_player: list, pieces_opponent: list):
        self.board = board
        self.last_move = last_move
        self.last_catch = last_catch
        self.depth = depth
        self.pieces_player = deepcopy(pieces_player)
        self.pieces_opponent = deepcopy(pieces_opponent)
        self.children = []
        if depth < DEPTH_LIMIT:
            self.get_children()

    def get_catches(self) -> dict | None:
        captures = {}
        # In the simulation tree, at depth 0 the opponent (AI) is moving.
        pieces = self.pieces_player if (self.depth % 2 == 1) else self.pieces_opponent
        for piece in pieces:
            moves = piece.get_catches(self.board)
            if moves:
                captures[(piece.x, piece.y)] = moves
        return captures if captures else None

    def get_moves(self) -> dict | None:
        moves = {}
        pieces = self.pieces_player if (self.depth % 2 == 1) else self.pieces_opponent
        for piece in pieces:
            if check_bounds(piece.x, piece.y):
                possible_moves = piece.get_moves(self.board)
                if possible_moves:
                    moves[(piece.x, piece.y)] = possible_moves
        return moves if moves else None

    def create_node(self, origin: tuple[int, int], destiny: tuple[int, int], capture: tuple[int, int] = None):
        # Create a new board that reflects the move.
        new_board = deepcopy(self.board)
        new_board[destiny[0]][destiny[1]] = new_board[origin[0]][origin[1]]
        new_board[origin[0]][origin[1]] = 0
        if capture:
            new_board[capture[0]][capture[1]] = 0

        # Instead of modifying the original pieces lists, make deep copies and update those.
        new_pieces_player = deepcopy(self.pieces_player)
        new_pieces_opponent = deepcopy(self.pieces_opponent)
        # Determine which side is moving and which is the opponent.
        if self.depth % 2 == 1:
            moving = new_pieces_player
            opponent_list = new_pieces_opponent
        else:
            moving = new_pieces_opponent
            opponent_list = new_pieces_player

        # Update the moving piece’s position.
        for piece in moving:
            if (piece.x, piece.y) == origin:
                piece.x, piece.y = destiny
                # Use the correct promotion condition (and update the simulated board)
                if (destiny[0] == 0 and not piece.player.opponent) or (destiny[0] == 7 and piece.player.opponent):
                    piece.set_queen(new_board)
                break

        # Remove the captured piece from the opponent’s list.
        if capture:
            for piece in opponent_list:
                if (piece.x, piece.y) == capture:
                    opponent_list.remove(piece)
                    break

        return Node(new_board, (origin, destiny), capture, self.depth + 1, new_pieces_player, new_pieces_opponent)

    def get_children(self):
        childs = self.get_catches()
        if childs is None:
            childs = self.get_moves()
            if childs is None:
                global game_over, winner
                game_over = True
                if self.depth % 2 == 0:
                    winner = "player"
                    print("Player won!")
                else:
                    winner = "ai"
                    print("AI won!")
                return
            for origin, moves in childs.items():
                for move in moves:
                    self.children.append(self.create_node(origin, move))
        else:
            max_consecutive_captures = 1
            for origin, catches in childs.items():
                for catch in catches:
                    if len(catch[1]) > max_consecutive_captures:
                        max_consecutive_captures = len(catch[1])
            for origin, catches in childs.items():
                for catch in catches:
                    self.children.append(self.create_node(origin, catch[0], catch[1]))

g_tree: Node

def ai():
    global g_tree
    # For the AI tree, depth 0 corresponds to the opponent’s (AI’s) move.
    g_tree = Node(g_board, None, None, 0, G_PLAYERS["player"].pieces, G_PLAYERS["opponent"].pieces)
    return minimax()

def minimax() -> Node: # Returns a node
    return random.choice(g_tree.children) if g_tree.children else None

def ai_turn():
    if game_over:
        return False
    move = ai()
    if move is None:
        check_win_condition()
        return False
    origin, destiny = move.last_move
    for piece in G_PLAYERS["opponent"].pieces:
        if (piece.x, piece.y) == (origin[0], origin[1]):
            piece.move((destiny[0], destiny[1]), move.last_catch)
            check_win_condition()
            return True
    return False

def check_win_condition():
    global game_over, winner
    if game_over:
        return
    player_moves = any(piece.get_moves(g_board) or piece.get_catches(g_board)
                       for piece in G_PLAYERS["player"].pieces)
    ai_moves = any(piece.get_moves(g_board) or piece.get_catches(g_board)
                   for piece in G_PLAYERS["opponent"].pieces)
    if not player_moves:
        game_over = True
        winner = "ai"
        print("AI won!")
    elif not ai_moves:
        game_over = True
        winner = "player"
        print("Player won!")

g_board = [
    [0, 2, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

G_PLAYERS = {"player": Player(False)}
G_PLAYERS["opponent"] = Player(True, True)

def initialize_board():
    global g_board
    # Clear the board first.
    g_board = [[0 for _ in range(8)] for _ in range(8)]
    # Set player and opponent pieces onto the board.
    for player in G_PLAYERS.values():
        for piece in player.pieces:
            g_board[piece.x][piece.y] = piece.symbol

initialize_board()

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
MARGIN = 40

WHITE = (255, 255, 255)
LIGHT_BROWN = (222, 184, 135)
DARK_BROWN = (101, 67, 33)
YELLOW = (255, 200, 0)
PLAYER_COLOR = (0, 0, 0)
OPPONENT_COLOR = (220, 20, 60)
CROWN_COLOR = (255, 215, 0)

pygame.init()

screen = pygame.display.set_mode((WIDTH + MARGIN, HEIGHT + MARGIN))
pygame.display.set_caption("Checkers")
font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

def draw_board():
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            rect = pygame.Rect(col * SQUARE_SIZE + MARGIN, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)
    letters = "ABCDEFGH"
    for i in range(COLS):
        text = font.render(letters[i], True, DARK_BROWN)
        screen.blit(text, (i * SQUARE_SIZE + MARGIN + SQUARE_SIZE // 2 - text.get_width() // 2, HEIGHT * 1.02))
    for i in range(ROWS):
        text = font.render(str(ROWS - i), True, DARK_BROWN)
        screen.blit(text, (12, i * SQUARE_SIZE + SQUARE_SIZE // 2 - text.get_height() // 2))

def draw_pieces():
    for row in range(ROWS):
        for col in range(COLS):
            cell = g_board[row][col]
            if cell != 0:
                center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2 + MARGIN
                center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                radius = SQUARE_SIZE // 3
                if cell in (1, 3):
                    pygame.draw.circle(screen, PLAYER_COLOR, (center_x, center_y), radius)
                elif cell in (2, 4):
                    pygame.draw.circle(screen, OPPONENT_COLOR, (center_x, center_y), radius)
                if cell in (3, 4):
                    pygame.draw.circle(screen, CROWN_COLOR, (center_x, center_y), radius // 2)

def get_board_position(mouse_pos):
    x, y = mouse_pos
    if x < MARGIN or x > WIDTH + MARGIN or y < 0 or y > HEIGHT:
        return None
    col = (x - MARGIN) // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return (row, col)

selected_piece_obj = None
turn = 0

loading_screen_with_image()
mode = show_menu()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over:
            continue
        if event.type == pygame.MOUSEBUTTONDOWN and (turn == 0 or mode == "PVP"):
            pos = pygame.mouse.get_pos()
            board_pos = get_board_position(pos)
            if board_pos:
                player = "player" if turn == 0 or mode == "PVC" else "opponent"
                row, col = board_pos
                if selected_piece_obj is None:
                    for piece in G_PLAYERS[player].pieces:
                        if (piece.x, piece.y) == (row, col):
                            selected_piece_obj = piece
                            break
                else:
                    normal_moves = selected_piece_obj.get_moves(g_board) or []
                    capture_moves = selected_piece_obj.get_catches(g_board) or []
                    valid_moves = {move: None for move in normal_moves}
                    for cap in capture_moves:
                        valid_moves[cap[0]] = cap[1]
                    if (row, col) in valid_moves:
                        selected_piece_obj.move((row, col), valid_moves[(row, col)])
                        check_win_condition()
                        selected_piece_obj = None
                        turn = abs(turn - 1)
                    else:
                        found = False
                        for piece in G_PLAYERS[player].pieces:
                            if (piece.x, piece.y) == (row, col):
                                selected_piece_obj = piece
                                found = True
                                break
                        if not found:
                            selected_piece_obj = None
        elif mode == "PVC" and turn == 1 and not game_over:
            time.sleep(0.5)
            ai_turn()
            turn = 0
    draw_board()
    draw_pieces()
    if selected_piece_obj:
        s_row, s_col = selected_piece_obj.x, selected_piece_obj.y
        rect = pygame.Rect(s_col * SQUARE_SIZE + MARGIN, s_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(screen, YELLOW, rect, 3)
    pygame.display.flip()

pygame.quit()
