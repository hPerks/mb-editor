from mb_editor.numberlists.numberlist import NumberList
from mb_editor.numberlists.vector3d import Vector3D


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


    @staticmethod
    def tests():
        p = Polyhedron3D.make("0 0 0", "1 1 0", "0 1 0", "0 0 1")
        assert p == "0 0 0 1 1 0 0 1 0 0 0 1"

        p.i = Vector3D.i
        p.k += p.j
        assert p == "0 0 0 1 0 0 0 1 0 0 1 1"

Polyhedron3D.identity = Polyhedron3D.make()

if __name__ == '__main__':
    Polyhedron3D.tests()
