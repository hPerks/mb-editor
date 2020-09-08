from amble.base import *
from amble.interior import *
from amble.items import *
from amble.mission import *
from amble.numberlists import *
from amble.parsingtests import *
from amble.pathnodes import *
from amble.staticshapes import *
from amble.triggers import *
from amble.tsstatics import *

from amble.numberlists import Color as color, Polyhedron3D as polyhedron, Rotation3D as rot, Vector3D as vec


def tests():
    import sys
    import traceback

    module = sys.modules[__name__]
    for key in dir(module):
        value = getattr(module, key)
        if isinstance(value, type):
            all_tests = getattr(value, 'tests', 0)
            inherited_tests = getattr(value.mro()[1], 'tests', 0)
            if all_tests and all_tests != inherited_tests:
                try:
                    print('testing', value)
                    tests()
                except AssertionError:
                    traceback.print_exc()


if __name__ == '__main__':
    tests()
