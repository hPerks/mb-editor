from amble.scriptobject import ScriptObject
from amble.implicit import Implicit


class MissionInfo(ScriptObject):
    defaults = dict(
        id='MissionInfo',
        name='New Mission',
        game='PQ',
        artist='Unknown',
        type='Custom',
        level='1',
        desc='No description set.',
        startHelpText='No start help text.',

        music=Implicit(''),
    )


class NormalMissionInfo(MissionInfo):
    defaults = dict(
        gameMode='Normal',
        parTime=Implicit(0),
        platinumTime=0,
        ultimateTime=0,
        awesomeTime=0,
    )


class HuntMissionInfo(MissionInfo):
    defaults = dict(
        gameMode='Hunt',
        radiusFromGem=30,
        maxGemsPerSpawn=6,
        gemGroups=Implicit(0),
        time=300000,
        parScore=0,
        platinumScore=0,
        ultimateScore=0,
        awesomeScore=0,
    )


class LapsMissionInfo(NormalMissionInfo):
    defaults = dict(
        gameMode='Laps',
        lapsNumber=3,
    )
