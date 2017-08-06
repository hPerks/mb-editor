from mb_editor.numberlists.color import Color
from mb_editor.numberlists.vector3d import Vector3D
from mb_editor.scriptobject import ScriptObject


class Sun(ScriptObject):
    classname = "Sun"

    defaults = dict(
        direction=Vector3D(0.5, 0.5, -0.5),
        color=Color(1.4, 1.2, 0.4, 1),
        ambient=Color(0.3, 0.3, 0.4, 1),
    )

Sun.normal = Sun(
    direction="0.5 0.5 -0.5",
    color="1.4 1.2 0.4 1",
    ambient="0.3 0.3 0.4 1",
)