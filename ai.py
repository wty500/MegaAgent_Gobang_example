"""
ai.py - Gobang AI Module

Implements a strong AI opponent for Gobang (Five in a Row) with at least two difficulty levels.
Exposes the required interface for integration with the game engine.
"""

import time
import random
import copy

BOARD_SIZE = 15
EMPTY = 0
PLAYER = 1
AI = 2

class GobangAI:
    def __init__(self, difficulty='hard'):
        self.difficulty = difficulty
        self.max_depth = 2 if difficulty == 'easy' else 4
        self.time_limit = 1.9  # seconds

    def get_move(self, board, ai_stone=AI, player_stone=PLAYER):
        """
        Receives the current board state and returns the AI's move as (row, col).
        board: 2D list (15x15) with 0=empty, 1=player, 2=AI
        ai_stone: value representing AI stones
        player_stone: value representing player stones
        """
        start_time = time.time()
        if self.difficulty == 'easy':
            return self._random_move(board)
        else:
            # 1. Check for immediate win
            win_move = self._find_immediate_win(board, ai_stone)
            if win_move:
                return win_move
            # 2. Check for immediate block
            block_move = self._find_immediate_win(board, player_stone)
            if block_move:
                return block_move
            # 3. Otherwise, use minimax
            move = self._iterative_deepening(board, ai_stone, player_stone, start_time)
            if move is None:
                return self._random_move(board)
            return move

    def _random_move(self, board):
        empty = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if board[r][c] == EMPTY]
        return random.choice(empty) if empty else None

    def _find_immediate_win(self, board, stone):
        # Return a move (r, c) that creates five in a row for 'stone', or None
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] == EMPTY:
                    board[r][c] = stone
                    if self._check_win(board, stone, r, c):
                        board[r][c] = EMPTY
                        return (r, c)
                    board[r][c] = EMPTY
        return None

    def _iterative_deepening(self, board, ai_stone, player_stone, start_time):
        best_move = None
        for depth in range(2, self.max_depth + 1):
            move, _ = self._minimax(board, depth, True, ai_stone, player_stone, -float('inf'), float('inf'), start_time)
            if time.time() - start_time > self.time_limit:
                break
            if move is not None:
                best_move = move
        return best_move

    def _minimax(self, board, depth, maximizing, ai_stone, player_stone, alpha, beta, start_time):
        if time.time() - start_time > self.time_limit:
            return None, 0
        winner = self._check_win_full(board)
        if winner == ai_stone:
            return None, 1000000
        elif winner == player_stone:
            return None, -1000000
        elif self._is_full(board):
            return None, 0
        if depth == 0:
            return None, self._evaluate(board, ai_stone, player_stone)
        moves = self._generate_moves(board)
        best_move = None
        if maximizing:
            max_eval = -float('inf')
            for move in moves:
                r, c = move
                board[r][c] = ai_stone
                _, eval = self._minimax(board, depth-1, False, ai_stone, player_stone, alpha, beta, start_time)
                board[r][c] = EMPTY
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return best_move, max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                r, c = move
                board[r][c] = player_stone
                _, eval = self._minimax(board, depth-1, True, ai_stone, player_stone, alpha, beta, start_time)
                board[r][c] = EMPTY
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return best_move, min_eval

    def _generate_moves(self, board):
        # Only consider empty cells near existing stones (for efficiency)
        moves = set()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] != EMPTY:
                    for dr in range(-2, 3):
                        for dc in range(-2, 3):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                                if board[nr][nc] == EMPTY:
                                    moves.add((nr, nc))
        if not moves:
            # If board is empty, play center
            return [(BOARD_SIZE//2, BOARD_SIZE//2)]
        return list(moves)

    def _is_full(self, board):
        return all(board[r][c] != EMPTY for r in range(BOARD_SIZE) for c in range(BOARD_SIZE))

    def _check_win_full(self, board):
        # Returns the winner's stone value, or None if no winner
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] == EMPTY:
                    continue
                if self._check_five(board, r, c):
                    return board[r][c]
        return None

    def _check_win(self, board, stone, r, c):
        # Check if placing at (r, c) for 'stone' results in a win
        for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
            count = 1
            for d in [1, -1]:
                nr, nc = r, c
                while True:
                    nr += dr * d
                    nc += dc * d
                    if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == stone:
                        count += 1
                    else:
                        break
            if count >= 5:
                return True
        return False

    def _check_five(self, board, r, c):
        # Check all directions for five in a row
        stone = board[r][c]
        for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
            count = 1
            for d in [1, -1]:
                nr, nc = r, c
                while True:
                    nr += dr * d
                    nc += dc * d
                    if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == stone:
                        count += 1
                    else:
                        break
            if count >= 5:
                return True
        return False

    def _evaluate(self, board, ai_stone, player_stone):
        # Simple evaluation: count open-ended lines of length 2, 3, 4 for both sides
        def count_patterns(stone):
            score = 0
            patterns = [2, 3, 4]
            for length in patterns:
                score += self._count_open_lines(board, stone, length) * (10 ** length)
            return score
        return count_patterns(ai_stone) - count_patterns(player_stone)

    def _count_open_lines(self, board, stone, length):
        count = 0
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
                    if self._is_open_line(board, r, c, dr, dc, stone, length):
                        count += 1
        return count

    def _is_open_line(self, board, r, c, dr, dc, stone, length):
        # Check if there's an open-ended line of 'length' for 'stone' starting at (r, c)
        for i in range(length):
            nr, nc = r + dr*i, c + dc*i
            if not (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE):
                return False
            if board[nr][nc] != stone:
                return False
        before_r, before_c = r - dr, c - dc
        after_r, after_c = r + dr*length, c + dc*length
        before_empty = (0 <= before_r < BOARD_SIZE and 0 <= before_c < BOARD_SIZE and board[before_r][before_c] == EMPTY)
        after_empty = (0 <= after_r < BOARD_SIZE and 0 <= after_c < BOARD_SIZE and board[after_r][after_c] == EMPTY)
        return before_empty and after_empty

# Interface for integration
_ai_instance = None

def set_difficulty(level):
    global _ai_instance
    _ai_instance = GobangAI(difficulty=level)

def get_ai_move(board, ai_stone=AI, player_stone=PLAYER):
    """
    board: 2D list (15x15) with 0=empty, 1=player, 2=AI
    Returns: (row, col) tuple for AI's move
    """
    global _ai_instance
    if _ai_instance is None:
        _ai_instance = GobangAI()
    return _ai_instance.get_move(copy.deepcopy(board), ai_stone, player_stone)
