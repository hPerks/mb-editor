from operator import mul

from mb_editor.numberlists.polyhedron3d import Polyhedron3D
from mb_editor.numberlists.rotation3d import Rotation3D
from mb_editor.numberlists.vector3d import Vector3D

from mb_editor.scriptobject import ScriptObject
from mb_editor.implicit import Implicit
from mb_editor.objectname import ObjectName


class PhysicalObject(ScriptObject):
    defaults = dict(
        position=Vector3D.zero,
        rotation=Rotation3D.identity,
        scale=Vector3D.one,
        path=Implicit(ObjectName.none)
    )

    def __add__(self, other):
        return self.copy(
            position=self.position + other.position,
            rotation=self.rotation + other.rotation,
            scale=self.scale.map(mul, other.scale),
        )

    def __sub__(self, other):
        return self + (other * -1)

    def __mul__(self, other):
        return self.copy(
            position=self.position * other,
            rotation=self.rotation * other,
            scale=pow(self.scale, other),
        )

    def __truediv__(self, other):
        return self * (1 / other)



    @staticmethod
    def tests():
        cc = PhysicalObject().copies(
            ("position.x", "position.y"),
            1, 3,
            3, 7,
        )
        assert len(cc) == 2
        assert cc[0].position == "1 3"


class BoundedObject(PhysicalObject):
    defaults = dict(
        polyhedron=Polyhedron3D.identity
    )


if __name__ == '__main__':
    PhysicalObject.tests()
