from mb_editor.simgroup import SimGroup
from mb_editor.physicalobject import PhysicalObject
from mb_editor.utils.lists import flatlist


class Marker(PhysicalObject):
    classname = "Marker"

    defaults = dict(
        seqNum=0,
        msToNext=0,
        smoothingType="Linear"
    )


class Path(SimGroup):
    classname = "Path"

    def __init__(self, *markers, **fields):
        super().__init__([marker.set(seqNum=seqNum) for seqNum, marker in enumerate(flatlist(*markers))], **fields)

    @property
    def markers(self):
        return self.children

    @classmethod
    def make(cls, *args, **fields):
        return cls(
            Marker(**fields).copies(
                ("position", "msToNext", "smoothingType"),
                *args
            )
        )

    @classmethod
    def make_linear(cls, *args, **fields):
        return cls(
            Marker(smoothingType="Linear", **fields).copies(
                ("position", "msToNext"),
                *args
            )
        )

    @classmethod
    def make_accelerate(cls, *args, **fields):
        return cls(
            Marker(smoothingType="Accelerate", **fields).copies(
                ("position", "msToNext"),
                *args
            )
        )


    @staticmethod
    def tests():
        p = Path.make_accelerate(
            "0 0 0", "1000",
            "0 0 4", "1000",
            "0 0 0"
        )

        assert len(p.markers) == 3
        assert p.markers[2].seqNum == 2

if __name__ == '__main__':
    Path.tests()
