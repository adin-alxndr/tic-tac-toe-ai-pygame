import pygame
import os
import datetime

# ------------------------- Game Evaluation -------------------------
def check_winner(board):
    for r in range(3):
        if board[r][0] == board[r][1] == board[r][2] != '':
            return board[r][0]
    for c in range(3):
        if board[0][c] == board[1][c] == board[2][c] != '':
            return board[0][c]
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    if all(cell != '' for row in board for cell in row):
        return 'Tie'
    return None

def evaluate(board):
    winner = check_winner(board)
    if winner == 'X': return -1
    elif winner == 'O': return 1
    elif winner == 'Tie': return 0
    return None

# ------------------------- Save Functions -------------------------
def save_result(board, message, ai_name):
    folder = os.path.join("images", f"{ai_name}_results")
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder, f"{timestamp}.png")
    pygame.image.save(pygame.display.get_surface(), filename)
    with open(f"{ai_name}_results.txt", "a") as f:
        f.write(f"{timestamp}: {message} (Image: {filename})\n")

def save_time_memory(time_taken, memory_kb):
    with open("time_memory.txt", "a") as f:
        f.write(f"Time: {time_taken:.3f}s, Memory: {memory_kb:.3f}kb\n")