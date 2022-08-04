
from core.polygon import Polygon
from core.point import Point
from core.line import Line
from core.boundary import Boundary

boundary = Boundary()

boundary.set_boundary(-10, 10, -10, 10)

p1 = Polygon(
    lines = [
        Line(Point(-9, -9), Point(9, -9)),
        Line(Point(9, -9), Point(9, 9)),
        Line(Point(9, 9), Point(-9, 9)),
        Line(Point(-9, 9), Point(-9, -9)),
    ], 
    points=[]
)

p2 = Polygon(
        lines = [
        Line(Point(-7, -7), Point(7, -7)),
        Line(Point(7, -7), Point(7, 7)),
        Line(Point(7, 7), Point(-7, 7)),
        Line(Point(-7, 7), Point(-7, -7)),
    ], 
    points=[]
)

assert p1.intersect_polygon(p2)

p3 = Polygon(
    lines = [
        Line(Point(-5, -5), Point(5, -5)),
        Line(Point(5, -5), Point(5, 5)),
        Line(Point(5, 5), Point(-5, 5)),
        Line(Point(-5, 5), Point(-5, -5)),
    ], 
    points=[]
)

p4 = Polygon(
        lines = [
        Line(Point(-7, -7), Point(7, -7)),
        Line(Point(7, -7), Point(7, 7)),
        Line(Point(7, 7), Point(-7, 7)),
        Line(Point(-7, 7), Point(-7, -7)),
    ], 
    points=[]
)

assert p3.intersect_polygon(p4)

p5 = Polygon(
    lines = [
        Line(Point(-5, -5), Point(5, -5)),
        Line(Point(5, -5), Point(5, 5)),
        Line(Point(5, 5), Point(-5, 5)),
        Line(Point(-5, 5), Point(-5, -5)),
    ], 
    points=[]
)

p6 = Polygon(
        lines = [
        Line(Point(-7, -7), Point(3, -7)),
        Line(Point(3, -7), Point(3, 7)),
        Line(Point(3, 7), Point(-7, 7)),
        Line(Point(-7, 7), Point(-7, -7)),
    ], 
    points=[]
)

assert p5.intersect_polygon(p6)

p7 = Polygon(
    lines = [
        Line(Point(4, -5), Point(5, -5)),
        Line(Point(5, -5), Point(5, 5)),
        Line(Point(5, 5), Point(4, 5)),
        Line(Point(4, 5), Point(4, -5)),
    ], 
    points=[]
)

p8 = Polygon(
    lines=[
        Line(Point(-7, -7), Point(3, -7)),
        Line(Point(3, -7), Point(3, 7)),
        Line(Point(3, 7), Point(-7, 7)),
        Line(Point(-7, 7), Point(-7, -7)),
    ], 
    points=[]
)

assert not p7.intersect_polygon(p8)

p7 = Polygon(
    lines = [
        Line(Point(3, -5), Point(5, -5)),
        Line(Point(5, -5), Point(5, 5)),
        Line(Point(5, 5), Point(3, 5)),
        Line(Point(3, 5), Point(3, -5)),
    ], 
    points=[]
)

p8 = Polygon(
    lines=[
        Line(Point(-7, -7), Point(3, -7)),
        Line(Point(3, -7), Point(3, 7)),
        Line(Point(3, 7), Point(-7, 7)),
        Line(Point(-7, 7), Point(-7, -7)),
    ], 
    points=[]
)

assert not p7.intersect_polygon(p8)