import os
import random

import svgwrite as svg
from svgwrite import percent as pct


class Display:
    def __init__(self, maze, padding):
        self.maze = maze
        self.rows = maze.rows
        self.columns = maze.columns
        self.padding = padding
        self.filename = "pathfinding/maze.svg"
        self.drawing = svg.Drawing(self.filename, size=(500, 500))

        bg = self.drawing.rect((0, 0), (500, 500), fill="navy")
        # bg.add(self.drawing.animate("fill", values=["red", "green", "blue", "green", "red"], begin="0s", dur="5s", repeatCount="indefinite"))
        self.drawing.add(bg)

        print(f"Creating svg with {self.rows} rows, {self.columns} columns.")

    def draw_line(self, start, end, lifetime=None):
        line = self.drawing.line(
            (start[0]*pct, start[1]*pct),
            (end[0]*pct, end[1]*pct),
            # tuple(map(pct, start)),
            # tuple(map(pct, end)),
            stroke="white", stroke_width=4, stroke_linecap="round"
        )
        if lifetime:
            time = f"{lifetime}s"
            # begin_time = str(lifetime) + "s"
            line.add(self.drawing.animate("opacity", values=[1, 0], begin=time, dur="0.25s", fill="freeze"))
        self.drawing.add(line)

    def draw_grid(self):
        cell_width = (100 - self.padding * 2) / self.columns
        cell_height = (100 - self.padding * 2) / self.rows

        walls_removed = list(self.maze.generator)

        for row in range(self.rows):
            for column in range(self.columns):
                x = self.padding + cell_width * column
                y = self.padding + cell_height * row
                cell = self.maze.grid[row][column]
                top_left = x, y
                top_right = x + cell_width, y
                bottom_left = x, y + cell_height
                bottom_right = x + cell_width, y + cell_height
                
                line_data = zip(
                    ("up", "right", "down", "left"),
                    (top_left, top_right, bottom_right, bottom_left),
                    (top_right, bottom_right, bottom_left, top_left)
                )
                for direction, start, end in line_data:
                    if not cell[direction]:
                        lifetime = random.random() * 5 + 1
                    else:
                        lifetime = None
                    self.draw_line(start, end, lifetime)

        self.drawing.save(pretty=True)
        print("Saved svg to", os.path.abspath(self.filename))



class Maze:
    directions = ["up", "down", "left", "right"]
    opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = [
            [{"up": True, "down": True, "left": True, "right": True, "visited": False}
                for _ in range(self.columns)]
                    for _ in range(self.rows)
        ]
        self.stack = [(self.columns // 2, self.rows // 2)]
        self.generator = self.generate()
        
    def step(self):
        # If the stack contains a cell, pop and use as current
        if self.stack:
            x, y = self.stack.pop()
            cell = self.grid[y][x]
            cell["visited"] = True

            # Find all unvisited neighbours of current cell
            up = x, y - 1
            down = x, y + 1
            left = x - 1, y
            right = x + 1, y

            neighbours = []
            for vector, direction in zip([up, down, left, right], Maze.directions):
                if self.valid_cell(*vector):
                    neighbour = self.grid[vector[1]][vector[0]]
                    neighbours.append((neighbour, direction))

            if neighbours:
                # If at least one neighbour, pick one randomly, and remove walls between
                next_cell, direction = random.choice(neighbours)
                # Removes the wall from the current cell
                opposite = Maze.opposites[direction]
                cell[direction] = False
                next_cell[opposite] = False

                if direction == "up": next_position = (x, y - 1)
                if direction == "down": next_position = (x, y + 1)
                if direction == "left": next_position = (x - 1, y)
                if direction == "right": next_position = (x + 1, y)
                
                # Add current position to the stack, repeat
                self.stack.append((x, y))
                self.stack.append(next_position)

                return (x, y, direction), (*next_position, opposite)
            else:
                # Run when in dead-end, no possible neighbours
                pass

    def valid_cell(self, x, y):    # Predicate function
        # Check if y is between 0 and number of rows
        # Check if x is between 0 and number of columns
        # If so, then check if the cell has been visited
        return 0 <= x < self.columns and 0 <= y < self.rows and self.grid[y][x]["visited"] == False
    
    def generate(self):
        while self.stack:
            walls = self.step()
            yield walls


if __name__ == "__main__":
    maze = Maze(5, 5)
    Display(maze, 10).draw_grid()
