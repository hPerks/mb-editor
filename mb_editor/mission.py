from mb_editor.implicit import Implicit
from mb_editor.simgroup import SimGroup
from mb_editor.missioninfo import MissionInfo
from mb_editor.sky import Sky
from mb_editor.sun import Sun
from mb_editor.physicalobject import PhysicalObject
from mb_editor.triggers import InBoundsTrigger
from mb_editor.utils.lists import flatlist


class Mission(SimGroup):
    local_dir = "~/data/missions"

    defaults = dict(
        info=MissionInfo(),
        sky=Sky(),
        sun=Sun(),
    )

    def __init__(self, *args, **fields):
        super().__init__(*args, **fields)

        for field in self.info.fields.list:
            if field.key in fields:
                self.info.fields.set(field.key, fields[field.key])
                self.fields.delete(field.key)

    def __repr__(self):
        return "//--- OBJECT WRITE BEGIN ---\n" + super().__repr__()

    def autobounds(self, horizontal_margin=20, top_margin=100, bottom_margin=20):
        descendant_positions = [
            descendant.position
            for descendant in self.descendants()
            if isinstance(descendant, PhysicalObject)
        ]

        minimum = descendant_positions[0].map(min, *descendant_positions)
        maximum = descendant_positions[0].map(max, *descendant_positions)

        return self.add(InBoundsTrigger(
            id="Bounds",
            position=minimum - (horizontal_margin, horizontal_margin, bottom_margin),
            scale=maximum - minimum + (2 * horizontal_margin, 2 * horizontal_margin, top_margin + bottom_margin)
        ))

    def write(self, filename):
        if not any(d.datablock == "InBoundsTrigger" for d in self.descendants()):
            raise Exception("Trying to write mission file without InBoundsTrigger")

        f = open(filename, 'w')
        f.write(repr(self))
        f.close()


    @classmethod
    def from_file(cls, filename):
        f = open(filename, 'r')
        string = f.read()
        f.close()

        return cls.from_string(string)


class NormalMission(Mission):
    defaults = dict(
        info=MissionInfo(
            gameMode="Normal",
            parTime=Implicit(0),
            platinumTime=0,
            ultimateTime=0,
            awesomeTime=0,
        )
    )


class HuntMission(Mission):
    defaults = dict(
        info=MissionInfo(
            gameMode="Hunt",
            radiusFromGem=30,
            maxGemsPerSpawn=6,
            gemGroups=Implicit(0),
            time=300000,
            parScore=0,
            platinumScore=0,
            ultimateScore=0,
            awesomeScore=0,
        )
    )


class LapsMission(NormalMission):
    defaults = dict(
        info=MissionInfo(
            gameMode="Laps",
            parTime=Implicit(0),
            platinumTime=0,
            ultimateTime=0,
            awesomeTime=0,
            lapsNumber=3
        )
    )

    def add_laps_checkpoint_triggers(self, *laps_checkpoint_triggers):
        return super().add([
            trigger.set(checkpointNumber=checkpointNumber)
            for checkpointNumber, trigger in enumerate(flatlist(*laps_checkpoint_triggers))
        ])
