from amble.interior import *
from amble.items import *
from amble.mapping.brush import *
from amble.mapping.faces import *
from amble.mapping.map import *
from amble.mapping.texture import *
from amble.mission import *
from amble.movinginterior import *
from amble.numberlists.color import Color as color
from amble.numberlists.polyhedron3d import Polyhedron3D as polyhedron
from amble.numberlists.rotation3d import Rotation3D as rot
from amble.numberlists.vector3d import Vector3D as vec
from amble.path import *
from amble.pathnodes import *
from amble.scriptobject import *
from amble.simgroup import *
from amble.sky import *
from amble.staticshapes import *
from amble.sun import *
from amble.triggers import *
from amble.tsstatics import *


def tests():
    import sys, traceback

    module = sys.modules[__name__]
    for key in dir(module):
        value = getattr(module, key)
        if isinstance(value, type):
            tests = getattr(value, 'tests', 0)
            inherited_tests = getattr(value.mro()[1], 'tests', 0)
            if tests and tests != inherited_tests:
                try:
                    print('testing', value)
                    tests()
                except:
                    traceback.print_exc()
            else:
                print('no tests for', value)


if __name__ == '__main__':
    tests()
