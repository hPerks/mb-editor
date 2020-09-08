import math

from amble.numberlists.numberlist import NumberList


class Vector2D(NumberList):

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

    @property
    def angle(self):
        return math.degrees(math.atan2(self.y, self.x))

    def rotated(self, angle):
        return self.__class__(
            abs(self) * math.cos(math.radians(self.angle + angle)),
            abs(self) * math.sin(math.radians(self.angle + angle))
        )


    none, i, j, zero, one = tuple(range(5))


Vector2D.none = Vector2D()

Vector2D.i = Vector2D(1, 0)
Vector2D.j = Vector2D(0, 1)

Vector2D.zero = Vector2D(0, 0)
Vector2D.one = Vector2D(1, 1)

__all__ = ['Vector2D']
