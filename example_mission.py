if __name__ == '__main__':

    from mb_editor import *

    mission = Mission.normal()\
        .set_info(
            name="Example Mission",
            author="hPerks",
            desc="Showcasing some of the features in my text-based MB level maker.",
            startHelpText="Here's some start help text.",
            platinumTime=25000,
            ultimateTime=18000,
            awesomeTime=15500,
            music="Good To Jump To.ogg",
        ).set_sky(
            Sky.blender1
        ).set_sun(
            ambient=(0.3, 0.3, 0.4, 1)
        ).add(
            StartPad("StartPoint", position=Vector3D.zero),
            Interior.local("exampleMission.dif", position="0 0 0"),

            SuperJump(position="0 3 0"),
            HelpTrigger(
                position="-4.5 2 0", scale="8.5 2 4",
                text="Items are placed with a single tiny line of code, and customized however much you want."
            ),

            TimeTravel(position="-4 16 6.5", timeBonus=2000),

            GravityModifier(position="11 12 7", rotation="0 -1 0 90"),
            GravityModifier(position="13 12 19", rotation="0 -1 0 180"),
            HelpTrigger(
                position="10 8 6", scale="2 8.5 4",
                text="There are many tools for handling lists of numbers like positions and rotations. You can even "
                     "(finally) combine rotations with a simple * sign!"
            ),

            *Bumper(scale="1.5 1.5 1.5").copies(
                "position",
                "21 -3 18", "25 -3 18",
                "23 -1 18", "27 -1 18",
                "21 1 18", "25 1 18",
                "23 3 18", "27 3 18",
            ),
            HelpTrigger(
                position="20 -8 18", scale="8.5 16 4",
                text="Placing multiple similar items is made super easy with functions like copies(), as well as the "
                     "builtlin loops and list comprehensions in Python."
            ),

            MovingInterior.make(
                PathedInterior.local("exampleMission.dif", 0),
                Path.make_accelerate("0 0 0", 3500, "0 0 12", 1500, "0 0 0")
            ),
            HelpTrigger(
                position="12 -16.5 18", scale="8 8.5 4",
                text="There are quite a few convenient ways to build moving platforms. This one uses the "
                     "MovingInterior.make() and Path.make_accelerate() builders."
            ),

            *[SimGroup(*TrapDoor().copies("position", *[(x,y,30) for x in range(-3,5,2)])) for y in range(-7,9,2)],
            HelpTrigger(
                position="-4.5 -8 30", scale="8.5 16 4",
                text="These trapdoors would take ages to make and tweak using either the LE or a normal text editor. "
                     "Here it's done in one (cramped) line of code, using SimGroups, copies(), and Python's range()."
            ),

            HelpTrigger(
                polyhedron=Polyhedron3D.make(o="4 8 30", i="16 0 6", j="0 8 0", k="0 0 4"),
                text="This help trigger is skewed so as to align with the ramp. You can't activate it from below!",
            ),

            TeleportPad(position="24 6 36", scale=".25 .25 .25"),
            *TeleportTrigger(position="22.5 4.5 36", scale="3 3 2").and_destination("destination", "24 0 48"),
            HelpTrigger(
                position="20 4 36", scale="8.5 12.5 4",
                text="The ObjectName type facilitates linking objects, like teleports and destinations. Instance "
                     "methods such as TeleportTrigger.and_destination() and EndPad.and_sign() make this even simpler."
            ),

            NestEgg(position="24 -6 40"),
            TeleportPad(position="24 -12 40", scale=".25 .25 .25"),
            TeleportTrigger(position="22.5 -14.5 40", scale="3 3 2", destination="destination"),

            *EndPad(position="12 0 48", rotation="0 0 -1 90").and_sign(),

        ).write("data/missions_pq/exampleMission.mis")
