# --------------------------------------------------------------------------- #
#                                                                             #
#     checkers.py                                         +#######+           #
#                                                       +###########+         #
#     PROJECT: Checkers                       ·''''''''·#############         #
#                                            '''''''''''+###########+         #
#                                            '''''''''''' +#######+           #
#     CREATED DATE: 30/01/2025               ''''''''''''                     #
#     LAST UPDATE: 14/02/2025                 `''''''''´                      #
#                                                                             #
# --------------------------------------------------------------------------- #

import os
import time
import pygame
from copy import deepcopy

from GUI.menu import show_menu
from GUI.loading_screen import loading_screen_with_image

from DB.openings import getNextMove

# TODO - Timer

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
                # Handle game over
                return
            for origin, moves in childs.items():
                for move in moves:
                    self.children.append(self.create_node(origin, move))
        else:
            # Find maximum captures in any move
            all_captures = [catch for _, catches in childs.items() for catch in catches]
            if not all_captures:
                return
            max_captures = max(len(catch[1]) for catch in all_captures)
            
            # Only keep moves with max captures
            for origin, catches in childs.items():
                for catch in catches:
                    if len(catch[1]) == max_captures:
                        self.children.append(self.create_node(origin, catch[0], catch[1]))

game_over = False
winner = None

g_trace = ""

g_tree: Node
DEPTH_LIMIT = 4

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

def check_bounds(x: int, y: int) -> bool:
    return 0 <= x < 8 and 0 <= y < 8

def empty_cell(x: int, y: int, board: list = None) -> bool:
    if board is None:
        board = g_board
    return board[x][y] == 0

def generate_mermaid_tree(node: Node) -> str:
    lines = ["graph TD"]
    node_ids = {}  # maps id(node) to a unique mermaid node id
    next_id = 0

    def traverse(current: Node):
        nonlocal next_id
        # Assign an id to the current node if not already assigned.
        current_id = node_ids.get(id(current))
        if current_id is None:
            current_id = f"node{next_id}"
            node_ids[id(current)] = current_id
            next_id += 1
        # Label for current node: include depth and score.
        label = f"Depth: {current.depth}\\nScore: {evaluate_score(current):.2f}"
        lines.append(f'{current_id}["{label}"]')
        # Process children.
        for child in current.children:
            # Assign id for the child.
            child_id = f"node{next_id}"
            node_ids[id(child)] = child_id
            next_id += 1
            # Label for child.
            child_label = f"Depth: {child.depth}\\nScore: {evaluate_score(child):.2f}"
            lines.append(f'{child_id}["{child_label}"]')
            # Optionally, show the move that led to this child.
            move_label = ""
            if child.last_move:
                move_label = f"{child.last_move[0]} -> {child.last_move[1]}".replace("(", "").replace(")", "").replace(",", "").replace("->", " to ")
            lines.append(f"{current_id} -->|{move_label}| {child_id}")
            # Recursively traverse the subtree.
            traverse(child)
    
    traverse(node)
    return "\n".join(lines)

def ai():
    global g_tree
    # For the AI tree, depth 0 corresponds to the opponent’s (AI’s) move.
    g_tree = Node(g_board, None, None, 0, G_PLAYERS["player"].pieces, G_PLAYERS["opponent"].pieces)
    mermaid_diagram = generate_mermaid_tree(g_tree)
    with open("mermaid_diagram.txt", "w") as f:
        f.write(mermaid_diagram)
    #os.startfile("mermaid_diagram.txt")
    return minimax()

def minimax() -> Node:
    if not g_tree.children:
        return None

    best_move = None
    # At the root (depth 0), it's the AI's move, so it is the minimizing player.
    best_value = float('inf')
    
    for child in g_tree.children:
        # Next level (depth 1) will be the maximizing player's turn.
        value = minimax_value(child, True)
        if value < best_value:
            best_value = value
            best_move = child

    return best_move

def evaluate_position(piece, player=True) -> float:
    if piece.queen:
        return 0.0
    
    row = piece.x  # Corrected to use row (x-coordinate)
    if player:
        return (7 - row) * 0.4  # Player advances toward row 0
    else:
        return row * 0.4  # AI advances toward row 7

def evaluate_score(node: Node) -> float:

    piece_value = 1.0
    queen_value = 3.5

    player_score = 0.0
    opponent_score = 0.0

    # Player pieces
    for piece in node.pieces_player:
        player_score += queen_value if piece.queen else piece_value
        player_score += evaluate_position(piece, player=True)
        try:
            moves = piece.get_moves(node.board)
            player_score += 0.3 * len(moves)
        except Exception:
            pass

    # AI pieces
    for piece in node.pieces_opponent:
        opponent_score += queen_value if piece.queen else piece_value
        opponent_score += evaluate_position(piece, player=False)
        try:
            moves = piece.get_moves(node.board)
            opponent_score += 0.3 * len(moves)
        except Exception:
            pass

    return player_score - opponent_score

def minimax_value(node: Node, maximizing: bool) -> float:
    if not node.children:
        return evaluate_score(node)
    
    if maximizing:
        best_value = float('-inf')
        for child in node.children:
            best_value = max(best_value, minimax_value(child, False))
        return best_value
    else: # Minimizing
        best_value = float('inf')
        for child in node.children:
            best_value = min(best_value, minimax_value(child, True))
        return best_value

def ai_turn():
    global g_trace
    # Check DB first
    db_move = getNextMove(g_trace)
    if db_move is not None:
        print("DB")
        origin, destiny = db_move
        for piece in G_PLAYERS["opponent"].pieces:
            if (piece.x, piece.y) == (8 - origin[1], "abcdefgh".index(origin[0])):
                g_trace += "abcdefgh"[piece.y] + str(8 - piece.x) + destiny[0] + str(destiny[1]) + ";"
                piece.move((8 - destiny[1], "abcdefgh".index(destiny[0])), None)
                check_win_condition()
                return True
    else:
        if game_over:
            return False
        move = ai()
        if move is None:
            check_win_condition()
            return False
        origin, destiny = move.last_move
        for piece in G_PLAYERS["opponent"].pieces:
            if (piece.x, piece.y) == (origin[0], origin[1]):
                g_trace += "abcdefgh"[piece.y] + str(8 - piece.x) + "abcdefgh"[destiny[1]] + str(8 - destiny[0]) + ";"
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

def initialize_board():
    global g_board
    # Clear the board first.
    g_board = [[0 for _ in range(8)] for _ in range(8)]
    # Set player and opponent pieces onto the board.
    for player in G_PLAYERS.values():
        for piece in player.pieces:
            g_board[piece.x][piece.y] = piece.symbol

initialize_board()
 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (222, 184, 135)
DARK_BROWN = (101, 67, 33)
YELLOW = (255, 200, 0)
PLAYER_COLOR = (0, 0, 0)
OPPONENT_COLOR = (220, 20, 60)
CROWN_COLOR = (255, 215, 0)
WOOD_COLOR = (139, 69, 19)

pygame.init()

pygame.display.set_caption("Checkers")
font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

WIDTH, HEIGHT = 620, 620
MARGIN = 80
TOP_MARGIN = 100
ROWS, COLS = 8, 8
SQUARE_SIZE = (WIDTH - MARGIN // 2) // COLS
BORDER_THICKNESS = 6

# Set screen size to include margins and border
screen = pygame.display.set_mode((WIDTH + 2 * MARGIN, HEIGHT + 2 * MARGIN))

def draw_board():
    screen.fill(WOOD_COLOR)
    
    # Draw border around the board (within expanded screen)
    border_rect = pygame.Rect(MARGIN + 2.5 * BORDER_THICKNESS, TOP_MARGIN, 
                              (WIDTH - MARGIN // 2) + 2.5 * BORDER_THICKNESS, (WIDTH - MARGIN // 2) + 2.5 * BORDER_THICKNESS)
    pygame.draw.rect(screen, BLACK, border_rect)
    
    # Draw checkered squares
    for row in range(ROWS):
        for col in range(COLS):
            x = col * SQUARE_SIZE + MARGIN + 4 * BORDER_THICKNESS
            y = row * SQUARE_SIZE + TOP_MARGIN + 1.5 * BORDER_THICKNESS
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
    
    # Draw coordinate labels (now within expanded margins)
    letters = "ABCDEFGH"
    # Column labels (A-H at the bottom)
    for i in range(COLS):
        text = font.render(letters[i], True, BLACK)
        screen.blit(text, (
            i * SQUARE_SIZE + MARGIN + SQUARE_SIZE - text.get_width() * 1.5,
            MARGIN + HEIGHT + 10
        ))
    
    # Row labels (8-1 on the left)
    for i in range(ROWS):
        text = font.render(str(ROWS - i), True, BLACK)
        screen.blit(text, (
            MARGIN - 12,
            i * SQUARE_SIZE + MARGIN + SQUARE_SIZE // 2 + text.get_height()
        ))

def draw_pieces():
    for row in range(ROWS):
        for col in range(COLS):
            cell = g_board[row][col]
            if cell == 0:
                continue
            
            # Calculate center position of the piece
            radius = SQUARE_SIZE // 3
            center_x = col * SQUARE_SIZE + MARGIN + SQUARE_SIZE // 2 + radius
            center_y = row * SQUARE_SIZE + TOP_MARGIN + SQUARE_SIZE // 2 + radius // 2.5
            
            # Determine piece color
            if cell in (1, 3):
                color = PLAYER_COLOR  # Black pieces
            else:
                color = OPPONENT_COLOR  # Red pieces
            
            # Draw the base piece
            pygame.draw.circle(screen, color, (center_x, center_y), radius)
            
            # Draw crown for kings (cells 3 or 4)
            if cell in (3, 4):
                crown_radius = radius // 2
                pygame.draw.circle(screen, CROWN_COLOR, (center_x, center_y), crown_radius)

def get_board_position(mouse_pos):
    x, y = mouse_pos
    if x < MARGIN or x > WIDTH + MARGIN or y < 0 or y > HEIGHT:
        return None
    col = (x - MARGIN) // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return (row, col)

selected_piece_obj = None
turn = 0

loading_screen_with_image(WIDTH, HEIGHT, MARGIN)
mode = show_menu(WIDTH, HEIGHT, MARGIN)

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
                        if (turn == 0 and mode == "PVC"):
                            g_trace += "abcdefgh"[selected_piece_obj.y] + str(8 - selected_piece_obj.x) + "abcdefgh"[col] + str(8 - row) + "-"
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
            draw_board()
            draw_pieces()
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
