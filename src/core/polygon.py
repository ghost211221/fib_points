from core.config import Config

config = Config()
from core.primitive import Primitive


class Polygon(Primitive):
    def __init__(self, lines):
        self._lines = lines
        self._rectangles = []
        self._points = []

    def __str__(self):
        return ' '.join([str(p) for p in self.points])

    @property
    def points(self):
        def __exists(point):
            for p in self._points:
                if p == point:
                    return True

        if not self._points:
            for line in self._lines:
                if not __exists(line.p1):
                    self._points.append(line.p1)
                if not __exists(line.p2):
                    self._points.append(line.p2)

        return self._points

    @property
    def lines(self):
        return self._lines

    def to_plot(self, d_x, d_y):
        points = []
        for l in self.lines:
            points.append((l.p1.x - d_x) * config.multiply)
            points.append((l.p1.y - d_y) * config.multiply)
            points.append((l.p2.x - d_x) * config.multiply)
            points.append((l.p2.y - d_y) * config.multiply)

        return points