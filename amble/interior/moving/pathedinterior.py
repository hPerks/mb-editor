import amble
from amble.numberlists import Rotation3D, Vector3D
from amble.utils import path


class PathedInterior(amble.SceneObject):
    classname = 'PathedInterior'

    defaults = dict(
        datablock='PathedDefault',
        interiorresource='',
        interiorindex=0,
        initialtargetposition=-1,

        baseposition=Vector3D.zero,
        baserotation=Rotation3D.identity,
        basescale=Vector3D.one,
    )

    @classmethod
    def local(cls, interiorresource, interiorindex, **fields):
        if not interiorresource.endswith('.dif'):
            interiorresource += '.dif'

        return cls(
            interiorresource=path.join('platinum/data/interiors_pq/custom', interiorresource),
            interiorindex=interiorindex,
            **fields
        )


__all__ = ['PathedInterior']
