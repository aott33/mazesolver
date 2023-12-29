from tkinter import Tk, BOTH, Canvas
import time
import random

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
            win = None,
            has_left_wall = True,
            has_right_wall = True,
            has_top_wall = True,
            has_bottom_wall = True,
            visited = False
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
        self.visited = visited

    def draw(self):
        top_left_point = Point(self._x1, self._y1)
        top_right_point = Point(self._x2, self._y1)
        bottom_left_point = Point(self._x1, self._y2)
        bottom_right_point = Point(self._x2, self._y2)
        

        if self.has_left_wall:
            self._win.draw_line(Line(top_left_point, bottom_left_point), "black")
        else:
            self._win.draw_line(Line(top_left_point, bottom_left_point), "white")
        if self.has_right_wall:
            self._win.draw_line(Line(top_right_point, bottom_right_point), "black")
        else:
            self._win.draw_line(Line(top_right_point, bottom_right_point), "white")
        if self.has_top_wall:
            self._win.draw_line(Line(top_left_point, top_right_point), "black")
        else:
            self._win.draw_line(Line(top_left_point, top_right_point), "white")
        if self.has_bottom_wall:
            self._win.draw_line(Line(bottom_left_point, bottom_right_point), "black")
        else:
            self._win.draw_line(Line(bottom_left_point, bottom_right_point), "white")
    
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
        win=None,
        seed=None
    ):
        if seed != None:
            random.seed(seed)
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._seed = seed
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()
    
    def _create_cells(self):
        for i in range(0, self._num_cols):
            col_list = []
            for j in range(0, self._num_rows):
                x1, x2, y1, y2 = self._calc_cell(i, j)
                cell = Cell(x1, x2, y1, y2, self._win)
                if cell._win != None:
                    cell.draw()
                    self._animate()
                col_list.append(cell)
            self._cells.append(col_list)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self._num_cols-1][self._num_rows-1].has_bottom_wall = False
        if self._win != None:
            self._cells[0][0].draw()
            self._animate()
            self._cells[self._num_cols-1][self._num_rows-1].draw()

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            to_visit = []
            directions = 0
            if i - 1 > 0 and not self._cells[i - 1][j].visited:
                to_visit.append([i - 1, j])
                directions += 1
            if j - 1 > 0 and not self._cells[i][j - 1].visited:
                to_visit.append([i, j - 1])
                directions += 1
            if i + 1 < self._num_cols and not self._cells[i + 1][j].visited:
                to_visit.append([i + 1, j])
                directions += 1
            if j + 1 < self._num_rows and not self._cells[i][j + 1].visited:
                to_visit.append([i, j + 1])
                directions += 1

            if directions == 0:
                if self._win != None:
                    self._cells[i][j].draw()
                return

            next_cell = to_visit[random.randint(0, len(to_visit)-1)]

            next_cell_i = next_cell[0]
            next_cell_j = next_cell[1]

            if next_cell_i < i:
                self._cells[i][j].has_left_wall = False
                self._cells[next_cell_i][next_cell_j].has_right_wall = False

            elif next_cell_i > i:
                self._cells[i][j].has_right_wall = False
                self._cells[next_cell_i][next_cell_j].has_left_wall = False
                
            elif next_cell_j < j:
                self._cells[i][j].has_top_wall = False
                self._cells[next_cell_i][next_cell_j].has_bottom_wall = False

            elif next_cell_j > j:
                self._cells[i][j].has_bottom_wall = False
                self._cells[next_cell_i][next_cell_j].has_top_wall = False

            if self._win != None:
                self._cells[i][j].draw()
                self._cells[next_cell_i][next_cell_j].draw()
                self._animate()

            self._break_walls_r(next_cell_i, next_cell_j)
    
    def _calc_cell(self, i, j):
        x1 = (self._cell_size_x * i) + self._x1
        x2 = x1 + self._cell_size_x
        y1 = (self._cell_size_y * j) + self._y1
        y2 = y1 + self._cell_size_y
        return x1, x2, y1, y2
    
    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)

    def _reset_cells_visited(self):
        for i in range(0, self._num_cols):
            for j in range(0, self._num_rows):
                self._cells[i][j].visited = False

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        directions = 0

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        
        if i - 1 > 0 and not self._cells[i - 1][j].visited and not self._cells[i][j].has_left_wall and not self._cells[i - 1][j].has_right_wall:
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                directions +=1
                return True
            self._cells[i][j].draw_move(self._cells[i - 1][j], True)

        if j - 1 > 0 and not self._cells[i][j - 1].visited and not self._cells[i][j].has_top_wall and not self._cells[i][j - 1].has_bottom_wall:
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j -1):
                directions +=1
                return True
            self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        if i + 1 < self._num_cols and not self._cells[i + 1][j].visited and not self._cells[i][j].has_right_wall and not self._cells[i + 1][j].has_left_wall:
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                directions +=1
                return True
            self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        if j + 1 < self._num_rows and not self._cells[i][j + 1].visited and not self._cells[i][j].has_bottom_wall and not self._cells[i][j + 1].has_top_wall:
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j+1):
                directions +=1
                return True
            self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        if directions == 0:
            return False


    def solve(self):
        solved = self._solve_r(0,0)
        return solved