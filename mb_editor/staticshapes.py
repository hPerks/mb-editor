from mb_editor.physicalobject import PhysicalObject


class StaticShape(PhysicalObject):
    classname = "StaticShape"


class StartPad(StaticShape):
    defaults = dict(datablock="StartPad")


class EndPad(StaticShape):
    defaults = dict(datablock="EndPad")


class FinishSign(StaticShape):
    defaults = dict(datablock="SignFinish")


class Bumper(StaticShape):
    defaults = dict(datablock="Bumper")


class DuctFan(StaticShape):
    defaults = dict(datablock="DuctFan")


class Mine(StaticShape):
    defaults = dict(datablock="LandMine")


class TrapDoor(StaticShape):
    defaults = dict(datablock="TrapDoor")


class Tornado(StaticShape):
    defaults = dict(datablock="Tornado")