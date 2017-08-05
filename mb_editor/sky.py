from mb_editor.numberlists.color import Color
from mb_editor.numberlists.rotation3d import Rotation3D
from mb_editor.numberlists.vector3d import Vector3D
from mb_editor.scriptobject import ScriptObject


class Sky(ScriptObject):
    classname = "Sky"

    local_dir = "~/data/skies"

    defaults = dict(
        position=Vector3D(336, 136, 0),
        rotation=Rotation3D.identity,
        scale=Vector3D.one,
        visibleDistance=500,
        useSkyTextures=1,
        renderBottomTexture=1,
        skySolidColor=Color(0.6, 0.6, 0.6, 1),
        materialList="~/data/skies/sky_day.dml",
        windVelocity=Vector3D.i,
        windEffectPrecipitation=0,
        noRenderBans=1,
    )

    @classmethod
    def local(cls, materialList, **fields):
        return cls(materialList="{}/{}".format(cls.local_dir, materialList), **fields)
