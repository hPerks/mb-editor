import amble
from amble.numberlists import Color, Rotation3D, Vector3D


class Sky(amble.ScriptObject):
    classname = 'Sky'

    local_dir = '~/data/skies_pq'

    defaults = dict(
        position=Vector3D(336, 136, 0),
        rotation=Rotation3D.identity,
        scale=Vector3D.one,
        visibledistance=500,
        useskytextures=1,
        renderbottomtexture=1,
        skysolidcolor=Color(0.6, 0.6, 0.6, 1),
        materiallist='~/data/skies_pq/Blender1/blender1.dml',
        windvelocity=Vector3D.i,
        windeffectprecipitation=0,
        norenderbans=1,
    )

    @classmethod
    def local(cls, materiallist, **fields):
        return cls(materiallist=f'{cls.local_dir}/{materiallist}', **fields)

    blender1, blender2, blender3, blender4, cloudy, wave = tuple(range(6))


Sky.blender1 = Sky.local('Blender1/blender1.dml')
Sky.blender2 = Sky.local('Blender2/blender2.dml')
Sky.blender3 = Sky.local('Blender3/blender3.dml')
Sky.blender4 = Sky.local('Blender4/blender4.dml')
Sky.cloudy = Sky.local('Cloudy/cloudy.dml')
Sky.wave = Sky.local('Wave/wave.dml')

__all__ = ['Sky']
