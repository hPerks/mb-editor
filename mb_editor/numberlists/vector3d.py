from mb_editor.numberlists.numberlist import NumberList


class Vector3D(NumberList):

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
    def z(self):
        return self[2]

    @z.setter
    def z(self, value):
        self[2] = value

    def dot(self, other):
        other = Vector3D(other)
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        other = Vector3D(other)
        return self.__class__(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def tangent(self):
        if abs(self.x) < 0.01 and abs(self.y) < 0.01:
            return Vector3D.j.cross(self).normalized()
        else:
            return Vector3D.k.cross(self).normalized()

    def cotangent(self):
        return self.tangent().cross(self).normalized()


    @staticmethod
    def tests():
        v = Vector3D('3 1 4')

        v.x = 2
        v.z = v.y * v.x
        assert v == '2 1 2'

        assert abs(v) == 3
        assert v.normalized() == (2/3, 1/3, 2/3)
        assert v.dot('-1 2 0') == 0
        assert v.cross('-1 2 0') == '-4 -2 5'
        assert v.tangent() == Vector3D(-1, 2, 0).normalized()
        assert v.dot(v.tangent()) == 0 and v.dot(v.cotangent()) == 0


Vector3D.none = Vector3D()

Vector3D.i = Vector3D(1, 0, 0)
Vector3D.j = Vector3D(0, 1, 0)
Vector3D.k = Vector3D(0, 0, 1)

Vector3D.zero = Vector3D(0, 0, 0)
Vector3D.one = Vector3D(1, 1, 1)


if __name__ == '__main__':
    Vector3D.tests()
