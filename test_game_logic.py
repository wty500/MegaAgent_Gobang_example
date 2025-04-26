import unittest
from game_logic import GobangGame, PLAYER_1, PLAYER_2, EMPTY, BOARD_SIZE

class TestGobangGame(unittest.TestCase):
    def setUp(self):
        self.game = GobangGame()

    def test_initial_state(self):
        self.assertEqual(self.game.get_current_player(), PLAYER_1)
        self.assertIsNone(self.game.get_winner())
        self.assertEqual(self.game.move_count, 0)
        self.assertEqual(len(self.game.get_board()), BOARD_SIZE)
        self.assertTrue(all(cell == EMPTY for row in self.game.get_board() for cell in row))

    def test_valid_move(self):
        self.assertTrue(self.game.is_valid_move(0, 0))
        self.assertTrue(self.game.make_move(0, 0))
        self.assertFalse(self.game.is_valid_move(0, 0))  # Already occupied
        self.assertFalse(self.game.make_move(0, 0))
        self.assertEqual(self.game.get_board()[0][0], PLAYER_1)

    def test_turn_switching(self):
        self.game.make_move(0, 0)
        self.assertEqual(self.game.get_current_player(), PLAYER_2)
        self.game.make_move(0, 1)
        self.assertEqual(self.game.get_current_player(), PLAYER_1)

    def test_win_horizontal(self):
        for col in range(5):
            self.game.make_move(0, col)
            if col < 4:
                self.game.make_move(1, col)  # Alternate moves
        self.assertEqual(self.game.get_winner(), PLAYER_1)

    def test_win_vertical(self):
        for row in range(5):
            self.game.make_move(row, 0)
            if row < 4:
                self.game.make_move(row, 1)
        self.assertEqual(self.game.get_winner(), PLAYER_1)

    def test_win_diagonal(self):
        for i in range(5):
            self.game.make_move(i, i)
            if i < 4:
                self.game.make_move(i, i+1)
        self.assertEqual(self.game.get_winner(), PLAYER_1)

    def test_win_anti_diagonal(self):
        for i in range(5):
            self.game.make_move(i, 4-i)
            if i < 4:
                self.game.make_move(i, 5-i)
        self.assertEqual(self.game.get_winner(), PLAYER_1)

    def test_draw(self):
        # Fill the board without any winner, alternate moves to avoid 5 in a row
        player = PLAYER_1
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.game.board[r][c] = player
                self.game.move_count += 1
                player = PLAYER_2 if player == PLAYER_1 else PLAYER_1
        self.game.winner = None
        self.assertTrue(self.game.is_full())
        self.assertIsNone(self.game.get_winner())

    def test_reset(self):
        self.game.make_move(0, 0)
        self.game.reset()
        self.assertEqual(self.game.get_current_player(), PLAYER_1)
        self.assertIsNone(self.game.get_winner())
        self.assertEqual(self.game.move_count, 0)
        self.assertTrue(all(cell == EMPTY for row in self.game.get_board() for cell in row))

    def test_get_valid_moves(self):
        self.assertEqual(len(self.game.get_valid_moves()), BOARD_SIZE * BOARD_SIZE)
        self.game.make_move(0, 0)
        self.assertNotIn((0, 0), self.game.get_valid_moves())

if __name__ == '__main__':
    unittest.main()
