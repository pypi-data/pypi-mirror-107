"""Store and manipulate cartesian coordinates easier"""
import math


class Coord:
    """Store and manipulate two dimentional cartesian points"""
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def set(self, x: float = None, y: float = None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

    @property
    def r(self):
        """gives r for x and y translated into polar coords"""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @r.setter
    def r(self, r):
        self.set(*Coord.from_polar(r, self.theta))

    @property
    def theta(self):
        """gives theta for x and y translated into polar coords"""
        return math.atan2(self.y, self.x)

    @theta.setter
    def theta(self, theta):
        self.set(*Coord.from_polar(self.r, theta))

    @staticmethod
    def from_tuple(c):
        """Convert a tuple of length two into a coordinate"""
        return Coord(*c)

    @staticmethod
    def from_polar(r, theta):
        """
        convert polar coordinates to cartesian
        :r: the radius of the coordinate
        :theta: the angle of the coordinate
        :returns: a Coord instance with x and y values derived from r and theta
        """
        return Coord(r * math.cos(theta), r * math.sin(theta))

    def to_tuple(self) -> (float, float):
        """Return a tuple of the values stored in the coordinate"""
        return tuple(self)

    def to_polar(self) -> (float, float):
        return self.r, self.theta

    def convert_tuple(func): #decorator
        """
        A decorator that converts the first argument after self into a Coord object from a tuple
        """
        def wrapper(self, c, *args, **kwargs):
            if type(c) is tuple and len(c) == 2:
                c = Coord.from_tuple(c)
            return func(self, c, *args, **kwargs)
        return wrapper

    def scalar_multiply(self, k: float) -> 'Coord':
        """Multiply both the x and y coordinate by a scalar"""
        t = type(k)
        if t is not int and t is not float:
            raise TypeError(f'k has to be a scalar (type float or int) not {t}')
        return Coord(k * self.x, k * self.y)
    scalar_mul = scalar_multiply
    scal_mul = scalar_mul

    @convert_tuple
    def dot_product(self, c) -> float:
        """Take the dot product of two coordinates"""
        return self.x * c.x + self.y * c.y
    dot_prod = dot_product
    dot = dot_prod

    @convert_tuple
    def distance_between(self, c) -> float:
        """Find the distance between two Coords"""
        return math.sqrt((c.x - self.x) ** 2 + (c.y - self.y) ** 2)
    distance = distance_between
    dist = distance

    @convert_tuple
    def almost_equal(self, c, precision: int = 8) -> bool:
        r = abs(round(self - c, precision))
        return r.x == r.y == 0
    almost_eq = almost_equal

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self) -> str:
        return f'Coord(x={self.x:.3f}, y={self.y:.3f})'

    def __neg__(self) -> 'Coord':
        return Coord(-self.x, -self.y)

    def __abs__(self) -> 'Coord':
        return Coord(abs(self.x), abs(self.y))

    def __round__(self, places: int = 8) -> 'Coord':
        return Coord(round(self.x, places), round(self.y, places))

    def __floor__(self) -> 'Coord':
        return Coord(math.floor(self.x), math.floor(self.y))

    def __ceil__(self) -> 'Coord':
        return Coord(math.ceil(self.x), math.ceil(self.y))

    @convert_tuple
    def __eq__(self, c) -> bool:
        if type(c) is not Coord:
            raise ValueError(f'Cannot compare {type(c)} with Coord')
        return self.x == c.x and self.y == c.y

    @convert_tuple
    def __add__(self, c) -> 'Coord':
        if type(c) is not Coord:
            raise ValueError(f'Cannot add {type(c)} with Coord')
        return Coord(self.x + c.x, self.y + c.y)

    def __radd__(self, c) -> 'Coord':
        return self.__add__(c)

    @convert_tuple
    def __sub__(self, c) -> 'Coord':
        if type(c) is not Coord:
            raise ValueError(f'Cannot subtract {type(c)} with Coord')
        return Coord(self.x - c.x, self.y - c.y)

    def __rsub__(self, c) -> 'Coord':
        return -self + c

    @convert_tuple
    def __mul__(self, c) -> 'Coord' or float:
        t = type(c)
        if t is Coord:
            return self.dot_product(c)
        elif t is int or t is float:
            return self.scalar_multiply(c)
        else:
            raise ValueError('Can only multiply by tuple, int, float, and Coord')

    def __rmul__(self, c) -> 'Coord' or float:
        return self.__mul__(c)
