from mb_editor.field import Field, Fields
from mb_editor.physicalobject import BoundedObject
from mb_editor.objectname import ObjectName
from mb_editor.tsstatics import TeleportPad
from mb_editor.numberlists.vector3d import Vector3D
from mb_editor.numberlists.rotation3d import Rotation3D


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
        return self.with_friends(DestinationTrigger(name, position=position, **fields))

    def with_pad(self, offset="8 8 0", **fields):
        return self.with_friends(TeleportPad(position=self.position + offset, **fields))


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


class LapsCheckpointTrigger(Trigger):
    defaults = dict(
        datablock="LapsCheckpoint",
        checkpointNumber=0,
    )


class LapsCounterTrigger(Trigger):
    defaults = dict(datablock="LapsCounterTrigger")


class TriggerGotoTarget(Trigger):
    defaults = dict(
        datablock="TriggerGotoTarget",
        targetTime=-1,
    )


class GravityWellTrigger(Trigger):
    defaults = dict(
        datablock="GravityWellTrigger",
        axis="x",
        customPoint=Vector3D.none,
        invert=0,
        restoreGravity=Rotation3D.none,
        useRadius=0,
        radius=0,
    )


class PhysModTrigger(Trigger):
    defaults = dict(
        datablock="MarblePhysModTrigger",
    )

    physics_field_names = [
        "maxRollVelocity", "angularAcceleration", "brakingAcceleration", "airAcceleration", "gravity", "staticFriction",
        "kineticFriction", "bounceKineticFriction", "maxDotSlide", "bounceRestitution", "jumpImpulse", "maxForceRadius",
        "mass"
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
                    Field("marbleAttribute{}".format(index), name, str),
                    Field("value{}".format(index), value, type(value))
                ]

                index += 1

        return Fields(fields_list)


    @staticmethod
    def tests():
        t = PhysModTrigger(gravity=4, jumpImpulse=20)
        assert t.gravity == 4
        assert t.written_fields().get("jumpImpulse") is None
        assert t.written_fields().get("value1") == 20


if __name__ == '__main__':
    TeleportTrigger.tests()
    PhysModTrigger.tests()
