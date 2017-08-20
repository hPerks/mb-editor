from mb_editor.numberlists.numberlist import NumberList
from mb_editor.numberlists.vector3d import Vector3D

from math import sin, cos, atan2, radians, degrees


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
            return Rotation3D.Quaternion(
                self[0] * other[0] - self[1] * other[1] - self[2] * other[2] - self[3] * other[3],
                self[0] * other[1] + self[1] * other[0] + self[2] * other[3] - self[3] * other[2],
                self[0] * other[2] - self[1] * other[3] + self[2] * other[0] + self[3] * other[1],
                self[0] * other[3] + self[1] * other[2] - self[2] * other[1] + self[3] * other[0]
            )

    def to_quaternion(self):
        cosine, sine = cos(radians(self.angle) / 2), sin(radians(self.angle) / 2)
        return Rotation3D.Quaternion(cosine, self.x * sine, self.y * sine, self.z * sine)

    @classmethod
    def from_quaternion(cls, q):
        cosine, sine = q[0], abs(Vector3D(q[1:4]))
        if sine == 0:
            return cls("1 0 0 0")

        return cls(q[1] / sine, q[2] / sine, q[3] / sine, 2 * degrees(atan2(sine, cosine)))


    def __eq__(self, other):
        return Vector3D.__eq__(self, other) or self.to_quaternion() == other.to_quaternion()

    def __add__(self, other):
        return self.__class__.from_quaternion(self.to_quaternion() * self.__class__(other).to_quaternion())

    def __sub__(self, other):
        return self + (other * -1)

    def __mul__(self, other):
        return self.__class__(self.x, self.y, self.z, self.angle * other)

    def __truediv__(self, other):
        return self * (1 / other)


    @staticmethod
    def tests():
        r = Rotation3D(*(Vector3D.i * 2), 90)
        s = Rotation3D(*Vector3D.j, 180)

        assert r.axis == Vector3D.i
        s.angle = s.angle - 90
        assert s.angle == 90

        p = r + repr(s)
        assert abs(p.axis - Vector3D.one.normalized()) < 0.01
        assert abs(p.angle - 120) < 0.01

Rotation3D.none = Rotation3D()

Rotation3D.identity = Rotation3D(1, 0, 0, 0)
Rotation3D.up = Rotation3D(1, 0, 0, 0)
Rotation3D.down = Rotation3D(1, 0, 0, 180)
Rotation3D.right = Rotation3D(0, -1, 0, 90)
Rotation3D.left = Rotation3D(0, 1, 0, 90)
Rotation3D.towards = Rotation3D(-1, 0, 0, 90)
Rotation3D.away = Rotation3D(1, 0, 0, 90)

Rotation3D.i = lambda angle: Rotation3D(1, 0, 0, angle)
Rotation3D.j = lambda angle: Rotation3D(0, 1, 0, angle)
Rotation3D.k = lambda angle: Rotation3D(0, 0, 1, angle)


if __name__ == '__main__':
    Rotation3D.tests()
