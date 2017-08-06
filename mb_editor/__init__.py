from mb_editor.numberlists.numberlist import NumberList
from mb_editor.numberlists.vector3d import Vector3D
from mb_editor.numberlists.rotation3d import Rotation3D
from mb_editor.numberlists.polyhedron3d import Polyhedron3D
from mb_editor.numberlists.color import Color

from mb_editor.objectname import ObjectName
from mb_editor.field import Field

from mb_editor.scriptobject import ScriptObject
from mb_editor.simgroup import SimGroup
from mb_editor.physicalobject import PhysicalObject, BoundedObject

from mb_editor.triggers import Trigger, SpawnTrigger, HelpTrigger, TeleportTrigger, RelativeTPTrigger, DestinationTrigger
from mb_editor.staticshapes import StaticShape, StartPad, EndPad, FinishSign, Bumper, DuctFan, Mine, TrapDoor, Tornado
from mb_editor.items import Item, Gem, TimeTravel, SuperJump, SuperSpeed, Gyrocopter, SuperBounce, ShockAbsorber

from mb_editor.interior import Interior
from mb_editor.path import Marker, Path
from mb_editor.movinginterior import PathedInterior, MovingInterior

from mb_editor.missioninfo import MissionInfo
from mb_editor.sky import Sky
from mb_editor.sun import Sun

from mb_editor.mission import Mission


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
