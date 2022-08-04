import itertools
from PIL import Image, ImageDraw, ImageFont


class Plotter():
    def __init__(self, x_size, y_size):
        self._x_size = x_size
        self._y_size = y_size
        
        self._frame = None

        self._img = Image.new( 'RGB', (self._x_size, self._y_size), "white")
        self._d = ImageDraw.Draw(self._img)
        
    def set_frame(self, frame):
        self._frame = frame

    def plot(self, polygons=[], points=[], frames=[], d_x=0, d_y=0, output_path='plotted.png'):
        for figure in itertools.chain(polygons, points, frames):
            if self._frame:
                to_plot = [p for p in figure.to_plot(d_x, d_y, self._frame)]
            else:
                to_plot = [p for p in figure.to_plot(d_x, d_y)]

            if figure.__class__.__name__ == 'Frame':
                self._d.polygon(to_plot, width=1, outline=(127,0,0))
            elif figure.__class__.__name__ == 'Polygon':
                # continue
                self._d.polygon(to_plot, width=1, outline=(0, 0, 127))
            elif figure.__class__.__name__ == 'Point':
                self._d.point(to_plot, fill=(0, 127, 0))

        self._img = self._img.transpose(method=Image.FLIP_TOP_BOTTOM)
        self._img.save(output_path)
