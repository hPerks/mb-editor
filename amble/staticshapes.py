from amble.id import ID
from amble.implicit import Implicit
from amble.sceneobject import SceneObject


class StaticShape(SceneObject):
    classname = 'StaticShape'


class StartPad(StaticShape):
    defaults = dict(datablock='StartPad_PQ')


class EndPad(StaticShape):
    defaults = dict(datablock='EndPad_PQ')

    def with_sign(self, offset='0 0 4', **fields):
        return self.with_friends(FinishSign(position=self.position + offset, **fields))


class FinishSign(StaticShape):
    defaults = dict(datablock='RegularFinishLineSign')


class Bumper(StaticShape):
    defaults = dict(datablock='RoundBumper_PQ')


class DuctFan(StaticShape):
    defaults = dict(datablock='DuctFan_PQ')


class Mine(StaticShape):
    defaults = dict(datablock='LandMine_PQ')


class TrapDoor(StaticShape):
    defaults = dict(datablock='TrapDoor_PQ')


class Tornado(StaticShape):
    defaults = dict(datablock='Tornado_PQ')


class FadePlatform(StaticShape):
    defaults = dict(
        datablock='FadePlatform',
        fadeStyle=Implicit('fade'),
        functionality=Implicit('trapdoor'),
        permanent=Implicit(0),
    )


class HelpBubble(StaticShape):
    defaults = dict(
        datablock='HelpBubble',
        text='',
        triggerRadius=Implicit(3),
        persistTime=Implicit(2000),
        displayOnce=Implicit(0),
    )


class PushButton(StaticShape):
    defaults = dict(
        datablock='PushButton_PQ',
        triggerOnce=Implicit(0),
        resetTime=Implicit(5000),
        triggerObject=Implicit(ID.none),
        objectMethod=Implicit(''),
    )


class TriggerButton(PushButton):
    defaults = dict(
        objectMethod='onEnterTrigger()'
    )


class Cannon(StaticShape):
    defaults = dict(
        datablock='DefaultCannon',
        aimSize=0.25,
        aimTriggers=0,
        chargeTime=2000,
        force=25,
        instant=0,
        instantDelayTime=0,
        lockCam=0,
        lockTime=0,
        pitch=0,
        pitchBoundHigh=0,
        pitchBoundLow=0,
        showAim=1,
        showReticle=0,
        useBase=1,
        useCharge=0,
        yaw=0,
        yawBoundLeft=0,
        yawBoundRight=0,
        yawLimit=0,
    )


class Checkpoint(StaticShape):
    defaults = dict(datablock='CheckPoint_PQ')
