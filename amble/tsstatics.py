from amble.sceneobject import SceneObject


class TSStatic(SceneObject):
    classname = 'TSStatic'


class TeleportPad(TSStatic):
    defaults = dict(shapeName='~/data/shapes/teleportpad.dts')