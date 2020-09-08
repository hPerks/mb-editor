import amble
from amble.numberlists import Color, Vector3D


class Sun(amble.ScriptObject):
    classname = 'Sun'

    defaults = dict(
        direction=Vector3D(0.5, 0.5, -0.5),
        color=Color(1.4, 1.2, 0.4, 1),
        ambient=Color(0.3, 0.3, 0.4, 1),
    )

    normal = None


Sun.normal = Sun(
    direction='0.5 0.5 -0.5',
    color='1.4 1.2 0.4 1',
    ambient='0.3 0.3 0.4 1',
)

__all__ = ['Sun']
