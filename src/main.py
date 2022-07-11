import argparse
import logging
from datetime import datetime
from math import ceil
import os

from numpy import float64

from core.boundary import Boundary
from core.config import Config
from core.filler import PointsFiller
from core.frame import create_frames
from core.line import Line
from core.point import Point
from core.plotter import Plotter
from gds_parser import GDSParser

def get_boundary(polygons):
    x_max = polygons[0].points[0].x
    x_min = polygons[0].points[0].x
    y_max = polygons[0].points[0].y
    y_min = polygons[0].points[0].y

    for polygon in polygons:
        for point in polygon.points:
            if not x_max or point.x > x_max:
                x_max = point.x
            if not x_min or point.x < x_min:
                x_min = point.x
            if not y_max or point.y > y_max:
                y_max = point.y
            if not y_min or point.y < y_min:
                y_min = point.y

    return x_max, x_min, y_max, y_min

def map_frame_polygons(frames, polygons):
    """map polygons to frames, one polygon may be placed in several frames"""
    def _check_polygon_in_frame(frame, polygon):
        """ whole polygon in frame """
        for p in polygon.points:
            if frame.origin.x <= p.x <= frame.foreign.x and frame.origin.y <= p.y <= frame.foreign.y:
                return True

    map_fp = {}

    for frame in frames:
        for polygon in polygons:
            if _check_polygon_in_frame(frame, polygon):
                if frame not in map_fp:
                    map_fp[frame] = []
                map_fp[frame].append(polygon)

    return map_fp



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('gds_file', help="input GDSII file name with path")
    parser.add_argument('direction', default="left-right", help="beam movement direction, possuble valuses are: left-rignt or down-top")
    parser.add_argument('frame_size', help="size of FIB frame in um. For example 51.2", type=float64)
    parser.add_argument('time_in_point', default=4000, help="time for FIB staying in one point, integer", type=int)
    parser.add_argument('-v', '--verbose', default=False, help="enable debug messages", type=bool)


    args = parser.parse_args()

    #  load parsed arguments to config
    config = Config()

    config.gds_file = args.gds_file
    config.direction = args.direction
    config.frame_size = args.frame_size
    config.time_in_point = args.time_in_point
    config.verbose = args.verbose
    config.frame_points = 4096
    config.output_path = f'output/processed_{datetime.today().strftime("%A_%d_%B_%Y__%I_%M_%S")}'

    logging.basicConfig(filename='main.log', level=logging.DEBUG)
    log = logging.getLogger(__name__)
    log.info('Started with parameters:')
    for k, v in config.__dict__.items():
        log.info(f'\t{k}\t{v}')

    # parse GDSII and extract polygons
    print(f'parsing {config.gds_file}')
    gds_parser = GDSParser(config.gds_file)
    gds_parser.parse()
    polygons = gds_parser.objects
    print(f'polygons extracted: {len(polygons)}')
    print('done')
    print()


    print('extracting boundary')
    x_max, x_min, y_max, y_min = get_boundary(polygons)
    boundary = Boundary()
    boundary.set_boundary(x_min, x_max, y_min, y_max)
    print(boundary)
    print('done')
    print()


    # generate frames of defied size
    print('creating frames...')
    frames = create_frames(
        boundary.xmax,
        boundary.xmin,
        boundary.ymax,
        boundary.ymin,
        config.frame_size
    )
    # plot frames
    config.multiply = 2
    plotter = Plotter(ceil(x_max - x_min), ceil(y_max - y_min))
    plotter.plot(
        polygons=polygons,
        frames=frames,
        d_x=x_min,
        d_y=y_min,
        output_path=os.path.join(config.output_path, 'figure.png')
    )

    print(f'frames created: {len(frames)}')
    print('done')
    print()

    print('mapping polygons to frames...')
    map_fp = map_frame_polygons(frames, polygons)
    print(f'frames with polygons: {len(map_fp)}')
    print('done')
    print()
    i = 1
    print('processing')
    # calculate step
    config.fib_step = config.frame_size / config.frame_points
    # calculate multiplier
    config.multiply = config.frame_points / config.frame_size * 2
    for f, polys in map_fp.items():
        print('-------------------------------')
        print(f'processing {i} of {len(map_fp)} frame\n{f}')
        filler = PointsFiller(f, polys)
        filler.fill()
        print('printing...')
        filler.print_points()
        print('plotting...')
        filler.plot()
        print('done')

        i += 1

print('\n==============================================')
print('GDS file processing done')


