import amble
from amble.interior.moving.marker import Marker
from amble.interior.moving.path import Path
from amble.interior.moving.pathedinterior import PathedInterior


class MovingInterior(amble.SimGroup):
    defaults = dict(
        interior=PathedInterior(),
        path=Path(),
    )

    @property
    def markers(self):
        return self.path.children

    @property
    def other_children(self):
        return list(filter(lambda child: child not in [self.interior, self.path], self.children))

    def path_add(self, *markers):
        self.path.add(*markers)
        return self

    def path_remove(self, *markers):
        self.path.remove(*markers)
        return self

    @classmethod
    def make(cls, pathedinterior, *args, **fields):
        if len(args) > 0 and isinstance(args[0], Path):
            path = args[0]
            other_children = args[1:]
        else:
            path = Path(*list(filter(lambda a: isinstance(a, Marker), args)))
            other_children = filter(lambda a: not isinstance(a, Marker), args)

        return cls(interior=pathedinterior, path=path, **fields).add(*other_children)


    @staticmethod
    def tests():
        h = MovingInterior.make(
            PathedInterior.local('foundationRepair.dif', 0, baseposition='4 2 0'),
            Marker(position='0 0 0', mstonext=1000),
            Marker(position='0 0 4', mstonext=1000),
            Marker(position='0 0 0'),
            amble.ScriptObject('Information', interiorname='TheHouse', animation='lifting')
        )

        assert h.interior.basePosition == [4, 2, 0]
        assert len(h.markers) == 3
        assert len(h.other_children) == 1
        assert h.other_children[0].animation == 'lifting'

        b = MovingInterior.make(
            PathedInterior.local('foundationRepair.dif', 1, baseposition='0 0 0'),
            Path.make_accelerate(
                '0 0 0', '5000',
                '0 40 -2'
            ),
            amble.ScriptObject('Information', interiorname='Ball', animation='rolling')
        )

        assert b.interior.interiorresource == h.interior.interiorresource
        assert b.markers[0].position.z > b.markers[1].position.z
        assert b.other_children[0].animation == 'rolling'

        b.path = Path.make_accelerate('0 0 0', '2000', '0 40 -2')
        assert b.markers[0].msToNext == 2000

        b.add(Path.make_accelerate('0 0 0', '8000', '0 40 -2'))
        assert b.markers[0].msToNext == 8000


if __name__ == '__main__':
    MovingInterior.tests()

__all__ = ['MovingInterior']
