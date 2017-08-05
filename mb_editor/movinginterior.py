from mb_editor.numberlists.rotation3d import Rotation3D
from mb_editor.numberlists.vector3d import Vector3D
from mb_editor.simgroup import SimGroup
from mb_editor.physicalobject import PhysicalObject


class Marker(PhysicalObject):
    classname = "Marker"

    defaults = dict(
        seqNum=0,
        msToNext=0,
        smoothingType="Linear"
    )


class Path(SimGroup):
    classname = "Path"


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
    def local(cls, interiorResource, **fields):
        return cls(interiorResource="{}/{}".format(cls.local_dir, interiorResource), **fields)


class MovingInterior(SimGroup):

    @classmethod
    def make(cls, pathedInterior, *markers, **fields):
        return cls(
            pathedInterior,
            Path(*(marker.set(seqNum=seqNum) for seqNum, marker in enumerate(markers))),
            **fields
        )


if __name__ == '__main__':
    print(MovingInterior.make(
        PathedInterior.local("foundationRepair.dif", basePosition="4 2 0"),
        Marker(position="0 0 0", msToNext=1000),
        Marker(position="3 1 4", msToNext=1000),
    ))