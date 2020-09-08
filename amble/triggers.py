from amble.base import BoundedObject, Field, Fields, ID, Implicit
from amble.numberlists import Rotation3D, Vector3D
from amble.tsstatics import TeleportPad


class Trigger(BoundedObject):
    classname = 'Trigger'

    defaults = dict(
        triggeronce=Implicit(0)
    )


class InBoundsTrigger(Trigger):
    defaults = dict(datablock='InBoundsTrigger')


class SpawnTrigger(Trigger):
    defaults = dict(datablock='SpawnTrigger')


class HelpTrigger(Trigger):
    defaults = dict(
        datablock='HelpTrigger',
        text='',
    )


class TeleportTrigger(Trigger):
    defaults = dict(
        datablock='TeleportTrigger',
        destination=ID.none,
        delay=Implicit(2000),
        silent=Implicit(0),
    )

    def with_destination(self, id, position, **fields):
        self.destination = id
        return self.with_friends(DestinationTrigger(id, position=position, **fields))

    def with_pad(self, offset='8 8 0', **fields):
        return self.with_friends(TeleportPad(position=self.position + offset, **fields))


    @staticmethod
    def tests():
        t = TeleportTrigger(position='4 2 0')
        td = t.with_destination('d', '0 6 9')
        tdp = td.with_pad(id='pad!', offset='4 4 0', scale='0.5 0.5 0.5')

        assert tdp.friends['pad!'].scale == '0.5 0.5 0.5'


class RelativeTPTrigger(TeleportTrigger):
    defaults = dict(
        datablock='RelativeTPTrigger',
        delay=Implicit(0),
        silent=Implicit(1),
    )


class DestinationTrigger(Trigger):
    defaults = dict(datablock='DestinationTrigger')


class LapsCheckpointTrigger(Trigger):
    defaults = dict(
        datablock='LapsCheckpoint',
        checkpointNumber=0,
    )


class LapsCounterTrigger(Trigger):
    defaults = dict(datablock='LapsCounterTrigger')


class TriggerGotoTarget(Trigger):
    defaults = dict(
        datablock='TriggerGotoTarget',
        targettime=-1,
    )


class GravityWellTrigger(Trigger):
    defaults = dict(
        datablock='GravityWellTrigger',
        axis=Vector3D.zero,
        custompoint=Vector3D.none,
        invert=Implicit(0),
        restoreGravity=Implicit(Rotation3D.none),
        useRadius=Implicit(0),
        radius=Implicit(0),
    )


class PhysModTrigger(Trigger):
    defaults = dict(
        datablock='MarblePhysModTrigger',
    )

    physics_field_names = [
        'maxrollvelocity', 'angularacceleration', 'brakingacceleration', 'airacceleration', 'gravity', 'staticfriction',
        'kineticfriction', 'bouncekineticfriction', 'maxdotslide', 'bouncerestitution', 'jumpimpulse', 'maxforceradius',
        'mass'
    ]

    def written_fields(self):
        fields_list = list(filter(
            lambda field: field.key not in self.physics_field_names,
            super().written_fields().list
        ))

        index = 0
        for name in self.physics_field_names:
            value = self.fields.get(name)
            if value is not None:
                fields_list += [
                    Field(f'marbleattribute{index}', name, str),
                    Field(f'value{index}', value, type(value))
                ]

                index += 1

        return Fields(fields_list)


    @staticmethod
    def tests():
        t = PhysModTrigger(gravity=4, jumpimpulse=20)
        assert t.gravity == 4
        assert t.written_fields().get('jumpimpulse') is None
        assert t.written_fields().get('value1') == 20


class PathTrigger(Trigger):
    defaults = dict(
        datablock='PathTrigger',
        triggeronce=Implicit(1),
    )


if __name__ == '__main__':
    TeleportTrigger.tests()
    PhysModTrigger.tests()

__all__ = [
    'DestinationTrigger',
    'GravityWellTrigger',
    'HelpTrigger',
    'InBoundsTrigger',
    'LapsCheckpointTrigger',
    'LapsCounterTrigger',
    'PathTrigger',
    'PhysModTrigger',
    'RelativeTPTrigger',
    'SpawnTrigger',
    'TeleportTrigger',
    'Trigger',
    'TriggerGotoTarget',
]
