if __name__ == '__main__':

    from mb_editor import *

    mission = Mission.normal()\
        .set_missionInfo(
            name="Example Mission",
            author="Your name here",
            desc="Example description",
            startHelpText="Example start help text",
            platinumTime=5000,
            ultimateTime=4000,
            awesomeTime=3000,
        ).set_sky(
            materialList="~/data/skies/sky_day.dml"
        ).add(
            StartPad("StartPoint").set(
                position="0 0 0"
            ),
            EndPad("EndPoint").set(
                position=[8, 0, 0],
                rotation=[0, 0, 1, 180]
            ),
        ).write("missions/exampleMission.mis")