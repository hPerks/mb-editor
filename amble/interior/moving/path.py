import amble
from amble.interior.moving.marker import Marker
from amble.utils.lists import flatlist


class Path(amble.SimGroup):
    classname = 'Path'

    def __init__(self, *markers, **fields):
        super().__init__([marker.copy(seqnum=seqnum) for seqnum, marker in enumerate(flatlist(*markers))], **fields)

    @property
    def markers(self):
        return self.children

    @classmethod
    def make(cls, *args, **fields):
        return cls(
            Marker(**fields).copies(
                ('position', 'mstonext', 'smoothingtype'),
                *args
            )
        )

    @classmethod
    def make_linear(cls, *args, **fields):
        return cls(
            Marker(smoothingtype='Linear', **fields).copies(
                ('position', 'mstonext'),
                *args
            )
        )

    @classmethod
    def make_accelerate(cls, *args, **fields):
        return cls(
            Marker(smoothingtype='Accelerate', **fields).copies(
                ('position', 'mstonext'),
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

__all__ = ['Path']
