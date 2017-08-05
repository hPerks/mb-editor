from .numberlist import NumberList


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

Vector3D.i = Vector3D(1, 0, 0)
Vector3D.j = Vector3D(0, 1, 0)
Vector3D.k = Vector3D(0, 0, 1)

Vector3D.zero = Vector3D(0, 0, 0)
Vector3D.one = Vector3D(1, 1, 1)