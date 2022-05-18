
from core.polygon import Polygon
from core.point import Point
from core.line import Line
from core.frame import create_frame
from core.plotter import Plotter
from core.config import Config

config = Config()

config.frame_size = 51.2
config.frame_points = 4096
config.multiply = config.frame_points / config.frame_size

polygons = [
    Polygon([
        Line(Point(15, 35), Point(35, 35)),
        Line(Point(35, 35), Point(35, 45)),
        Line(Point(35, 45), Point(15, 45)),
        Line(Point(15, 45), Point(15, 35)),
    ]),
    Polygon([
        Line(Point(15, 40), Point(35, 40)),
        Line(Point(35, 40), Point(35, 255)),
        Line(Point(35, 255), Point(75, 255)),
        Line(Point(75, 255), Point(15, 40)),
    ]),
]
frames = [
    create_frame(Point(0, 0), 51.2)
]

points = [
    Point(0.1, 0.1),
    Point(0.1125, 0.1),
    Point(0.125, 0.1),
    Point(0.1375, 0.1),
    Point(0.15, 0.1),
    Point(20, 40)
]

plotter = Plotter(4096, 4096)
plotter.plot(frames=frames, polygons=polygons, points=points, d_x=0, d_y=0)


# from PIL import Image, ImageDraw

# img = Image.new( 'RGB', (200, 200), "white")
# img.transpose(method=Image.FLIP_TOP_BOTTOM)
# d = ImageDraw.Draw(img)
# # d.polygon((1201, 2801, 2801, 2801, 2801, 3601, 1201, 3601), width=1, outline=(0, 0, 0))
# # d.rectangle((1, 1, 4097, 4097), width=1, outline=(127, 0, 0))
# d.point((100, 100), (0, 127, 0))
# d.point((101, 100), (0, 127, 0))
# d.point((102, 100), (0, 127, 0))
# d.point((103, 100), (0, 127, 0))
# d.point((104, 100), (0, 127, 0))
# d.point((105, 100), (0, 127, 0))

# img.transpose(method=Image.FLIP_TOP_BOTTOM)
# img.save('plotted.jpg')