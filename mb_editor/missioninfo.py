from mb_editor.scriptobject import ScriptObject


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
    )
    