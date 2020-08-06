from amble.numberlists.color import Color
from amble.numberlists.rotation3d import Rotation3D
from amble.numberlists.vector3d import Vector3D
from amble.scriptobject import ScriptObject


class Sky(ScriptObject):
    classname = 'Sky'

    local_dir = '~/data/skies_pq'

    defaults = dict(
        position=Vector3D(336, 136, 0),
        rotation=Rotation3D.identity,
        scale=Vector3D.one,
        visibleDistance=500,
        useSkyTextures=1,
        renderBottomTexture=1,
        skySolidColor=Color(0.6, 0.6, 0.6, 1),
        materialList='~/data/skies_pq/Blender1/blender1.dml',
        windVelocity=Vector3D.i,
        windEffectPrecipitation=0,
        noRenderBans=1,
    )

    @classmethod
    def local(cls, materialList, **fields):
        return cls(materialList='{}/{}'.format(cls.local_dir, materialList), **fields)


Sky.blender1 = Sky.local('Blender1/blender1.dml')
Sky.blender2 = Sky.local('Blender2/blender2.dml')
Sky.blender3 = Sky.local('Blender3/blender3.dml')
Sky.blender4 = Sky.local('Blender4/blender4.dml')
Sky.cloudy = Sky.local('Cloudy/cloudy.dml')
Sky.wave = Sky.local('Wave/wave.dml')
