# ai.py
from utils import check_winner, evaluate
import copy
import random
import math

BOARD_ROWS, BOARD_COLS = 3, 3

# Minimax AI
def minimax_ai_move(board):
    best_score = float('-inf')
    best_move = (None, None)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == '':
                board[row][col] = 'O'
                score = minimax(board, False)
                board[row][col] = ''
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    return best_move

def minimax(board, is_maximizing):
    result = evaluate(board)
    if result is not None:
        return result
    if is_maximizing:
        best_score = float('-inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == '':
                    board[row][col] = 'O'
                    score = minimax(board, False)
                    board[row][col] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == '':
                    board[row][col] = 'X'
                    score = minimax(board, True)
                    board[row][col] = ''
                    best_score = min(score, best_score)
        return best_score

# Alphabeta AI
def alphabeta_ai_move(board):
    best_score = float('-inf')
    best_move = None
    alpha, beta = float('-inf'), float('inf')
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if board[r][c] == '':
                board[r][c] = 'O'
                score = alphabeta(board, False, alpha, beta)
                board[r][c] = ''
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
                alpha = max(alpha, best_score)
    return best_move

def alphabeta(board, is_maximizing, alpha, beta):
    score = evaluate(board)
    if score is not None:
        return score
    if is_maximizing:
        best_score = float('-inf')
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if board[r][c] == '':
                    board[r][c] = 'O'
                    best_score = max(best_score, alphabeta(board, False, alpha, beta))
                    board[r][c] = ''
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float('inf')
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if board[r][c] == '':
                    board[r][c] = 'X'
                    best_score = min(best_score, alphabeta(board, True, alpha, beta))
                    board[r][c] = ''
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score

# MCTS AI
class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

def get_legal_actions(board):
    return [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] == '']

def apply_action(board, action, turn):
    r, c = action
    new_board = copy.deepcopy(board)
    new_board[r][c] = turn
    return new_board

def is_terminal(board):
    return check_winner(board) is not None

def simulate(board, turn):
    b = copy.deepcopy(board)
    current_turn = turn
    while not is_terminal(b):
        moves = get_legal_actions(b)
        move = random.choice(moves)
        b[move[0]][move[1]] = current_turn
        current_turn = 'O' if current_turn == 'X' else 'X'
    result = evaluate(b)
    return result

def backpropagate(node, result):
    while node:
        node.visits += 1
        node.wins += result
        node = node.parent

def uct(node):
    if node.visits == 0:
        return float('inf')
    return (node.wins / node.visits) + math.sqrt(2 * math.log(node.parent.visits) / node.visits)

def select(node):
    while node.children:
        node = max(node.children, key=uct)
    return node

def expand(node, turn):
    actions = get_legal_actions(node.state)
    for action in actions:
        new_state = apply_action(node.state, action, turn)
        child = Node(new_state, parent=node)
        node.children.append(child)
    return random.choice(node.children) if node.children else node

def mcts_ai_move(board, iterations=500):
    root = Node(board)
    turn = 'O'
    for _ in range(iterations):
        node = select(root)
        result = simulate(node.state, turn)
        backpropagate(node, result)
    best_child = max(root.children, key=lambda n: n.visits, default=None)
    if best_child:
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if board[r][c] == '' and best_child.state[r][c] == 'O':
                    return (r, c)
    return None