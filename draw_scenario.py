"""
Script to fill the Gobang board completely without forming any five-in-a-row (true draw scenario).
This script can be used for integration testing to validate draw detection logic.
"""
from game_logic import GobangGame, PLAYER_1, PLAYER_2, BOARD_SIZE

def generate_draw_moves():
    # Fill the board in a way that avoids any five-in-a-row in all directions
    # We use a shifted checkerboard pattern every row to break diagonal alignments
    moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            # Shift the pattern every row to break diagonals
            if ((r % 2 == 0 and c % 2 == 0) or (r % 2 == 1 and c % 2 == 1)):
                player = PLAYER_1 if (r % 4 < 2) else PLAYER_2
            else:
                player = PLAYER_2 if (r % 4 < 2) else PLAYER_1
            moves.append((r, c, player))
    return moves

def play_draw_game():
    game = GobangGame()
    moves = generate_draw_moves()
    for r, c, player in moves:
        game.current_player = player
        assert game.make_move(r, c), f"Move ({r},{c}) by player {player} failed!"
        assert game.get_winner() is None, f"Unexpected win detected at ({r},{c})!"
    assert game.is_full(), "Board should be full (draw)!"
    assert game.get_winner() is None, "There should be no winner (draw)!"
    print("Draw scenario test passed: Board is full and no winner.")

if __name__ == "__main__":
    play_draw_game()
