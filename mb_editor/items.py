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
        datablock="GemItem"
    )

    datablocks = {
        1: "GemItemRed",
        2: "GemItemYellow",
        5: "GemItemBlue",
        10: "kys"
    }

    @classmethod
    def points(cls, points, **fields):
        return cls(datablock=cls.datablocks[points], **fields)


class TimeTravel(Item):
    defaults = dict(
        datablock="TimeTravelItem",
        timeBonus=5000
    )


class SuperJump(Item):
    defaults = dict(datablock="SuperJumpItem")


class SuperSpeed(Item):
    defaults = dict(datablock="SuperSpeedItem")


class Gyrocopter(Item):
    defaults = dict(datablock="HelicopterItem")


class SuperBounce(Item):
    defaults = dict(datablock="SuperBounceItem")


class ShockAbsorber(Item):
    defaults = dict(datablock="ShockAbsorberItem")
