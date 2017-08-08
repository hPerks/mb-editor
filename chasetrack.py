from mb_editor import *

mission = LapsMission().set_info(
    name="Chasetrack",
    author="hPerks",
    desc="Chase after the gems around the track. Can you get them all in 3 laps?",
    startHelpText="No cheating - you still have to do 3 laps!",
    parTime=150000,
    platinumTime=90000,
    ultimateTime=70000,
    awesomeTime=55000,
).set_sky(
    Sky.wave
).add(
    StartPad(position="8 2 0", rotation="0 0 -1 90"),
    Interior.local("chasetrack.dif"),
    Interior.local("chasetrack_tightrope.dif").copies(
        ("position", "scale"),
        "6 25 -22", "0.125 14 0",
        "-1.25 -32 0", "1.5 0.125 0",
        "-2 -22 0", "0.125 20.125 0",
        "-1.25 -12 0", "1.5 0.125 0",
        "5.25 -32 0", "1.5 0.125 0",
        "6 -22 0", "0.125 20.125 0",
        "5.25 -12 0", "1.5 0.125 0",
    ),

    MovingInterior.make(
        PathedInterior.local("chasetrack.dif", 0, initialTargetPosition=0),
        TriggerGotoTarget(position="7 1 0", scale="2 2 1", targetTime=-1),
    ).copies(
        ""
    ),
).add_laps_checkpoint_triggers(
    LapsCheckpointTrigger().copies(
        ("position", "scale"),
        "-44 50 -8", "3 3 1",
        "-2 46 -43", "12 1 20",
        "-10 -116 -44", "24 1 20"
    )
).add(
    LapsCounterTrigger(position="-0.5 5.5 0", scale="7 0.5 10"),

    TimeTravel().copies(
        ("position", "timeBonus"),
        "-9 14.75 0.5", 2000,
        "-19 15 -1.25", 2000,
        "-19 3 -1.25", 2000,
        "-29 3.25 -2.5", 2000,
        "-36.5 69 -16.5", 2000,
        "-34 71 -16.5", 2000,
        "-1 25 -26.25", 5000,
        "13 25 -26.25", 5000,
        "11.25 -12 -23.5", 4000,
        "2.5 -23.25 -23.5", 4000,
        "10 -46 -23.5", 2000,
        "6 -54 -23.5", 2000,
        "2 -58 -23.5", 2000,
        "10 -62 -23.5", 2000,
        "6 -66 -23.5", 2000,
    ),

    Anvil(position="-42.5 49 1"),
    GravityModifier(position="-42.5 51.5 -6", scale="2.5 2.5 2.5"),
    DuctFan(rotation=rot.towards).copies("position", "5 82 -15", "7 82 -15"),
    GravityWellTrigger(position="-7 -146 -43", scale="20 30 30", customPoint="3 -116 -13"),
    Anvil(position="2 -127 -3", rotation=rot.towards),
    GravityModifier(position="2 -124.5 -1", rotation=rot.down),

    FadePlatform(fadeStyle="fade", permanent=1).copies("position", *[(p % 4, p, -0.5) for p in range(-29, -13, 2)]),

).autobounds().set_info(name="Chasetrack [WIP]").write("data/missions_pq/chasetrack.mis")