from mb_editor.physicalobject import BoundedObject
from mb_editor.objectname import ObjectName


class Trigger(BoundedObject):
    classname = "Trigger"

    defaults = dict(
        triggerOnce=0
    )


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

    def and_destination(self, name, position, **fields):
        self.destination = name
        return [self, DestinationTrigger(name, position=position, **fields)]


class RelativeTPTrigger(TeleportTrigger):
    defaults = dict(
        datablock="RelativeTPTrigger",
        delay=0,
        silent=1,
    )


class DestinationTrigger(Trigger):
    defaults = dict(datablock="DestinationTrigger")

