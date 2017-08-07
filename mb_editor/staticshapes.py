from mb_editor.physicalobject import PhysicalObject


class StaticShape(PhysicalObject):
    classname = "StaticShape"


class StartPad(StaticShape):
    defaults = dict(datablock="StartPad")


class EndPad(StaticShape):
    defaults = dict(datablock="EndPad")

    def and_sign(self, offset="0 0 4", **fields):
        return [self, FinishSign(position=self.position + offset, **fields)]


class FinishSign(StaticShape):
    defaults = dict(datablock="RegularFinishLineSign")


class Bumper(StaticShape):
    defaults = dict(datablock="RoundBumper_PQ")


class DuctFan(StaticShape):
    defaults = dict(datablock="DuctFan_PQ")


class Mine(StaticShape):
    defaults = dict(datablock="LandMine_PQ")


class TrapDoor(StaticShape):
    defaults = dict(datablock="TrapDoor_PQ")


class Tornado(StaticShape):
    defaults = dict(datablock="Tornado_PQ")