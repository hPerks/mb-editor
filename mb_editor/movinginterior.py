from mb_editor.numberlists.rotation3d import Rotation3D
from mb_editor.numberlists.vector3d import Vector3D
from mb_editor.simgroup import SimGroup
from mb_editor.physicalobject import PhysicalObject
from mb_editor.path import Marker, Path


class PathedInterior(PhysicalObject):
    classname = "PathedInterior"

    local_dir = "platinum/data/interiors"

    defaults = dict(
        datablock="PathedDefault",
        interiorResource="",
        interiorIndex=0,
        initialTargetPosition=-1,

        basePosition=Vector3D.zero,
        baseRotation=Rotation3D.identity,
        baseScale=Vector3D.one,
    )

    @classmethod
    def local(cls, interiorResource, interiorIndex, **fields):
        return cls(
            interiorResource="{}/{}".format(cls.local_dir, interiorResource),
            interiorIndex=interiorIndex,
            **fields
        )


class MovingInterior(SimGroup):

    @classmethod
    def make(cls, pathedInterior, *args, **fields):
        markers = filter(lambda a: isinstance(a, Marker), args)
        others = filter(lambda a: not isinstance(a, Marker), args)

        return cls(
            pathedInterior,
            Path(*markers),
            *others,
            **fields
        )


if __name__ == '__main__':
    print(MovingInterior.make(
        PathedInterior.local("foundationRepair.dif", 0, basePosition="4 2 0"),
        Marker(position="0 0 0", msToNext=1000),
        Marker(position="3 1 4", msToNext=1000),
        Marker(position="0 0 0")
    ))

    print(MovingInterior.make(
        PathedInterior.local("foundationRepair.dif", 0, basePosition="4 2 0"),
        *Marker().copies(
            ("position", "msToNext"),
            "0 0 0", 1000,
            "3 1 4", 1000,
            "0 0 0"
        )
    ))

    print(MovingInterior.make(
        PathedInterior.local("foundationRepair.dif", 0, basePosition="4 2 0"),
        Path.make_linear(
            "0 0 0", 1000,
            "3 1 4", 1000,
            "0 0 0"
        )
    ))
