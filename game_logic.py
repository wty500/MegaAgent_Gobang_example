"""
Gobang Game Logic Module
-----------------------
Manages the Gobang board state, move validation, placement, turn management, and win detection.
Exposes a clear interface for integration with main.py and AI modules.
"""

from typing import List, Optional, Tuple

BOARD_SIZE = 15
EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2

class GobangGame:
    """
    Core Gobang game logic: board management, move validation, placement, turn management, and win detection.
    """
    def __init__(self):
        """Initialize a new Gobang game with an empty board and set the starting player."""
        self.board: List[List[int]] = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player: int = PLAYER_1
        self.winner: Optional[int] = None
        self.move_count: int = 0
        self.last_move: Optional[Tuple[int, int]] = None

    def reset(self):
        """Reset the game to the initial state."""
        self.__init__()

    def get_board(self) -> List[List[int]]:
        """Return a deep copy of the current board state."""
        return [row[:] for row in self.board]

    def get_current_player(self) -> int:
        """Return the player whose turn it is (PLAYER_1 or PLAYER_2)."""
        return self.current_player

    def is_valid_move(self, row: int, col: int) -> bool:
        """Check if a move is valid (within bounds and on an empty cell)."""
        return (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == EMPTY and self.winner is None)

    def make_move(self, row: int, col: int) -> bool:
        """
        Place a stone for the current player at (row, col) if valid.
        Returns True if the move was successful, False otherwise.
        Updates the game state and checks for a win.
        """
        if not self.is_valid_move(row, col):
            return False
        self.board[row][col] = self.current_player
        self.last_move = (row, col)
        self.move_count += 1
        if self.check_win(row, col):
            self.winner = self.current_player
        else:
            self.current_player = PLAYER_1 if self.current_player == PLAYER_2 else PLAYER_2
        return True

    def check_win(self, row: int, col: int) -> bool:
        """
        Check if placing a stone at (row, col) wins the game for the current player.
        Returns True if the current player has five in a row.
        """
        directions = [
            (1, 0),   # vertical
            (0, 1),   # horizontal
            (1, 1),   # diagonal down-right
            (1, -1),  # diagonal down-left
        ]
        player = self.board[row][col]
        for dr, dc in directions:
            count = 1
            # Check in the positive direction
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            # Check in the negative direction
            r, c = row - dr, col - dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
            if count >= 5:
                return True
        return False

    def get_winner(self) -> Optional[int]:
        """Return the winner (PLAYER_1 or PLAYER_2), or None if no winner yet."""
        return self.winner

    def is_full(self) -> bool:
        """Return True if the board is full (draw), False otherwise."""
        return self.move_count >= BOARD_SIZE * BOARD_SIZE and self.winner is None

    def get_last_move(self) -> Optional[Tuple[int, int]]:
        """Return the coordinates of the last move made, or None if no moves have been made."""
        return self.last_move

    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """Return a list of all valid (row, col) moves on the current board."""
        if self.winner is not None:
            return []
        return [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.board[r][c] == EMPTY]
