from amble.numberlists import *
from amble.base.sceneobject import SceneObject


class BoundedObject(SceneObject):
    defaults = dict(polyhedron=Polyhedron3D.identity)


__all__ = ['BoundedObject']
