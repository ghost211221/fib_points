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
        return round(self._x, 6) == round(other.x, 6) and round(self._y, 6) == round(other.y, 6)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __convert_coord(self, coord, frame, is_y=False):
        if is_y:
            return config.frame_points - round((coord - frame.points[0].y) / config.fib_step) - 1

        return int((coord - frame.points[0].x) / config.fib_step)

    def to_plot(self, d_x, d_y, frame):

        return [
            self.__convert_coord(self._x - d_x, frame)*2,
            self.__convert_coord((self._y - d_y), frame, is_y=True)*2
        ]

    def to_print(self, d_x, d_y, frame):
        return f'{self.__convert_coord(self._x - d_x, frame)} {self.__convert_coord(self._y - d_y, frame, is_y=True)}'
