from tkinter import Tk, BOTH, Canvas
import time

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.canvas = Canvas(self.__root, width= self.width, height= self.height, bg="white")
        self.canvas.pack()
        self.window_is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.window_is_running = True
        while self.window_is_running:
            self.redraw()

    def close(self):
        self.window_is_running = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.point1 = p1
        self.point2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2
        )
        canvas.pack()

class Cell:
    def __init__( 
            self,
            x1,
            x2,
            y1,
            y2,
            win,
            has_left_wall = True,
            has_right_wall = True,
            has_top_wall = True,
            has_bottom_wall = True
        ):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = win

    def draw(self):
        top_left_point = Point(self._x1, self._y1)
        top_right_point = Point(self._x2, self._y1)
        bottom_left_point = Point(self._x1, self._y2)
        bottom_right_point = Point(self._x2, self._y2)
        

        if self.has_left_wall:
            self._win.draw_line(Line(top_left_point, bottom_left_point), "black")
        if self.has_right_wall:
            self._win.draw_line(Line(top_right_point, bottom_right_point), "black")
        if self.has_top_wall:
            self._win.draw_line(Line(top_left_point, top_right_point), "black")
        if self.has_bottom_wall:
            self._win.draw_line(Line(bottom_left_point, bottom_right_point), "black")
    
    def draw_move(self, to_cell, undo=False):
        line_color = "red"
        if undo:
            line_color = "gray"
        middle_y1 = (self._y1 + self._y2)/2
        middle_y2 = (to_cell._y1 + to_cell._y2)/2
        start_point = Point(self._x1, middle_y1)
        end_point = Point(to_cell._x2, middle_y2)

        self._win.draw_line(Line(start_point, end_point), line_color)


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()
    
    def _create_cells(self):
        for i in range(0, self._num_cols):
            col_list = []
            for j in range(0, self._num_rows):
                x1, x2, y1, y2 = self._calc_cell(i, j)
                cell = Cell(x1, x2, y1, y2, self._win)
                cell.draw()
                self._animate()
                col_list.append(cell)
            self._cells.append(col_list)
    
    def _calc_cell(self, i, j):
        x1 = (self._cell_size_x * i) + self._x1
        x2 = x1 + self._cell_size_x
        y1 = (self._cell_size_y * j) + self._y1
        y2 = y1 + self._cell_size_y
        return x1, x2, y1, y2
    
    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)
        


win = Window(800, 600)
maze = Maze(30, 30, 10, 10, 50, 50, win)

# cell1 = Cell(110, 150, 110, 150, win, True, False)
# cell2 = Cell(150, 190, 110, 150, win, False)

# cell1.draw()
# cell2.draw()
# cell1.draw_move(cell2)

# win.draw_line(Line(Point(20, 50), Point(50, 50)), "red")
# win.draw_line(Line(Point(50, 50), Point(100, 100)), "red")
# win.draw_line(Line(Point(100, 100), Point(100, 500)), "red")

win.wait_for_close()