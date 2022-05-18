class Boundary():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Boundary, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__xmin = None
        self.__xmax = None
        self.__ymin = None
        self.__ymax = None

    def __str__(self):
        return f'xmin -> {self.__xmin}\n\txmax -> {self.__xmax}\n\tymin -> {self.__ymin}\n\tymax -> {self.__ymax}\n'

    def set_boundary(self, xmin, xmax, ymin, ymax):
        self.__xmin = xmin
        self.__xmax = xmax
        self.__ymin = ymin
        self.__ymax = ymax

    def adjust_boundary(self, frames):
        for frame in frames:
            if frame.origin.x < self.__xmin:
                self.__xmin = frame.origin.x
            if frame.origin.y < self.__ymin:
                self.__ymin = frame.origin.y
            if frame.foreign.x < self.__xmax:
                self.__xmax = frame.foreign.x
            if frame.foreign.y < self.__ymax:
                self.__ymax = frame.foreign.y

    @property
    def xmin(self):
        return self.__xmin

    @property
    def xmax(self):
        return self.__xmax

    @property
    def ymin(self):
        return self.__ymin

    @property
    def ymax(self):
        return self.__ymax