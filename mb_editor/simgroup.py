from mb_editor.scriptobject import ScriptObject
from mb_editor.utils.lists import flatlist


class SimGroup(ScriptObject):
    classname = "SimGroup"

    def __init__(self, *children, **fields):
        self._children = []
        super().__init__(**fields)
        self.add(*children)

    @property
    def children(self):
        return list(self._children)

    def add(self, *children):
        for child in flatlist(*children):
            for key, value in self.fields.dict.items():
                if isinstance(child, type(value)) and child != value:
                    self.__setattr__(key, child)
                    break

            self._children.append(child)
            child._group = self

            for friend in child.friends.list:
                if friend.group != self:
                    self._children.append(friend)
                    friend._group = self

        return self

    def remove(self, *children):
        for child in flatlist(*children):
            self._children.remove(child)
            child._group = None

            for friend in child.friends.list:
                if friend.group == self:
                    self._children.remove(friend)
                    friend._group = None

        return self

    def remove_all(self):
        self.remove(self.children)
        return self

    def descendants(self):
        return self.children + flatlist([child.descendants() for child in self.children])

    def inner_str(self):
        return super().inner_str() + "\n" + "\n\n".join(map(repr, self.children))


    def __setattr__(self, key, value):
        super().__setattr__(key, value)

        if key[0] == "_":
            return

        if isinstance(value, ScriptObject):
            for child in self.children:
                if isinstance(value, type(child)):
                    self.remove(child)
            self.add(value)


    @staticmethod
    def tests():
        g = SimGroup(
            ScriptObject(
                "WesleySeeton",
                catchphrase="do it all over again",
            ),

            ScriptObject(
                "EdBeacham",
                catchphrase="take a shit on the house",
            ),

            id="HohSisGroup",
            mission="to get the joj done",
        )

        assert len(g.children) == 2
        assert g.children[1].group.mission == "to get the joj done"

        g.remove(g.children[0])
        assert len(g.children) == 1

        g.add([
            ScriptObject(
                "JudithMiller",
                catchphrase="i would recommend them to anybody",
            )
        ])
        g.children[1].speed = "slow"
        assert (g.children[1].catchphrase, g.children[1].speed) == ("i would recommend them to anybody", "slow")

        g.add(
            ScriptObject(
                "JojIteration",
                rating="A+",
            ).copies(
                ("numTimesAllOverAgain", "satisfaction", "isDone"),
                *[(i, i * 100 / 15, i == 15) for i in range(16)],
            )
        )

        assert len(g.children) == 18
        assert not g.children[-2].isDone
        assert g.children[-1].isDone

        from mb_editor.id import ID

        class Person(ScriptObject):
            defaults = dict(
                hometown=ID.none
            )

        m = SimGroup(
            [ScriptObject(
                "SaintLouis",
                primary_export="drugs",
            )],

            Person(
                "noby",
                hometown="SaintLouis"
            ),

            id="MemesGroup"
        ).add(g)

        descendant_ids = [descendant.id for descendant in m.descendants()]
        assert all(id in descendant_ids for id in ["SaintLouis", "HohSisGroup", "EdBeacham"])
        assert m.descendant("JojIteration_15").satisfaction == 100
        assert m.descendant("noby").deref("hometown").primary_export == "drugs"


if __name__ == '__main__':
    SimGroup.tests()
