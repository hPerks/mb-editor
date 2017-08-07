from mb_editor.physicalobject import BoundedObject
from mb_editor.objectname import ObjectName
from mb_editor.tsstatics import TeleportPad


class Trigger(BoundedObject):
    classname = "Trigger"

    defaults = dict(
        triggerOnce=0
    )


class InBoundsTrigger(Trigger):
    defaults = dict(datablock="InBoundsTrigger")


class SpawnTrigger(Trigger):
    defaults = dict(datablock="SpawnTrigger")


class HelpTrigger(Trigger):
    defaults = dict(
        datablock="HelpTrigger",
        text="",
    )


class TeleportTrigger(Trigger):
    defaults = dict(
        datablock="TeleportTrigger",
        destination=ObjectName.none,
        delay=2000,
        silent=0,
    )

    def with_destination(self, name, position, **fields):
        self.destination = name
        return self.with_friend(DestinationTrigger(name, position=position, **fields))

    def with_pad(self, offset="8 8 0", **fields):
        return self.with_friend(TeleportPad(position=self.position + offset, **fields))


    @staticmethod
    def tests():
        t = TeleportTrigger(position="4 2 0")
        td = t.with_destination("d", "0 6 9")
        tdp = td.with_pad(offset="4 4 0", scale="0.5 0.5 0.5")

        assert tdp.friends[1].scale == "0.5 0.5 0.5"


class RelativeTPTrigger(TeleportTrigger):
    defaults = dict(
        datablock="RelativeTPTrigger",
        delay=0,
        silent=1,
    )


class DestinationTrigger(Trigger):
    defaults = dict(datablock="DestinationTrigger")


if __name__ == '__main__':
    TeleportTrigger.tests()
