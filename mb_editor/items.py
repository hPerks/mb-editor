from mb_editor.implicit import Implicit
from mb_editor.physicalobject import PhysicalObject


class Item(PhysicalObject):
    classname = "Item"

    defaults = dict(
        collideable=0,
        static=1,
        rotate=1
    )


class Gem(Item):
    defaults = dict(
        datablock="GemItem_PQ"
    )

    datablocks = {
        1: "GemItemRed_PQ",
        2: "GemItemYellow_PQ",
        5: "GemItemBlue_PQ",
        10: "kys"
    }

    @classmethod
    def points(cls, points, **fields):
        return cls(datablock=cls.datablocks[points], **fields)


class TimeTravel(Item):
    defaults = dict(
        datablock="TimeTravelItem_PQ",
        timeBonus=Implicit(5000)
    )


class SuperJump(Item):
    defaults = dict(datablock="SuperJumpItem_PQ")


class SuperSpeed(Item):
    defaults = dict(datablock="SuperSpeedItem_PQ")


class Gyrocopter(Item):
    defaults = dict(datablock="HelicopterItem_PQ")


class SuperBounce(Item):
    defaults = dict(datablock="SuperBounceItem_PQ")


class ShockAbsorber(Item):
    defaults = dict(datablock="ShockAbsorberItem_PQ")


class GravityModifier(Item):
    defaults = dict(datablock="AntiGravityItem_PQ")


class Anvil(Item):
    defaults = dict(datablock="AnvilItem")


class NestEgg(Item):
    defaults = dict(datablock="NestEgg_PQ")
