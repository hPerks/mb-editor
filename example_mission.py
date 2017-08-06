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
            Sky.local("sky_day.dml")
        ).set_sun(
            ambient=(0.3, 0.3, 0.4, 1)
        ).add(
            StartPad("StartPoint").set(
                position="0 0 0"
            ),
            EndPad("EndPoint").set(
                position=[8, 0, 0],
                rotation=[0, 0, 1, 180],
            ),
            Interior.local(
                "exampleMission.dif",
                position="0 0 0",
            ),
            *Gem("ThisIsJustTheNameBtw", scale=(Vector3D.one * 2)).copies(
                ("position", "datablock"),
                ("0 4 0", "GemItemRed"),
                ("0 8 0", "GemItemOrange"),
                ("4 8 0", "GemItemYellow"),
                ("8 8 0", "GemItemGreen"),
                ("8 4 0", "GemItemBlue"),
            ),
            MovingInterior.make(
                PathedInterior.local("exampleMission.dif", 0),
                *Marker(smoothingType="Accelerate").copies(
                    ("position", "msToNext"),
                    "0 0 0", 5000,
                    "0 -4 0", 500,
                    "0 2 0", 1000,
                ),
            ),
        ).write("missions/exampleMission.mis")
