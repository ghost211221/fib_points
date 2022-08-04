from core.point import Point
from core.line import Line
from core.polygon import Polygon

class Fabric():

    @staticmethod
    def create_from_points(points: list or tuple):
        lines = []
        points_ = []
        
        for i, p in enumerate(points):
            lp = points[i-1]
            lines.append(Line(Point(lp[0], lp[1]), Point(p[0], p[1])))
            points_.append(Point(p[0], p[1]))

        return Polygon(lines, points=points_)
