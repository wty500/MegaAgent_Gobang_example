"""
Script to fill the Gobang board completely without forming any five-in-a-row (true draw scenario).
This script can be used for integration testing to validate draw detection logic.
"""
from game_logic import GobangGame, PLAYER_1, PLAYER_2, BOARD_SIZE

def generate_draw_moves():
    # Fill the board in a checkerboard pattern, which guarantees no five in a row
    moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            # Alternate players in a checkerboard pattern
            if (r + c) % 2 == 0:
                moves.append((r, c, PLAYER_1))
            else:
                moves.append((r, c, PLAYER_2))
    return moves

def play_draw_game():
    game = GobangGame()
    moves = generate_draw_moves()
    for r, c, player in moves:
        # Set the current player explicitly to avoid turn issues
        game.current_player = player
        assert game.make_move(r, c), f"Move ({r},{c}) by player {player} failed!"
        assert game.get_winner() is None, f"Unexpected win detected at ({r},{c})!"
    assert game.is_full(), "Board should be full (draw)!"
    assert game.get_winner() is None, "There should be no winner (draw)!"
    print("Draw scenario test passed: Board is full and no winner.")

if __name__ == "__main__":
    play_draw_game()
