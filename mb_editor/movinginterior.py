from mb_editor.numberlists.rotation3d import Rotation3D
from mb_editor.numberlists.vector3d import Vector3D
from mb_editor.simgroup import SimGroup
from mb_editor.sceneobject import SceneObject
from mb_editor.path import Marker, Path
from mb_editor.utils import path


class PathedInterior(SceneObject):
    classname = 'PathedInterior'

    defaults = dict(
        datablock='PathedDefault',
        interiorResource='',
        interiorIndex=0,
        initialTargetPosition=-1,

        basePosition=Vector3D.zero,
        baseRotation=Rotation3D.identity,
        baseScale=Vector3D.one,
    )

    @classmethod
    def local(cls, interiorResource, interiorIndex, **fields):
        return cls(
            interiorResource=path.join('platinum/data/interiors_pq/custom', interiorResource),
            interiorIndex=interiorIndex,
            **fields
        )


class MovingInterior(SimGroup):

    defaults = dict(
        interior=PathedInterior(),
        path=Path()
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
    def make(cls, pathedInterior, *args, **fields):
        if len(args) > 0 and isinstance(args[0], Path):
            path = args[0]
            other_children = args[1:]
        else:
            path = Path(*list(filter(lambda a: isinstance(a, Marker), args)))
            other_children = filter(lambda a: not isinstance(a, Marker), args)

        return cls(interior=pathedInterior, path=path, **fields).add(*other_children)


    @staticmethod
    def tests():
        from mb_editor.scriptobject import ScriptObject
        h = MovingInterior.make(
            PathedInterior.local('foundationRepair.dif', 0, basePosition='4 2 0'),
            Marker(position='0 0 0', msToNext=1000),
            Marker(position='0 0 4', msToNext=1000),
            Marker(position='0 0 0'),
            ScriptObject('Information', interiorName='TheHouse', animation='lifting')
        )

        assert h.interior.basePosition == [4, 2, 0]
        assert len(h.markers) == 3
        assert len(h.other_children) == 1
        assert h.other_children[0].animation == 'lifting'

        b = MovingInterior.make(
            PathedInterior.local('foundationRepair.dif', 1, basePosition='0 0 0'),
            Path.make_accelerate(
                '0 0 0', '5000',
                '0 40 -2'
            ),
            ScriptObject('Information', interiorName='Ball', animation='rolling')
        )

        assert b.interior.interiorResource == h.interior.interiorResource
        assert b.markers[0].position.z > b.markers[1].position.z
        assert b.other_children[0].animation == 'rolling'

        b.path = Path.make_accelerate('0 0 0', '2000', '0 40 -2')
        assert b.markers[0].msToNext == 2000

        b.add(Path.make_accelerate('0 0 0', '8000', '0 40 -2'))
        assert b.markers[0].msToNext == 8000


if __name__ == '__main__':
    MovingInterior.tests()
