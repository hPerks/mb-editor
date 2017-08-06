from mb_editor.scriptobject import ScriptObject


class SimGroup(ScriptObject):
    classname = "SimGroup"

    def __init__(self, *children, **fields):
        super().__init__(**fields)

        self._children = list(children)

    @property
    def children(self):
        return list(self._children)

    def add(self, *children):
        try:
            self._children += children[0]
        except TypeError:
            self._children += children

        return self

    def remove(self, *children):
        for child in children:
            self._children.remove(child)
        return self

    def inner_str(self):
        return super().inner_str() + "\n\n" + "\n\n".join(map(repr, self.children))


if __name__ == '__main__':
    s = SimGroup(
        ScriptObject(
            name="WesleySeeton",
            catchphrase="do it all over again",
        ),

        ScriptObject(
            name="EdBeacham",
            catchphrase="take a shit on the house",
        ),

        name="HohSisGroup",
        mission="to get the joj done",
    )
    assert len(s.children) == 2

    s.remove(s.children[0])
    assert len(s.children) == 1

    s.add(
        ScriptObject(
            name="JudithMiller",
            catchphrase="i would recommend them to anybody"
        )
    )
    assert s.children[1].catchphrase == "i would recommend them to anybody"

    s.add(
        ScriptObject(
            name="JojIteration",
            rating="A+",
        ).copies(
            ("numTimesAllOverAgain", "percentSatisfaction", "isDone"),
            *[(i, float(i) * 100 / 15, i == 15) for i in range(16)]
        )
    )

    assert len(s.children) == 18
    assert not s.children[-2].isDone
    assert s.children[-1].isDone

    print(s)