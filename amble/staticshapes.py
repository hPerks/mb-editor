from amble.base import ID, Implicit, SceneObject


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
        fadestyle=Implicit('fade'),
        functionality=Implicit('trapdoor'),
        permanent=Implicit(0),
    )


class HelpBubble(StaticShape):
    defaults = dict(
        datablock='HelpBubble',
        text='',
        triggerradius=Implicit(3),
        persisttime=Implicit(2000),
        displayonce=Implicit(0),
    )


class PushButton(StaticShape):
    defaults = dict(
        datablock='PushButton_PQ',
        triggeronce=Implicit(0),
        resettime=Implicit(5000),
        triggerobject=Implicit(ID.none),
        objectmethod=Implicit(''),
    )


class TriggerButton(PushButton):
    defaults = dict(
        objectmethod='onentertrigger()'
    )


class Cannon(StaticShape):
    defaults = dict(
        datablock='DefaultCannon',
        aimsize=0.25,
        aimtriggers=0,
        chargetime=2000,
        force=25,
        instant=0,
        instantdelaytime=0,
        lockcam=0,
        locktime=0,
        pitch=0,
        pitchboundhigh=0,
        pitchboundlow=0,
        showaim=1,
        showreticle=0,
        usebase=1,
        usecharge=0,
        yaw=0,
        yawboundleft=0,
        yawboundright=0,
        yawlimit=0,
    )


class Checkpoint(StaticShape):
    defaults = dict(datablock='CheckPoint_PQ')


__all__ = [
    'Bumper',
    'Cannon',
    'Checkpoint',
    'DuctFan',
    'EndPad',
    'FadePlatform',
    'FinishSign',
    'HelpBubble',
    'Mine',
    'PushButton',
    'StartPad',
    'StaticShape',
    'Tornado',
    'TrapDoor',
    'TriggerButton',
]
