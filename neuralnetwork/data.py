import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import itertools


def classify(line, point):
    #   y = m*x + c
    #   c = y - m*x
    c = 0
    dx = line[1][0] - line[0][0]
    dy = line[1][1] - line[0][1]
    line_gradient = dy / dx
    c = line[1][1] - line_gradient * line[1][0]

    line_y = line_gradient * point[0] + c
    if point[1] > line_y:
        return 1
    else:
        return 0


def create_points():
    points = [(random.random() * 200 - 100, random.random() * 200 - 100)
              for _ in range(400)]
    return points


def label_points(line, points):
    labelled = []
    for point in points:
        label = classify(line, point)
        # labelled.append((point[0], point[1], label))
        labelled.append((*point, label))
    return labelled


def create_line():
    line = []
    for _ in range(2):
        fixed = random.choice([-100, 100])
        if random.random() < 0.5:
            point = fixed, random.random() * 200 - 100
        else:
            point = random.random() * 200 - 100, fixed
        line.append(point)
    
    if line[0][0] == line[1][0] or line[0][1] == line[1][1]:
        return create_line()
    else:
        return line


def draw(line):
    print("Getting ready to display...")

    plt.style.use("ggplot")
    # plt.figure(figsize=(5, 5))
    gathered_points = []
    all_colours = []

    while True:
        points = yield
        if points is None:
            break
        points_array = np.array(points)

        if points_array.shape[1] == 3:
            colours = []
            # 0 -> 0
            # 1 -> 0
            # 0.5 -> 1
            for confidence in points_array[:, 2]:
                r = max(0, confidence - 0.5) * 2
                g = (0.5 - abs(0.5 - confidence)) * 2
                b = max(0, 0.5 - confidence) * 2
                colour = [r, g, b]
                colours.append(colour)
        else:
            colours = ["black"] * len(points_array)

        gathered_points.append(points_array)
        all_colours.append(colours)
        
    gathered_points = np.array(gathered_points)


    figure, axes = plt.subplots(figsize=(5, 5))
    axes.set_xlim(-110, 110)
    axes.set_ylim(-110, 110)
    sct = axes.scatter([], [])
    

    def step(index):
        sct.set_offsets(gathered_points[index, :, :2])
        sct.set_color(all_colours[index])
        axes.set_title(index)
        return sct
    
    animation = FuncAnimation(figure, step, frames=len(gathered_points), interval=100, repeat=False, init_func=lambda *args, **kwargs: None)

    if line:
        line_array = np.array(line)
        plt.plot(line_array[:, 0], line_array[:, 1], c="c")
    
    plt.show()


def display(*points, line=None):
    try:
        displayer = draw(line)
        next(displayer)
        for p in points:
            displayer.send(p)
        next(displayer)
    except StopIteration:
        pass
