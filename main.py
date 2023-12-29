import maze

win = maze.Window(800, 600)
maze = maze.Maze(30, 30, 10, 9, 50, 50, win, 1)

win.wait_for_close()