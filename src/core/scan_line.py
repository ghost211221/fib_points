from core.config import Config
from core.line import Line
from core.point import Point

config = Config()

class ScanLine(Line):
    def __init__(self, point1: Point, point2: Point):
        super().__init__(point1, point2)

        self.__segments = []
        self.__points = []

    def intersection_segments(self, polygon):
        points = []
        for line in polygon.lines:
            point = self.intersection_point(line)
            if point:
                points.append(point)

        if not points:
            return []

        points.sort(key=lambda p: p.x if self.is_horizontal else p.y)

        lines = {}
        points.sort(key=lambda p: p.x)
        # make init lines from intersections of scan_line and polygon
        for i, point in enumerate(points[1:]):
            if point.x == points[i].x or abs(point.x - points[i].x) < config.fib_step:
                continue

            if i % 2 == 1:
                continue

            self.__segments.append(ScanLine(points[i], point))

        return self.__segments

    @property
    def __first_segment_point_on_grid(self):
        """segment must be horizontal"""
        def _process(val):
            a = abs(val // config.fib_step)
            b = abs(val) % config.fib_step
            if val < 0:
                return -1 * a * config.fib_step

            if b == 0:
                return a * config.fib_step

            return (a + 1) * config.fib_step

        if self.is_horizontal:
            return Point(_process(self.p1.x), self.p1.y)

        if self.is_vertical:
            return Point(self.p1.x, _process(self.p1.y))

        raise Exception('Unknown scan line type')

    @property
    def points_on_scan_line(self):
        first_point = self.__first_segment_point_on_grid

        temp = first_point.x if self.is_horizontal else first_point.y
        end = self.p2.x if self.is_horizontal else self.p2.y

        while temp < end:
            point = None
            if self.is_horizontal:
                point = Point(temp, first_point.y)
            elif self.is_horizontal:
                point = Point(first_point.yx, temp)
            else:
                raise Exception('Unknown scan line type')

            self.__points.append(point)

            temp += config.fib_step

        return self.__points
