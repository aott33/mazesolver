import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells1(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
    def test_maze_create_cells2(self):
        num_cols = 5
        num_rows = 5
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
    def test_maze_create_cells3(self):
        num_cols = 40
        num_rows = 40
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_cell_visited_resets1(self):
        num_cols = 10
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)

        anyTrue = False

        for i in range(0, m1._num_cols):
            for j in range(0, m1._num_rows):
                if m1._cells[i][j].visited == True:
                    anyTrue = True

        self.assertNotEqual(
            anyTrue,
            True
        )
    
if __name__ == "__main__":
    unittest.main()