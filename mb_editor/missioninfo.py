from mb_editor.scriptobject import ScriptObject


class MissionInfo(ScriptObject):
    def __init__(self, **fields):
        super().__init__(name="MissionInfo", **fields)

    defaults = dict(
        name="New Mission",
        game="PQ",
        author="Unknown",
        type="Custom",
        level="1",
        desc="No description set.",
        startHelpText="No start help text.",
    )
    