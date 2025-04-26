# Gobang AI Module (ai.py)

## Overview
This module implements a strong AI opponent for Gobang (Five in a Row) with two difficulty levels: 'easy' and 'hard'. It is designed for integration with the main game engine as specified in architecture.txt.

## AI Approach
- **Easy Mode**: The AI selects a random valid move.
- **Hard Mode**: The AI uses Minimax search with Alpha-Beta pruning and iterative deepening. The search is limited to a maximum depth (default 4) and a time limit of 2 seconds per move. The evaluation function considers open-ended lines of length 2, 3, and 4 for both the AI and the player.

## Interface
- `set_difficulty(level)`: Set the AI difficulty ('easy' or 'hard').
- `get_ai_move(board, ai_stone=2, player_stone=1)`: Given the current board state (2D list), returns the AI's move as a (row, col) tuple.

## Performance
- The AI guarantees a move within 2 seconds.
- The hard mode is competitive and suitable for experienced players.

## Integration
- The module is stateless except for the difficulty setting.
- Designed for direct use by integration.py or main.py as per the architecture.

---
For questions or suggestions, please contact the AI module maintainer.
