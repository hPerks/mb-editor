from amble.simgroup import SimGroup
from amble.sceneobject import SceneObject
from amble.utils.lists import flatlist


class Marker(SceneObject):
    classname = 'Marker'

    defaults = dict(
        seqNum=0,
        msToNext=0,
        smoothingType='Linear'
    )


class Path(SimGroup):
    classname = 'Path'

    def __init__(self, *markers, **fields):
        super().__init__([marker.copy(seqNum=seqNum) for seqNum, marker in enumerate(flatlist(*markers))], **fields)

    @property
    def markers(self):
        return self.children

    @classmethod
    def make(cls, *args, **fields):
        return cls(
            Marker(**fields).copies(
                ('position', 'msToNext', 'smoothingType'),
                *args
            )
        )

    @classmethod
    def make_linear(cls, *args, **fields):
        return cls(
            Marker(smoothingType='Linear', **fields).copies(
                ('position', 'msToNext'),
                *args
            )
        )

    @classmethod
    def make_accelerate(cls, *args, **fields):
        return cls(
            Marker(smoothingType='Accelerate', **fields).copies(
                ('position', 'msToNext'),
                *args
            )
        )

    def start_at_index(self, index, loop=True):
        if loop:
            return Path(self.markers[index:-1] + self.markers[:index] + [self.markers[index]])
        else:
            return Path(self.markers[index:])


    @staticmethod
    def tests():
        p = Path.make_accelerate(
            '0 0 0', '1000',
            '0 0 4', '200',
            '0 0 6', '200',
            '0 0 4', '1000',
            '0 0 0'
        )

        assert len(p.markers) == 5
        assert p.markers[2].seqNum == 2

        q = p.start_at_index(2)
        assert len(q.markers) == 5
        assert q.markers[2].position == '0 0 0'
        assert q.markers[2].seqNum == 2

if __name__ == '__main__':
    Path.tests()
