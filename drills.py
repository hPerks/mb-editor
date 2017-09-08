from mb_editor import *

mission = NormalMission()

mission.info.set(
    name="Drills",
    author="hPerks",
)

mission.add(
    StartPad(position="-150 -3 0", rotation=rot.k(90)),
    Interior.local("custom/drills.dif"),
)

mission.autobounds(horizontal_margin=200).write("data/missions_pq/custom/drills.mis")
