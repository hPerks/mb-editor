from mb_editor.implicit import Implicit
from mb_editor.simgroup import SimGroup
from mb_editor.missioninfo import *
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
