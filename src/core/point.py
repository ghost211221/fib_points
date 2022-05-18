
from core.config import Config
from core.primitive import Primitive

config = Config()

class Point(Primitive):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __str__(self):
        return f'{self._x}, {self._y}'

    def __eq__(self, other: 'Point'):
        return self._x == other.x and self._y == other.y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def to_plot(self, d_x, d_y):

        return [
            (self._x - d_x) * config.multiply,
            (self._y - d_y) * config.multiply
        ]