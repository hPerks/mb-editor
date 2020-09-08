import amble


class MissionInfo(amble.ScriptObject):
    defaults = dict(
        id='MissionInfo',
        name="New Mission",
        game='Custom',
        artist="Unknown",
        type='Custom',
        level='1',
        desc="No description set.",
        starthelptext="No start help text.",
        music=amble.Implicit(''),
    )


class NormalMissionInfo(MissionInfo):
    defaults = dict(
        gamemode='null',
        time=amble.Implicit(0),
        platinumtime=0,
        ultimatetime=0,
        awesometime=0,
    )


class HuntMissionInfo(MissionInfo):
    defaults = dict(
        gamemode='Hunt',
        radiusfromgem=30,
        maxgemsfromspawn=6,
        gemgroups=amble.Implicit(0),
        time=300000,
        score=0,
        platinumscore=0,
        ultimatescore=0,
        awesomescore=0,
    )


class LapsMissionInfo(NormalMissionInfo):
    defaults = dict(
        gamemode='Laps',
        lapsnumber=3,
    )


__all__ = ['HuntMissionInfo', 'LapsMissionInfo', 'MissionInfo', 'NormalMissionInfo']
