from mb_editor.numberlists.vector3d import Vector3D as vec
from mb_editor.numberlists.rotation3d import Rotation3D as rot
from mb_editor.numberlists.polyhedron3d import Polyhedron3D as polyhedron
from mb_editor.numberlists.color import Color as color

from mb_editor.triggers import *
from mb_editor.staticshapes import *
from mb_editor.items import *
from mb_editor.tsstatics import *

from mb_editor.interior import *
from mb_editor.movinginterior import *
from mb_editor.pathnodes import *

from mb_editor.mission import *


def tests():
    import sys, traceback

    module = sys.modules[__name__]
    for key in dir(module):
        value = getattr(module, key)
        if isinstance(value, type) and hasattr(value, "tests"):
            try:
                value.tests()
            except:
                traceback.print_exc()


if __name__ == '__main__':
    tests()
