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


class BoundedObject(PhysicalObject):
    defaults = dict(
        polyhedron=Polyhedron3D.identity
    )


if __name__ == '__main__':
    b = BoundedObject()
    assert b.position.x == 0
    assert b.polyhedron.i == "1 0 0"

    print(b)
