import pygame
import sys
import time
import psutil
from ai import minimax_ai_move, alphabeta_ai_move, mcts_ai_move, BOARD_ROWS, BOARD_COLS
from utils import save_result, save_time_memory, check_winner

# ------------------------- Settings -------------------------
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
TOP_MARGIN = 50
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe AI")

# Board settings
BOARD_WIDTH = 300
BOARD_HEIGHT = 300
SQUARE_SIZE = BOARD_WIDTH // BOARD_COLS
OFFSET_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
OFFSET_Y = TOP_MARGIN

# Colors - pastel theme
WHITE = (245, 245, 245)
BG_COLOR = (200, 230, 255)
LINE_COLOR = (100, 100, 100)
X_COLOR = (255, 100, 100)
O_COLOR = (100, 255, 100)
HIGHLIGHT_COLOR = (255, 255, 255, 50)

# Font
font = pygame.font.Font(None, 48)

# ------------------------- Board State -------------------------
board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
turn = 'X'
player_move_time = 0

# ------------------------- Drawing Functions -------------------------
def draw_grid():
    screen.fill(BG_COLOR)
    line_width = 5
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR,
                         (OFFSET_X, OFFSET_Y + i * SQUARE_SIZE),
                         (OFFSET_X + BOARD_WIDTH, OFFSET_Y + i * SQUARE_SIZE),
                         line_width)
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR,
                         (OFFSET_X + i * SQUARE_SIZE, OFFSET_Y),
                         (OFFSET_X + i * SQUARE_SIZE, OFFSET_Y + BOARD_HEIGHT),
                         line_width)

def draw_markers():
    line_width = 10
    padding = 20
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            x_center = OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
            y_center = OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
            if board[row][col] == 'X':
                pygame.draw.line(screen, X_COLOR,
                                 (OFFSET_X + col * SQUARE_SIZE + padding, OFFSET_Y + row * SQUARE_SIZE + padding),
                                 (OFFSET_X + (col + 1) * SQUARE_SIZE - padding, OFFSET_Y + (row + 1) * SQUARE_SIZE - padding),
                                 line_width)
                pygame.draw.line(screen, X_COLOR,
                                 (OFFSET_X + (col + 1) * SQUARE_SIZE - padding, OFFSET_Y + row * SQUARE_SIZE + padding),
                                 (OFFSET_X + col * SQUARE_SIZE + padding, OFFSET_Y + (row + 1) * SQUARE_SIZE - padding),
                                 line_width)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, O_COLOR, (x_center, y_center), SQUARE_SIZE // 2 - padding, line_width)

def highlight_square(mouse_pos):
    col = (mouse_pos[0] - OFFSET_X) // SQUARE_SIZE
    row = (mouse_pos[1] - OFFSET_Y) // SQUARE_SIZE
    if 0 <= col < BOARD_COLS and 0 <= row < BOARD_ROWS:
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill(HIGHLIGHT_COLOR)
        screen.blit(s, (OFFSET_X + col * SQUARE_SIZE, OFFSET_Y + row * SQUARE_SIZE))

# ------------------------- Menu -------------------------
def main_menu():
    WIDTH_MENU, HEIGHT_MENU = 600, 400
    menu_screen = pygame.display.set_mode((WIDTH_MENU, HEIGHT_MENU))
    pygame.display.set_caption("Select AI")
    WHITE, BLACK = (255, 255, 255), (0, 0, 0)
    font_menu = pygame.font.SysFont(None, 36)

    def draw_text(text, x, y):
        surf = font_menu.render(text, True, BLACK)
        rect = surf.get_rect(center=(x, y))
        menu_screen.blit(surf, rect)

    button_width, button_height = 200, 50
    start_y = HEIGHT_MENU // 2 - button_height
    buttons = [
        (pygame.Rect(WIDTH_MENU//2 - button_width//2, start_y, button_width, button_height), "Minimax AI", 'minimax'),
        (pygame.Rect(WIDTH_MENU//2 - button_width//2, start_y + 75, button_width, button_height), "Alpha-Beta AI", 'alphabeta'),
        (pygame.Rect(WIDTH_MENU//2 - button_width//2, start_y + 150, button_width, button_height), "MCTS AI", 'mcts')
    ]

    while True:
        menu_screen.fill(WHITE)
        draw_text("Select AI to Play Against", WIDTH_MENU//2, HEIGHT_MENU//4)

        for rect, text, _ in buttons:
            pygame.draw.rect(menu_screen, BLACK, rect, 2)
            draw_text(text, rect.centerx, rect.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for rect, _, choice in buttons:
                    if rect.collidepoint(pos):
                        return choice

        pygame.display.update()

# ------------------------- Main Game -------------------------
def reset_board():
    global board, turn, player_move_time
    board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    turn = 'X'
    player_move_time = 0

def main():
    global turn, player_move_time, board
    ai_choice = main_menu()
    running = True

    while running:
        current_time = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and turn == 'X':
                col = (mouse_pos[0] - OFFSET_X) // SQUARE_SIZE
                row = (mouse_pos[1] - OFFSET_Y) // SQUARE_SIZE
                if 0 <= col < BOARD_COLS and 0 <= row < BOARD_ROWS and board[row][col] == '':
                    board[row][col] = 'X'
                    turn = 'O'
                    player_move_time = current_time

        # AI move
        if turn == 'O' and current_time - player_move_time >= 500:
            start_time = time.time()
            before_memory = psutil.Process().memory_info().rss

            if ai_choice == 'minimax':
                row, col = minimax_ai_move(board)
            elif ai_choice == 'alphabeta':
                row, col = alphabeta_ai_move(board)
            else:
                row, col = mcts_ai_move(board)

            if row is not None and col is not None:
                board[row][col] = 'O'
                turn = 'X'

            end_time = time.time()
            after_memory = psutil.Process().memory_info().rss
            save_time_memory(end_time - start_time, (after_memory - before_memory)/1024)

        # Draw board
        draw_grid()
        draw_markers()
        highlight_square(mouse_pos)
        pygame.display.update()

        # Check winner
        winner = check_winner(board)
        if winner:
            message = "Tie!" if winner == 'Tie' else f"{winner} wins!"
            save_result(board, message, ai_choice)

            # Display overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0,0,0))
            screen.blit(overlay, (0,0))
            text_surf = font.render(message, True, WHITE)
            screen.blit(text_surf, text_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
            pygame.display.update()
            pygame.time.delay(2000)
            reset_board()

if __name__ == "__main__":
    main()