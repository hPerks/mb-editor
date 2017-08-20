from mb_editor.simgroup import SimGroup
from mb_editor.missioninfo import MissionInfo
from mb_editor.sky import Sky
from mb_editor.sun import Sun
from mb_editor.physicalobject import PhysicalObject
from mb_editor.triggers import InBoundsTrigger
from mb_editor.utils.lists import flatlist
from mb_editor.triggers import LapsCheckpointTrigger


class Mission(SimGroup):
    local_dir = "~/data/missions"

    def __init__(self, **fields):
        super().__init__(name="MissionGroup", **fields)

        self._info, self._sky, self._sun = MissionInfo(), Sky(), Sun()
        self.add(self.info, self.sky, self.sun)

    def __repr__(self):
        return "//--- OBJECT WRITE BEGIN ---\n" + super().__repr__()

    @property
    def info(self):
        return self._info

    @property
    def sky(self):
        return self._sky

    @property
    def sun(self):
        return self._sun

    def set_info(self, info=None, **fields):
        if info is not None:
            self.info.set(**info.fields.dict)
        self.info.set(**fields)
        return self

    def set_sky(self, sky=None, **fields):
        if sky is not None:
            self.sky.set(**sky.fields.dict)
        self.sky.set(**fields)
        return self

    def set_sun(self, sun=None, **fields):
        if sun is not None:
            self.sun.set(**sun.fields.dict)
        self.sun.set(**fields)
        return self

    def autobounds(self, horizontal_margin=20, top_margin=100, bottom_margin=20):
        descendant_positions = [
            descendant.position
            for descendant in self.descendants()
            if isinstance(descendant, PhysicalObject)
        ]

        minimum = descendant_positions[0].map(min, *descendant_positions)
        maximum = descendant_positions[0].map(max, *descendant_positions)

        return self.add(InBoundsTrigger(
            name="Bounds",
            position=minimum - (horizontal_margin, horizontal_margin, bottom_margin),
            scale=maximum - minimum + (2 * horizontal_margin, 2 * horizontal_margin, top_margin + bottom_margin)
        ))

    def write(self, filename):
        if not any(d.datablock == "InBoundsTrigger" for d in self.descendants()):
            raise Exception("Trying to write mission file without InBoundsTrigger")

        f = open(filename, 'w')
        f.write(repr(self))
        f.close()


class NormalMission(Mission):

    def __init__(self, **fields):
        super().__init__(**fields)
        self.set_info(
            gameMode="Normal",
            parTime=0,
            platinumTime=0,
            ultimateTime=0,
            awesomeTime=0,
        )


class HuntMission(Mission):

    def __init__(self, **fields):
        super().__init__(**fields)
        self.set_info(
            gameMode="Hunt",
            radiusFromGem=30,
            maxGemsPerSpawn=6,
            gemGroups=0,
            time=300000,
            parScore=0,
            platinumScore=0,
            ultimateScore=0,
            awesomeScore=0,
        )


class LapsMission(NormalMission):

    def __init__(self, **fields):
        super().__init__(**fields)
        self.set_info(
            gameMode="Laps",
            lapsNumber=3
        )

    def add_laps_checkpoint_triggers(self, *laps_checkpoint_triggers):
        return super().add([
            trigger.set(checkpointNumber=checkpointNumber)
            for checkpointNumber, trigger in enumerate(flatlist(*laps_checkpoint_triggers))
        ])
