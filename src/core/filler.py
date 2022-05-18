import os

from matplotlib.pyplot import plot

from core.boundary import Boundary
from core.config import Config
from core.scan_line import ScanLine
from core.point import Point
from core.plotter import Plotter

config = Config()
boundary = Boundary()


class PointsFiller():
    def __init__(self, frame, polygons):
        self._frame = frame
        self._polygons = polygons

        self._p1 = None
        self._p2 = None
        self._i_coord = 0
        self._e_coord = 0
        # dirrection an time
        self._reverse = False

        self.__points = []

    def _line_gen(self):

        if config.direction == 'left-right':
            return ScanLine(
                Point(boundary.xmin, self._i_coord + self._frame.origin.y),
                Point(boundary.xmax, self._i_coord + self._frame.origin.y)
            )
        elif config.direction == 'down-top':
            return  ScanLine(
                Point(self._i_coord + self._frame.origin.x, boundary.ymin),
                Point(self._i_coord + self._frame.origin.x, boundary.ymax)
            )

        return

    @property
    def _d_x(self):
        return self._frame.points[0].x

    @property
    def _d_y(self):
        return self._frame.points[0].y

    def __init_line(self):
        self._i_coord = 0
        self._e_coord = config.frame_size

    def fill(self):
        for polygon in self._polygons:
            self.__init_line()
            while self._i_coord <= self._e_coord:
                scan_line = self._line_gen()
                if not scan_line:
                    break

                # print(f'scan line: {scan_line}')
                var = 'x' if scan_line.is_horizontal else 'y'

                for segment in scan_line.intersection_segments(polygon):
                    points = list(filter(
                        lambda p: getattr(self._frame.points[0], var) <= getattr(p, var) < getattr(self._frame.points[2], var),
                        segment.points_on_scan_line
                    ))

                    if self._reverse:
                        points = list(reversed(points))

                    self._reverse = not self._reverse
                    self.__points.extend(points)

                self._i_coord = round(self._i_coord + config.fib_step, 4)

    def __convert_coord(self, coord, is_y=False):
        if is_y:
            return config.frame_points - int((coord - self._frame.points[0].y) / config.fib_step) - 1

        return int((coord - self._frame.points[0].x) / config.fib_step)

    def print_points(self):
        path = os.path.join(config.output_path, f'frame_{self._frame}.txt')
        if not os.path.exists(config.output_path):
            os.makedirs(config.output_path, exist_ok=True)

        with open(path, 'w', encoding='utf8') as f:
            f.write('S\n')
            f.write(f'{len(self.__points)}\n')
            for p in self.__points:
                f.write(f'40000 {self.__convert_coord(p.x)} {self.__convert_coord(p.y, True)}\n')

        if config.debug:
            self._print_debug()


    def plot(self):
        path = os.path.join(config.output_path, 'plots', f'frame_{self._frame}.png')
        if not os.path.exists(config.output_path):
            os.mkdir(config.output_path)

        if not os.path.exists(os.path.join(config.output_path, 'plots')):
            os.mkdir(os.path.join(config.output_path, 'plots'))

        plotter = Plotter(config.frame_points, config.frame_points)

        plotter.plot(
            frames=[self._frame,],
            polygons=self._polygons,
            points=self.__points,
            d_x=self._frame.points[0].x,
            d_y=self._frame.points[0].y,
            output_path=path
        )

    def _print_debug(self):
        # print points
        os.mkdir(os.path.join(config.output_path, 'debug'))
        path = os.path.join(config.output_path, 'debug', f'frame_{self._frame}__not_converted.txt')
        with open(path, 'w', encoding='utf8') as f:
            for i, p in enumerate(self.__points):
                if i % 2048 == 0:
                    f.write(f'{p.x}, {p.y}\n')

        # print frame
        path = os.path.join(config.output_path, 'debug', f'frame.txt')
        with open(path, 'w', encoding='utf8') as f:
            for i, l in enumerate(self._frame.lines):
                f.write(f'{l.p1.x}, {l.p1.y}\n')
                f.write(f'{l.p2.x}, {l.p2.y}\n')

        # print polygons
        for i, polygon in enumerate(self._polygons):
            path = os.path.join(config.output_path, 'debug', f'polygon_{i}.txt')
            with open(path, 'w', encoding='utf8') as f:
                for i, l in enumerate(polygon.lines):
                    f.write(f'{l.p1.x}, {l.p1.y}\n')
                    f.write(f'{l.p2.x}, {l.p2.y}\n')
