from amble.simgroup import SimGroup
from amble.missioninfo import *
from amble.sky import Sky
from amble.sun import Sun
from amble.sceneobject import SceneObject
from amble.triggers import InBoundsTrigger
from amble.utils.lists import flatlist
from amble.utils import path


class Mission(SimGroup):
    defaults = dict(
        info=MissionInfo(),
        sky=Sky(),
        sun=Sun(),
    )

    def __init__(self, **fields):
        if 'id' not in fields:
            super().__init__(id='MissionGroup', **fields)
        else:
            super().__init__(**fields)

    def __repr__(self):
        return '//--- OBJECT WRITE BEGIN ---\n' + super().__repr__()

    def autobounds(self, horizontal_margin=20, top_margin=100, bottom_margin=20):
        descendant_positions = [
            descendant.position
            for descendant in self.descendants()
            if isinstance(descendant, SceneObject)
        ]

        minimum = descendant_positions[0].map(min, *descendant_positions)
        maximum = descendant_positions[0].map(max, *descendant_positions)

        return self.add(InBoundsTrigger(
            id='Bounds',
            position=minimum - (horizontal_margin, horizontal_margin, bottom_margin),
            scale=maximum - minimum + (2 * horizontal_margin, 2 * horizontal_margin, top_margin + bottom_margin)
        ))

    def write(self, filename):
        if not any(d.datablock == 'InBoundsTrigger' for d in self.descendants()):
            raise Exception('Trying to write mission file without InBoundsTrigger')

        if not filename.endswith('.mis'):
            filename += '.mis'
        with open(path.platinum('data/missions/custom', filename), 'w') as f:
            f.write(repr(self))

    @classmethod
    def from_file(cls, filename):
        if not filename.endswith('.mis'):
            filename += '.mis'

        f = open(path.platinum('data/missions/custom', filename), errors='ignore')
        string = f.read()
        f.close()

        return cls.from_string(string.split('//--- OBJECT WRITE BEGIN ---\n')[1])

    @classmethod
    def normal(cls, *args, **fields):
        return cls(*args, info=NormalMissionInfo(**fields))

    @classmethod
    def hunt(cls, *args, **fields):
        return cls(*args, info=HuntMissionInfo(**fields))

    @classmethod
    def laps(cls, *args, **fields):
        return cls(*args, info=LapsMissionInfo(**fields))

    def add_laps_checkpoint_triggers(self, *laps_checkpoint_triggers):
        return self.add([
            trigger.set(checkpointNumber=checkpointNumber)
            for checkpointNumber, trigger in enumerate(flatlist(*laps_checkpoint_triggers))
        ])
