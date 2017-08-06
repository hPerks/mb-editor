from mb_editor.simgroup import SimGroup
from mb_editor.missioninfo import MissionInfo
from mb_editor.sky import Sky
from mb_editor.sun import Sun


class Mission(SimGroup):
    classname = "MissionGroup"

    local_dir = "~/data/missions"

    def __init__(self, **fields):
        super().__init__(**fields)

        self._missionInfo, self._sky, self._sun = MissionInfo(), Sky(), Sun()
        self.add(self.missionInfo, self.sky, self.sun)

    @property
    def missionInfo(self):
        return self._missionInfo

    @property
    def sky(self):
        return self._sky

    @property
    def sun(self):
        return self._sun

    def set_missionInfo(self, missionInfo=None, **fields):
        if missionInfo is not None:
            self.remove(self.missionInfo)
            self._missionInfo = missionInfo
            self.add(missionInfo)

        self.missionInfo.set(**fields)
        return self

    def set_sky(self, sky=None, **fields):
        if sky is not None:
            self.remove(self.sky)
            self._sky = sky
            self.add(sky)

        self.sky.set(**fields)
        return self

    def set_sun(self, sun=None, **fields):
        if sun is not None:
            self.remove(self.sun)
            self._sun = sun
            self.add(sun)

        self.sun.set(**fields)
        return self

    def write(self, filename):
        f = open(filename, 'w')
        f.write(repr(self))
        f.close()

    @classmethod
    def normal(cls, **fields):
        return cls(**fields).set_missionInfo(
            gameMode="Normal",
            parTime=0,
            platinumTime=0,
            ultimateTime=0,
            awesomeTime=0,
        )

    @classmethod
    def hunt(cls, **fields):
        return cls(**fields).set_missionInfo(
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
