"""
main.py - Gobang Command-Line Interface
--------------------------------------
Integrates game_logic.py (GobangGame) and ai.py (GobangAI) to provide a playable CLI Gobang game against a strong AI.
"""

import sys
from game_logic import GobangGame, PLAYER_1, PLAYER_2, BOARD_SIZE
import ai

def print_board(board):
    print("   " + " ".join(f"{i:2}" for i in range(BOARD_SIZE)))
    for idx, row in enumerate(board):
        print(f"{idx:2} " + " ".join(['.' if cell == 0 else ('X' if cell == 1 else 'O') for cell in row]))

def get_user_move(game):
    while True:
        try:
            move = input("Enter your move as 'row col': ").strip()
            if move.lower() in ['q', 'quit', 'exit']:
                print("Exiting game.")
                sys.exit(0)
            row, col = map(int, move.split())
            if game.is_valid_move(row, col):
                return row, col
            else:
                print("Invalid move. Please try again.")
        except Exception:
            print("Invalid input. Please enter row and column as two integers (e.g., '7 7').")

def choose_difficulty():
    while True:
        diff = input("Choose AI difficulty (easy/hard): ").strip().lower()
        if diff in ['easy', 'hard']:
            return diff
        print("Invalid choice. Please enter 'easy' or 'hard'.")

def choose_player_stone():
    while True:
        stone = input("Do you want to play as X (first) or O (second)? (X/O): ").strip().upper()
        if stone in ['X', 'O']:
            return stone
        print("Invalid choice. Please enter 'X' or 'O'.")

def main():
    print("Welcome to Gobang (Five in a Row)!")
    difficulty = choose_difficulty()
    ai.set_difficulty(difficulty)
    player_stone_choice = choose_player_stone()
    player_stone = PLAYER_1 if player_stone_choice == 'X' else PLAYER_2
    ai_stone = PLAYER_2 if player_stone == PLAYER_1 else PLAYER_1

    game = GobangGame()
    print_board(game.get_board())

    while True:
        current_player = game.get_current_player()
        if current_player == player_stone:
            print("Your turn ({}):".format('X' if player_stone == PLAYER_1 else 'O'))
            row, col = get_user_move(game)
        else:
            print("AI is thinking...")
            row, col = ai.get_ai_move(game.get_board(), ai_stone, player_stone)
            print(f"AI moves at: {row} {col}")
        game.make_move(row, col)
        print_board(game.get_board())
        winner = game.get_winner()
        if winner:
            print("{} wins!".format('You' if winner == player_stone else 'AI'))
            break
        if game.is_full():
            print("It's a draw!")
            break
    print("Game over.")

if __name__ == "__main__":
    main()
