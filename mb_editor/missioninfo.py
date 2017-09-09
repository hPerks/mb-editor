from mb_editor.scriptobject import ScriptObject
from mb_editor.implicit import Implicit


class MissionInfo(ScriptObject):
    defaults = dict(
        id="MissionInfo",
        name="New Mission",
        game="PQ",
        author="Unknown",
        type="Custom",
        level="1",
        desc="No description set.",
        startHelpText="No start help text.",

        music=Implicit(""),
    )
