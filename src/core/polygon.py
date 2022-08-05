from core.boundary import Boundary
from core.line import Line
from core.point import Point
from core.primitive import Primitive


boundary = Boundary()


class Polygon(Primitive):
    def __init__(self, lines, points=[]):
        self._lines = lines
        self._rectangles = []
        self._points = points

        self.__projection_x = None
        self.__projection_y = None

    def __str__(self):
        return '\n'.join([str(p) for p in self.points])

    @property
    def projection_x(self):
        if not self.__projection_x:
            x_coords = [p.x for p in self.points]
            self.__projection_x = (min(x_coords), max(x_coords))

        return self.__projection_x

    @property
    def projection_y(self):
        if not self.__projection_y:
            y_coords = [p.y for p in self.points]
            self.__projection_y = (min(y_coords), max(y_coords))

        return self.__projection_y

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
        for p in self.points:
            points.append((p.x, p.y))


        return points

    def has_point(self, point):
        beam = Line(point, Point(boundary.xmax, boundary.ymax))
        intersections = set()
        for l in self.lines:
            if l.point_on_line(point):
                return

            if beam.intersects(l):
                p = beam.intersection_point(l)
                intersections.add((round(p.x, 3), round(p.y, 3)))

        if len(intersections) % 2 == 1:
            return True

    def intersect_polygon(self, polygon: 'Polygon'):
        """detect intersection of two polygons
        firt of all check than axis projections are overlaped

        3 situations:
        1 - A lies in B
        2 - B lies in A
        3 - intersections of polygon sides
        """

        x1_1, x1_2 = self.projection_x
        x2_1, x2_2 = polygon.projection_x

        y1_1, y1_2 = self.projection_y
        y2_1, y2_2 = polygon.projection_y

        if not ((min((x1_2, x2_2)) >= max((x1_1, x2_1))) and (min((y1_2, y2_2)) >= max((y1_1, y2_1)))):
            return

        # situation 1
        for p in polygon.points:
            if self.has_point(p):
                return True


        # situation 2
        for p in self.points:
            if polygon.has_point(p):
                return True

        for sl in self.lines:
            for pl in polygon.lines:
                if sl.intersects(pl):
                    p = sl.intersection_point(pl)
                    if not ((p and p in (sl.p1, sl.p2, pl.p1, pl.p2)) or sl.co_parallel(pl)):
                        return True
