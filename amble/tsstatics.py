from amble.base import SceneObject


class TSStatic(SceneObject):
    classname = 'TSStatic'


class TeleportPad(TSStatic):
    defaults = dict(shapename='~/data/shapes/teleportpad.dts')


__all__ = ['TeleportPad', 'TSStatic']
