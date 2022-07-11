import svgwrite as svg
from svgwrite import percent as pct

def draw_line(drawing, start, end):
    drawing.add(drawing.line(
        (start[0]*pct, start[1]*pct),
        (end[0]*pct, end[1]*pct),
        # tuple(map(pct, start)),
        # tuple(map(pct, end)),
        stroke="red", stroke_width=10
    ))

drawing = svg.Drawing("pathfinding/maze.svg")

for row in range(4):
    for column in range(4):
        x = 10 + 20 * column
        y = 10 + 20 * row
        top_left = x, y
        top_right = x + 20, y
        bottom_left = x, y + 20
        bottom_right = x + 20, y + 20
        draw_line(drawing, top_left, top_right)
        draw_line(drawing, top_right, bottom_right)
        draw_line(drawing, bottom_right, bottom_left)
        draw_line(drawing, bottom_left, top_left)
drawing.save()
