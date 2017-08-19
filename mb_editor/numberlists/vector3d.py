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

    def __abs__(self):
        return pow(sum(map(lambda i: i ** 2, self)), 0.5)

    def normalized(self):
        return self / abs(self)


    @staticmethod
    def tests():
        v = Vector3D("3 1 4")

        v.x = 2
        v.z = v.y * v.x
        assert v == "2 1 2"

        assert abs(v) == 3
        assert v.normalized() == (2/3, 1/3, 2/3)

Vector3D.none = Vector3D()

Vector3D.i = Vector3D(1, 0, 0)
Vector3D.j = Vector3D(0, 1, 0)
Vector3D.k = Vector3D(0, 0, 1)

Vector3D.zero = Vector3D(0, 0, 0)
Vector3D.one = Vector3D(1, 1, 1)


if __name__ == '__main__':
    Vector3D.tests()
