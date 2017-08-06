from mb_editor.numberlists.color import Color
from mb_editor.numberlists.rotation3d import Rotation3D
from mb_editor.numberlists.vector3d import Vector3D
from mb_editor.scriptobject import ScriptObject


class Sky(ScriptObject):
    classname = "Sky"

    local_dir = "~/data/skies_pq"

    defaults = dict(
        position=Vector3D(336, 136, 0),
        rotation=Rotation3D.identity,
        scale=Vector3D.one,
        visibleDistance=500,
        useSkyTextures=1,
        renderBottomTexture=1,
        skySolidColor=Color(0.6, 0.6, 0.6, 1),
        materialList="~/data/skies_pq/blender1.dml",
        windVelocity=Vector3D.i,
        windEffectPrecipitation=0,
        noRenderBans=1,
    )

    @classmethod
    def local(cls, materialList, **fields):
        return cls(materialList="{}/{}".format(cls.local_dir, materialList), **fields)

Sky.blender1 = Sky.local("blender1.dml")
Sky.blender2 = Sky.local("blender2.dml")
Sky.blender3 = Sky.local("blender3.dml")
Sky.blender4 = Sky.local("blender4.dml")
Sky.cloudy = Sky.local("cloudy.dml")
Sky.wave = Sky.local("wave.dml")
