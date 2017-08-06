from mb_editor.simgroup import SimGroup
from mb_editor.missioninfo import MissionInfo
from mb_editor.sky import Sky
from mb_editor.sun import Sun


class Mission(SimGroup):
    local_dir = "~/data/missions"

    def __init__(self, **fields):
        super().__init__(name="MissionGroup", **fields)

        self._info, self._sky, self._sun = MissionInfo(), Sky(), Sun()
        self.add(self.info, self.sky, self.sun)

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
            self.info.set(**info.fields)
        self.info.set(**fields)
        return self

    def set_sky(self, sky=None, **fields):
        if sky is not None:
            self.sky.set(**sky.fields)
        self.sky.set(**fields)
        return self

    def set_sun(self, sun=None, **fields):
        if sun is not None:
            self.sun.set(**sun.fields)
        self.sun.set(**fields)
        return self

    def write(self, filename):
        f = open(filename, 'w')
        f.write(repr(self))
        f.close()

    @classmethod
    def normal(cls, **fields):
        return cls(**fields).set_info(
            gameMode="Normal",
            parTime=0,
            platinumTime=0,
            ultimateTime=0,
            awesomeTime=0,
        )

    @classmethod
    def hunt(cls, **fields):
        return cls(**fields).set_info(
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
