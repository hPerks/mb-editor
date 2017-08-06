from mb_editor.physicalobject import PhysicalObject

class TSStatic(PhysicalObject):
    classname = "TSStatic"

class TeleportPad(TSStatic):
    defaults = dict(shapeName="~/data/shapes/teleportpad.dts")
