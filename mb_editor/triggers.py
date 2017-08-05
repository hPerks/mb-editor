from mb_editor.physicalobject import BoundedObject


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


class RelativeTPTrigger(Trigger):
    defaults = dict(
        datablock="RelativeTPTrigger",
        destination="",
        delay=0,
        silent=1,
    )


class DestinationTrigger(Trigger):
    defaults = dict(datablock="DestinationTrigger")
