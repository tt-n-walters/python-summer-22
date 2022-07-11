import os

import svgwrite as svg
from svgwrite import percent as pct



class Display:
    def __init__(self, rows, columns, padding):
        self.rows = rows
        self.columns = columns
        self.padding = padding
        self.filename = "pathfinding/maze.svg"
        self.drawing = svg.Drawing(self.filename, size=(500, 500))

        self.drawing.add(self.drawing.rect((0, 0), (500, 500), fill="grey"))
        print(f"Creating svg with {self.rows} rows, {self.columns} columns.")

    def draw_line(self, start, end):
        self.drawing.add(self.drawing.line(
            (start[0]*pct, start[1]*pct),
            (end[0]*pct, end[1]*pct),
            # tuple(map(pct, start)),
            # tuple(map(pct, end)),
            stroke="white", stroke_width=4, stroke_linecap="round"
        ))

    def draw_grid(self):
        cell_width = (100 - self.padding * 2) / self.columns
        cell_height = (100 - self.padding * 2) / self.rows

        for row in range(self.rows):
            for column in range(self.columns):
                x = self.padding + cell_width * column
                y = self.padding + cell_height * row
                top_left = x, y
                top_right = x + cell_width, y
                bottom_left = x, y + cell_height
                bottom_right = x + cell_width, y + cell_height

                self.draw_line(top_left, top_right)
                self.draw_line(top_right, bottom_right)
                self.draw_line(bottom_right, bottom_left)
                self.draw_line(bottom_left, top_left)
        self.drawing.save()
        print("Saved svg to", os.path.abspath(self.filename))



class Maze:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = [
            [{"up": True, "down": True, "left": True, "right": True, "visited": False}
                for _ in range(self.columns)]
                    for _ in range(self.rows)
        ]
        self.stack = [(self.columns // 2, self.rows // 2)]
        
    def step(self):
        # If the stack contains a cell, pop and use as current
        if self.stack:
            x, y = self.stack.pop(0)
            cell = self.grid[y][x]

            up = self.grid[y - 1][x]
            down = self.grid[y + 1][x]
            left = self.grid[y][x - 1]
            right = self.grid[y][x + 1]

            






        # Find all unvisited neighbours of current cell

        # If at least one neighbour, pick one randomly, and remove walls between

        # Add current position to the stack, repeat

        pass



Maze(11, 11)
Display(11, 11, 10).draw_grid()
Maze.step()