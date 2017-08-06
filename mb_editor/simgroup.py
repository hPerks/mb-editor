from mb_editor.scriptobject import ScriptObject

from functools import reduce
from operator import add


class SimGroup(ScriptObject):
    classname = "SimGroup"

    def __init__(self, *children, **fields):
        super().__init__(**fields)

        self._children = []
        self.add(children)

    @property
    def children(self):
        return list(self._children)

    def add(self, *children):
        if len(children) > 0:
            try:
                self._children += children[0]
            except TypeError:
                self._children += children

            for child in self._children:
                child._group = self

        return self

    def remove(self, *children):
        for child in children:
            self._children.remove(child)
            child._group = None
        return self

    def removeall(self):
        for child in self.children:
            self.remove(child)
        return self

    def descendants(self):
        return self.children + list(reduce(add, [child.descendants() for child in self.children]))

    def inner_str(self):
        return super().inner_str() + "\n\n" + "\n\n".join(map(repr, self.children))


    @staticmethod
    def tests():
        g = SimGroup(
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

        assert len(g.children) == 2
        assert g.children[1].group.mission == "to get the joj done"

        g.remove(g.children[0])
        assert len(g.children) == 1

        g.add(
            ScriptObject(
                name="JudithMiller",
                catchphrase="i would recommend them to anybody",
            )
        )
        g.children[1].speed = "slow"
        assert (g.children[1].catchphrase, g.children[1].speed) == ("i would recommend them to anybody", "slow")

        g.add(
            ScriptObject(
                name="JojIteration",
                rating="A+",
            ).copies(
                ("numTimesAllOverAgain", "satisfaction", "isDone"),
                *[(i, i * 100 / 15, i == 15) for i in range(16)],
            )
        )

        assert len(g.children) == 18
        assert not g.children[-2].isDone
        assert g.children[-1].isDone

        from mb_editor.objectname import ObjectName
        m = SimGroup(
            ScriptObject(
                name="SaintLouis",
                primary_export="drugs",
            ),

            ScriptObject(
                name="noby",
                hometown=ObjectName("SaintLouis")
            ),

            name="MemesGroup",
        ).add(g)

        descendant_names = [descendant.name for descendant in m.descendants()]
        assert all(name in descendant_names for name in ["SaintLouis", "HohSisGroup", "EdBeacham"])
        assert m.descendant_named("JojIteration_15").satisfaction == 100
        assert m.descendant_named("noby").deref("hometown").primary_export == "drugs"


if __name__ == '__main__':
    SimGroup.tests()
