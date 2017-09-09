from mb_editor import *
from mb_editor.utils.lists import drange

from math import sin, cos, radians

TOTAL_PATH_TIME = 64000
NUM_GEMS = 12
GEM_OFFSET = 0.5

mission = LapsMission(
    name="Chasetrack",
    author="hPerks",
    desc="Chase after the gems around the track. Can you get them all in 3 laps?",
    startHelpText="No cheating - you still have to do 3 laps!",
    parTime=150000,
    platinumTime=90000,
    ultimateTime=70000,
    awesomeTime=55000,

    sky=Sky.wave,
).add(
    StartPad(position="8 2 0", rotation="0 0 -1 90"),
    Interior.local("expert/chasetrack.dif"),
    Interior.local("expert/chasetrack_tightrope.dif").copies(
        ("position", "scale"),
        "6 25 -22", "0.125 14 0",
        "-1.25 -32 0", "1.5 0.125 0",
        "-2 -22 0", "0.125 20.125 0",
        "-1.25 -12 0", "1.5 0.125 0",
        "5.25 -32 0", "1.5 0.125 0",
        "6 -22 0", "0.125 20.125 0",
        "5.25 -12 0", "1.5 0.125 0",
    ),

    [
        MovingInterior.make(
            PathedInterior.local("chasetrack.dif", 0, basePosition=(0, y, 0), initialTargetPosition=0),
            TriggerGotoTarget(position="7 1 0", scale="2 2 1", targetTime=-1),
        ).set(path=Path.make_linear(
            (0, y, 0), 62.5 * (40 - y),
            (0, 40, 0), 0,
            (0, -8, 0), 62.5 * (y + 8),
            (0, y, 0)
        ))

        for y in range(-8, 40, 8)
    ],
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

    FadePlatform(fadeStyle="fade", permanent=1).copies("position", [(p % 4, p, -0.5) for p in range(-29, -13, 2)]),

    HelpBubble(triggerRadius=5, displayOnce=1).copies(
        ("position", "rotation", "text"),
        ["-42.5 45 4", rot.up, "Use the Anvil to shoot down the chute!"],
        ["-33 77 -19", rot.down, "The path splits here - follow the gem, if you see one!"],
        ["6 36 -25", rot.down, "Your marble is too heavy to walk on this tightrope!"],
        ["2.5 -130 -7", rot.towards, "You know what to do with this Anvil!"],
    )

)

path = PathNode("path1_up", position="3 9 0", rotation=rot.up).with_path_of_copies(
    "position",
    "0 9 0", "-4 8.75 0", "-8 8.75 0", "-12 9 0", "-24 9 -3", "-26 9 -3", "-42 10 -3", "-44 10 -3",
    "-44 27.75 -3", "-44 27.75 0", "-44 29 1", "-44 30 1", "-43 42 1", "-42.5 46 1", "-42.5 51.5 1"
).path_add(
    PathNode("path1_down", position="-42.5 51.5 -16", rotation=rot.down).with_path_of_copies(
        "position",
        "-42.5 57 -16", "-42 65 -16", "-41.5 73.5 -16", "-41.5 77.5 -16", "-39 77 -16", "-30 77 -16",
        "-13 68 -16", "-10 68 -16", "-4 68 -17.5", "5 68 -17.5", "8 68 -17", "8 66 -17", "8 60 -20",
        "7 54 -23", "6 48 -23", "6 42 -23", "6 38 -22", "6 4 -22", "8 -4 -22", "4.5 -13 -22", "4.5 -17 -22",
        "8.5 -19 -22", "7.5 -23 -22", "7 -26 -22", "6.5 -28 -22", "7 -32 -22", "6 -40 -22", "6 -50 -22",
        "10 -50 -22", "10 -58 -22", "6 -58 -22", "6 -62 -22", "2 -62 -22", "2 -80 -22", "3 -88 -22",
        "3 -92 -22", "3 -100 -24"
    )
).path_add(
    PathNode("path1_well", position="3 -116 -24", rotation=rot.down).with_path_of_copies(
        ("position", "rotation"),
        [
            (
                (3, -116 + 11 * sin(radians(angle)), -13 + 11 * cos(radians(angle))),
                rot.i(angle)
            )
            for angle in drange(180 + 90/16, 270, 90/16)  # angle: 180 to 270, excluding endpoints
        ]
    )
).path_add(
    PathNode("path1_sideways", position="3 -127 -13", rotation=rot.towards).with_path_of_copies(
        "position",
        "3 -127 -13", "3 -127 -11", "2 -127 -3", "2 -127 -1", "2 -124.5 -1"
    )
).path_add(
    PathNode("path1_back_up", position="2 -122 -2", rotation=rot.up).with_path_of_copies(
        "position",
        "2 -122 -2", "2 -118 -2", "3 -110 -2", "2 -102 -2", "2 -101.75 -2.25", "2 -62.25 -2.25", "2 -62 -2",
        "2 -52 -2", "1.5 -46 -4", "2 -42 -4", "2 -40.25 -4", "2 -40.25 -1", "2 -39 0", "2 -32 0", "-2 -32 0",
        "-2 -12 0", "2 -12 0", "2 -10 0", "3 -2 0"
    )
).path_loop()

path2 = path.copy("path2_up").with_path_of_copies(
    ("position", "rotation"),
    [(node.position, node.rotation) for node in path.path()]
).path_loop()

path2.path_add(
    PathNode("path2_down_split", position="-26 77 -16", rotation=rot.down).with_path_of_copies(
        "position",
        "-17 80 -16", "-8 80 -16", "-2 80 -14.5", "1.5 80 -14.5", "6 80 -14", "6 76 -14", "7 70 -17"
    ),
    after=path2.path_node_at_position("-39 77 -16"),
    before=path2.path_node_at_position("8 66 -17"),
).path_add(
    PathNode("path2_back_up_split", position="6 -32 0", rotation=rot.up).with_path_of_copies(
        "position", "6 -12 0"
    ),
    after=path2.path_node_at_position("2 -32 0"),
    before=path2.path_node_at_position("2 -12 0"),
)

path.path_set_time(TOTAL_PATH_TIME)
path2.path_set_time(TOTAL_PATH_TIME)

mission.add(
    path, path2,
    [
        Gem(path=[path, path2][index % 2].path_node_at_time((index + GEM_OFFSET) * TOTAL_PATH_TIME / NUM_GEMS))
        for index in range(NUM_GEMS)
    ],

    PathNode(
        "CameraPath1",
        position="10 -12 10", rotation="0.57 0.2 -0.8 45", timeToNext=5500
    ).with_path_of_copies(
        ("position", "rotation", "timeToNext"),
        "-22 -5 2", "0.65 0.1 -0.75 25", 1,
        "-22 60 -33", "-0.95 -0.1 -0.3 45", 3500,
        "-12 56 -33", "-0.5 0.25 0.8 65", 3000,
        "-10 48 -36", "0 0.2 0.95 145", 1,
        "-1 -92 1", "0 -0.15 0.98 160", 7000,
        "-1 -56 1", "0 -0.15 0.98 160", 1,
    ).path_loop()

).autobounds().write("data/missions_pq/expert/chasetrack.mis")
