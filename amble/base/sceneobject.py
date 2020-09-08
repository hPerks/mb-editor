from operator import mul

from amble.base.fields import Implicit
from amble.base.id import ID
from amble.base.scriptobject import ScriptObject
from amble.numberlists import Rotation3D, Vector3D


class SceneObject(ScriptObject):
    defaults = dict(
        position=Vector3D.zero,
        rotation=Rotation3D.identity,
        scale=Vector3D.one,
        path=Implicit(ID.none),
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
        cc = SceneObject().copies(
            ('position.x', 'position.y'),
            1, 3,
            3, 7,
        )
        assert len(cc) == 2
        assert cc[0].position == '1 3'


if __name__ == '__main__':
    SceneObject.tests()

__all__ = ['SceneObject']
