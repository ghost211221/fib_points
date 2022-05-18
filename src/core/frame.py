from copy import copy

from numpy import size

from core.config import Config
from core.consts import sym_power_map
from core.line import Line
from core.point import Point
from core.polygon import Polygon

config = Config()

def create_frame(point, size):
    lines = [
        Line(point, Point(point.x + size, point.y)),
        Line(Point(point.x + size, point.y), Point(point.x + size, point.y + size)),
        Line(Point(point.x + size, point.y + size), Point(point.x, point.y + size)),
        Line(Point(point.x, point.y + size), point)
    ]

    return Frame(lines)

def create_frames(x_max, x_min, y_max, y_min, size):
    frames = []
    x = copy(x_min)
    y = copy(y_min)

    while y < y_max:
        while x < x_max:
            frame = create_frame(Point(x, y), size)
            frames.append(frame)

            x += size

        y += size
        x = copy(x_min)

    return frames

class Frame(Polygon):

    def __str__(self):
        return f'{round(self.points[0].x, 4)}_{round(self.points[0].y, 4)}__{round(self.points[2].x, 4)}_{round(self.points[2].y, 4)}'

    @property
    def origin(self):
        return self.points[0]

    @property
    def foreign(self):
        return self.points[2]

    def to_plot(self, d_x, d_y):
        points = []
        for p in self.points:
            points += [(p.x - d_x) * config.multiply, (p.y - d_y) * config.multiply]

        return points
    #     return [
    #         (self.points[0].x + delta_x) * config.multiply,
    #         (self.points[0].y + delta_y) * config.multiply,
    #         (self.points[2].x + delta_x) * config.multiply,
    #         (self.points[2].y + delta_y) * config.multiply
    #     ]


