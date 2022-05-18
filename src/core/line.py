from core.primitive import Primitive
from core.point import Point

class Line(Primitive):
    def __init__(self, point1: Point, point2: Point):
        if point1.x > point2.x:
            self._p1 = point2
            self._p2 = point1
        else:
            self._p1 = point1
            self._p2 = point2

        self._a = None
        self._b = None

    def __str__(self):
        return f'({self._p1}), ({self._p2})'

    def to_plot(self):
        return (self.p1.to_plot(), self.p2.to_plot())

    @property
    def p1(self):
        return self._p1

    @property
    def p2(self):
        return self._p2

    @property
    def is_horizontal(self):
        return self._p1.y == self._p2.y

    @property
    def is_vertical(self):
        return self._p1.x == self._p2.x

    @property
    def a(self):
        """parameter a of line equation y = a * x + b"""
        if not self._a:
            try:
                self._a = (self._p2.y - self._p1.y) / (self._p2.x - self._p1.x)
            except ZeroDivisionError:
                self._a = None

        return self._a

    @property
    def b(self):
        """parameter b of line equation y = a * x + b"""
        if not self._b:
            self._b = self._p1.y - self.a * self._p1.x if not self.is_vertical else None

        return self._b

    def intersects(self, line):
        if self.is_vertical and line.is_vertical and \
           self.p1.x == line.p1.x and (min(self.p2.y - line.p2.y) >= max(self.p1.y, line.p1.y)):
            return True

        if self.is_horizontal and line.is_horizontal and \
           self.p1.y == line.p1.y and (min(self.p2.x, line.p2.x) >= max(self.p1.x, line.p1.x)):
            return True

        return bool(self.intersection_point(line))

    def intersection_point(self, line: 'Line'):
        if self.is_vertical and line.is_vertical:
            return

        if self.is_vertical and line.p1.x <= self.p1.x <= line.p2.x:
            y = self.p1.x * line.a + line.b
            if self.p1.y <= y <= self.p2.y or self.p1.y <= y <= self.p2.y:
                return Point(self.p1.x, y)

        if line.is_vertical and self.p1.x <= line.p1.x <= self.p2.x:
            y = line.p1.x * self.a + self.b
            if line.p1.y <= y <= line.p2.y or line.p2.y <= y <= line.p1.y:
                return Point(line.p1.x, y)

        if self.a == line.a == 0:
            return

        try:
            x = (self.b - line.b) / (line.a - self.a)
            y = self.a * x + self.b

            if line.p1.x <= x <= line.p2.x or line.p2.x <= x <= line.p1.x or \
               line.p1.y <= y <= line.p2.y or line.p2.y <= y <= line.p1.y:
                return Point(x, y)
        except Exception:
            return


if __name__ == '__main__':
    # test line parameters counting
    line = Line(Point(1, 1), Point(3,3))
    assert line.a == 1, 'wrong a, must be 1'
    assert line.b == 0, 'wrong b, must be 0'

    line = Line(Point(1, 1), Point(3,5))
    assert line.a == 2, 'wrong a, must be 1'
    assert line.b == -1, 'wrong b, must be 0'

    line = Line(Point(1, 1), Point(3,1))
    assert line.a == 0, 'wrong a, must be 0'
    assert line.b == 1, 'wrong b, must be 1'

    line = Line(Point(1, 1), Point(1,3))
    assert line.a == None, 'wrong a, must be None'
    assert line.b == None, 'wrong b, must be None'

    # test lines intersections
    line1 = Line(Point(1, 1), Point(5, 3))
    line2 = Line(Point(1, 2), Point(5, 2))
    assert line1.intersection_point(line2) == Point(3, 2), 'not Point(3, 2)'

    line1 = Line(Point(1, 1), Point(5, 3))
    line2 = Line(Point(1, 0), Point(1, 5))
    assert line1.intersection_point(line2) == Point(1, 1), 'not Point(1, 1)'

    line1 = Line(Point(1, 0), Point(1, 5))
    line2 = Line(Point(1, 1), Point(5, 2))
    assert line1.intersection_point(line2) == Point(1, 1), 'not Point(1, 1)'

    line1 = Line(Point(1, 0), Point(1, 5))
    line2 = Line(Point(1, 1), Point(5, 1))
    assert line1.intersection_point(line2) == Point(1, 1), 'not Point(1, 1)'

    line1 = Line(Point(1, 0), Point(1, 5))
    line2 = Line(Point(1, 2), Point(1, 4))
    assert not line1.intersection_point(line2), 'must be passed when both lines are vertical'

    line1 = Line(Point(1, 0), Point(5, 0))
    line2 = Line(Point(2, 0), Point(7, 0))
    assert not line1.intersection_point(line2), 'must be passed when both lines are horizontal'

