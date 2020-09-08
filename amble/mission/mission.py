import os

import amble
from amble.mission.missioninfo import MissionInfo, NormalMissionInfo, HuntMissionInfo, LapsMissionInfo
from amble.mission.sky import Sky
from amble.mission.sun import Sun
from amble.utils.lists import flatlist
from amble.utils import path


class Mission(amble.SimGroup):
    defaults = dict(
        info=MissionInfo(),
        sky=Sky(),
        sun=Sun(),
    )

    def __init__(self, *children, **fields):
        if 'id' not in fields:
            super().__init__(id='MissionGroup', *children, **fields)
        else:
            super().__init__(*children, **fields)

    def __str__(self):
        return '//--- OBJECT WRITE BEGIN ---\n' + super().__str__()

    def autobounds(self, horizontal_margin=20, top_margin=100, bottom_margin=20):
        descendant_positions = [
            descendant.position
            for descendant in self.descendants()
            if isinstance(descendant, amble.SceneObject)
        ]

        minimum = descendant_positions[0].map(min, *descendant_positions)
        maximum = descendant_positions[0].map(max, *descendant_positions)

        return self.add(amble.InBoundsTrigger(
            id='Bounds',
            position=minimum - (horizontal_margin, horizontal_margin, bottom_margin),
            scale=maximum - minimum + (2 * horizontal_margin, 2 * horizontal_margin, top_margin + bottom_margin)
        ))

    def write(self, filename):
        assert any(d.datablock == 'InBoundsTrigger' for d in self.descendants()), \
            'Trying to write mission file without InBoundsTrigger'

        if not filename.endswith('.mis'):
            filename += '.mis'
        with open(path.platinum('data/missions/custom', filename), 'w') as f:
            f.write(str(self))

    @classmethod
    def from_file(cls, filename):
        if not filename.endswith('.mis'):
            filename += '.mis'

        if os.path.exists(path.platinum('data/missions/custom', filename)):
            filename = path.platinum('data/missions/custom', filename)

        with open(filename, errors='ignore') as f:
            return cls.from_string(f.read().split('//--- OBJECT WRITE BEGIN ---\n')[-1])

    @classmethod
    def normal(cls, *children, **fields):
        return cls(*children, info=NormalMissionInfo(**fields))

    @classmethod
    def hunt(cls, *children, **fields):
        return cls(*children, info=HuntMissionInfo(**fields))

    @classmethod
    def laps(cls, *children, **fields):
        return cls(*children, info=LapsMissionInfo(**fields))

    def add_laps_checkpoint_triggers(self, *laps_checkpoint_triggers):
        return self.add([
            trigger.set(checkpointnumber=checkpointnumber)
            for checkpointnumber, trigger in enumerate(flatlist(*laps_checkpoint_triggers))
        ])


__all__ = ['Mission']
