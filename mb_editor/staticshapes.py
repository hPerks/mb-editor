from mb_editor.implicit import Implicit
from mb_editor.physicalobject import PhysicalObject


class StaticShape(PhysicalObject):
    classname = "StaticShape"


class StartPad(StaticShape):
    defaults = dict(datablock="StartPad_PQ")


class EndPad(StaticShape):
    defaults = dict(datablock="EndPad_PQ")

    def with_sign(self, offset="0 0 4", **fields):
        return self.with_friends(FinishSign(position=self.position + offset, **fields))


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


class FadePlatform(StaticShape):
    defaults = dict(
        datablock="FadePlatform",
        fadeStyle=Implicit("fade"),
        functionality=Implicit("trapdoor"),
        permanent=Implicit(0),
    )


class HelpBubble(StaticShape):
    defaults = dict(
        datablock="HelpBubble",
        text="",
        triggerRadius=Implicit(3),
        persistTime=Implicit(2000),
        displayOnce=Implicit(0),
    )
