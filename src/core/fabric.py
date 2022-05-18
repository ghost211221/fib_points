from core.point import Point
from core.line import Line
from core.polygon import Polygon
from core.frame import Frame

class Fabric():

    @staticmethod
    def create_from_points(points: list or tuple):
        lines = []

        # first add line from last to first point
        lines.append(Line(Point(points[0][0], points[0][1]), Point(points[-1][0], points[-1][1])))
        # and other lines
        buf = []
        for coord in points:
            if len(buf) < 2:
                buf.append(coord)

            if len(buf) == 2:
                lines.append(Line(Point(buf[0][0], buf[0][1]), Point(buf[1][0], buf[1][1])))
                buf = []
                buf.append(coord)

        return Polygon(lines)
