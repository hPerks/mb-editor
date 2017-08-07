from mb_editor.numberlists.polyhedron3d import Polyhedron3D
from mb_editor.numberlists.rotation3d import Rotation3D
from mb_editor.numberlists.vector3d import Vector3D
from mb_editor.scriptobject import ScriptObject


class PhysicalObject(ScriptObject):
    defaults = dict(
        position=Vector3D.zero,
        rotation=Rotation3D.identity,
        scale=Vector3D.one,
    )

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
