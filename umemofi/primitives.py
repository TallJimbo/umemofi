class SkyRegion:

    @staticmethod
    def from_polygon(vertices):
        raise NotImplementedError()

    def __init__(self, ranges):
        self.ranges = ranges

    def overlaps(self, other):
        raise NotImplementedError()

    def __or__(self, other):
        raise NotImplementedError()

    def __and__(self, other):
        raise NotImplementedError()


class Span(tuple):
    # Needs to be native C++

    def __new__(cls, y, x0, x1):
        return tuple.__new__(cls, (int(y), int(x0), int(x1)))

    @property
    def y(self):
        return self[0]

    @property
    def x0(self):
        return self[1]

    @property
    def x1(self):
        return self[2]


class SpanSet(tuple):
    # Needs to be native C++

    def __new__(cls, spans):
        return tuple.__new__(cls, spans)

    @property
    def bbox(self):
        raise NotImplementedError()

    def overlaps(self, other):
        raise NotImplementedError()

    def __or__(self, other):
        raise NotImplementedError()

    def __and__(self, other):
        raise NotImplementedError()


class Image:
    # Might need to be native C++ (could pass NumPy array and xy0 separately)

    def __init__(self, array, x0=0, y0=0):
        self.array = array
        self.x0 = x0
        self.y0 = y0


class AffineTransform:
    # Definitely should be native C++

    def __init__(self, xx, xy, yx, yy, x0, y0):
        self.xx = float(xx)
        self.xy = float(xy)
        self.yx = float(yx)
        self.yy = float(yy)
        self.x0 = float(x0)
        self.y0 = float(y0)


class SED:
    # Maybe native C++ (could pass arrays and wavelength ranges separately)

    def __init__(self, array, lambda0, lambda1):
        self.array = array
        self.lambda0 = lambda0
        self.lambda1 = lambda1
