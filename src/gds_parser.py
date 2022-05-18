import gdspy
import magic

from core.config import Config
from core.fabric import Fabric

config = Config()


class GDSParser():

    def __init__(self, gds_file):
        if 'GDSII Stream file' not in magic.from_file(gds_file):
            raise Exception(f'{gds_file} is not GDSII file by magic')

        self._file = gds_file

        self._objects = []

    def parse(self):
        gdsii = gdspy.GdsLibrary(infile=self._file)

        config.precision = gdsii.precision
        config.unit = gdsii.unit

        for cell, body in gdsii.cells.items():
            for polygon in body.polygons:
                self._objects.append(Fabric.create_from_points(points=polygon.polygons[0]))

    @property
    def objects(self):
        return self._objects


if __name__ == '__main__':
    parser = GDSParser('files/DC_375.gds')
    assert parser, 'problem accured'

    parser.parse()
    assert len(parser.objects) == 4, 'not 4 polygons'
