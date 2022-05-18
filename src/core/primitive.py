from abc import abstractmethod, ABCMeta

class Primitive(metaclass=ABCMeta):
    """Abstract class for geometrical figures
    """

    @abstractmethod
    def to_plot(self):
        raise Exception('Not implemeted')