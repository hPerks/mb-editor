from math import sin, cos, atan2, radians, degrees

from amble.numberlists.numberlist import NumberList
from amble.numberlists.vector3d import Vector3D
from amble.utils.numbers import str_float


class Rotation3D(Vector3D):

    def __init__(self, *args):
        super().__init__(*args)

        self.axis = self.axis.normalized()

    @property
    def axis(self):
        return Vector3D(self[0:3])

    @axis.setter
    def axis(self, value):
        self[0:3] = Vector3D(value).normalized()

    @property
    def angle(self):
        return self[3]

    @angle.setter
    def angle(self, value):
        self[3] = value

    class Quaternion(NumberList):
        def __mul__(self, other):
            return self.__class__(
                self[0] * other[0] - self[1] * other[1] - self[2] * other[2] - self[3] * other[3],
                self[0] * other[1] + self[1] * other[0] + self[2] * other[3] - self[3] * other[2],
                self[0] * other[2] - self[1] * other[3] + self[2] * other[0] + self[3] * other[1],
                self[0] * other[3] + self[1] * other[2] - self[2] * other[1] + self[3] * other[0]
            )

        def conjugate(self):
            return self.__class__(self[0], -self[1], -self[2], -self[3])

    def to_quaternion(self):
        cosine, sine = cos(radians(self.angle) / 2), sin(radians(self.angle) / 2)
        return Rotation3D.Quaternion(cosine, self.x * sine, self.y * sine, self.z * sine)

    @classmethod
    def from_quaternion(cls, q):
        cosine, sine = q[0], abs(Vector3D(q[1:4]))
        if sine == 0:
            return cls('1 0 0 0')

        return cls(q[1] / sine, q[2] / sine, q[3] / sine, 2 * degrees(atan2(sine, cosine)))

    def __eq__(self, other):
        return super().__eq__(other) or self.to_quaternion() == other.to_quaternion()

    def __add__(self, other):
        return self.__class__.from_quaternion(self.to_quaternion() * self.__class__(other).to_quaternion())

    def __sub__(self, other):
        return self + (other * -1)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.__class__(self.x, self.y, self.z, self.angle * other)

        return Vector3D((
            self.to_quaternion().conjugate() *
            Rotation3D.Quaternion(0, *Vector3D(other).values) *
            self.to_quaternion()
        )[1:4])

    def __truediv__(self, other):
        return self * (1 / other)

    def __neg__(self):
        return self * -1


    @staticmethod
    def tests():
        r = Rotation3D(*(Vector3D.i * 2), 90)
        s = Rotation3D(*Vector3D.j, 180)

        assert r.axis == Vector3D.i
        s.angle = s.angle - 90
        assert s.angle == 90

        p = r + str(s)
        assert abs(p.axis - Vector3D.one.normalized()) < 0.01
        assert abs(p.angle - 120) < 0.01

        r.angle = 30
        assert str_float((r * s.axis).z) == '-0.5'


    @staticmethod
    def i(angle):
        return Rotation3D(1, 0, 0, angle)

    @staticmethod
    def j(angle):
        return Rotation3D(0, 1, 0, angle)

    @staticmethod
    def k(angle):
        return Rotation3D(0, 0, 1, angle)


    none, identity, up, down, right, left, towards, away = tuple(range(8))


Rotation3D.none = Rotation3D()

Rotation3D.identity = Rotation3D(1, 0, 0, 0)
Rotation3D.up = Rotation3D(1, 0, 0, 0)
Rotation3D.down = Rotation3D(1, 0, 0, 180)
Rotation3D.right = Rotation3D(0, -1, 0, 90)
Rotation3D.left = Rotation3D(0, 1, 0, 90)
Rotation3D.towards = Rotation3D(-1, 0, 0, 90)
Rotation3D.away = Rotation3D(1, 0, 0, 90)


if __name__ == '__main__':
    Rotation3D.tests()

__all__ = ['Rotation3D']
