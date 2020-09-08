from amble.numberlists.numberlist import NumberList
from amble.numberlists.vector3d import Vector3D


class Polyhedron3D(NumberList):

    @classmethod
    def make(cls, o=Vector3D.zero, i=Vector3D.i, j=Vector3D.j, k=Vector3D.k):
        instance = cls(*([0] * 12))
        instance.o, instance.i, instance.j, instance.k = o, i, j, k
        return instance

    @property
    def o(self):
        return Vector3D(self[0:3])

    @o.setter
    def o(self, value):
        self[0:3] = Vector3D(value)

    @property
    def i(self):
        return Vector3D(self[3:6])

    @i.setter
    def i(self, value):
        self[3:6] = Vector3D(value)

    @property
    def j(self):
        return Vector3D(self[6:9])

    @j.setter
    def j(self, value):
        self[6:9] = Vector3D(value)

    @property
    def k(self):
        return Vector3D(self[9:12])

    @k.setter
    def k(self, value):
        self[9:12] = Vector3D(value)

    def with_offset_faces(self, right=0, left=0, front=0, back=0, top=0, bottom=0):
        return Polyhedron3D.make(
            o=self.o + (left, back, bottom),
            i=self.i + (right-left, 0, 0),
            j=self.j + (0, front-back, 0),
            k=self.k + (0, 0, top-bottom),
        )


    @staticmethod
    def tests():
        p = Polyhedron3D.make('0 0 0', '1 1 0', '0 1 0', '0 0 1')
        assert p == '0 0 0 1 1 0 0 1 0 0 0 1'

        p.i = Vector3D.i
        p.k += p.j
        assert p == '0 0 0 1 0 0 0 1 0 0 1 1'

        q = p.with_offset_faces(right=1, left=-1, bottom=-1)
        assert q == '-1 0 -1 3 0 0 0 1 0 0 1 2'


    identity = None


Polyhedron3D.identity = Polyhedron3D.make()


if __name__ == '__main__':
    Polyhedron3D.tests()

__all__ = ['Polyhedron3D']
