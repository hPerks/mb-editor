import amble


class Marker(amble.SceneObject):
    classname = 'Marker'

    defaults = dict(
        seqnum=0,
        mstonext=0,
        smoothingtype='Linear',
    )


__all__ = ['Marker']
