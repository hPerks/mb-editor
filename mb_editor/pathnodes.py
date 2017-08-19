from mb_editor.objectname import ObjectName
from mb_editor.staticshapes import StaticShape

class PathNode(StaticShape):
    defaults = dict(
        datablock="PathNode",
        nextNode=ObjectName.none,
        timeToNext=0,
    )

    def chain_of_copies(self, keys_tuple, *values_tuples, name="(name)_(i)", loop=True):
        copies = self.copies(keys_tuple, *values_tuples, name=name)

        for index, copy in enumerate(copies[:-1]):
            copy.nextNode = copies[index + 1]

        if loop:
            copies[-1].nextNode = copies[0]

        return copies

    def get_chain(self, end=None):
        next = self.deref("nextNode")
        if next is None or next == end:
            return [self]

        return [self] + next.get_chain(end=self if end is None else end)

    def split_chain(self, time):
        next = self.deref("nextNode")
        if next is None:
            return None

        if time < self.timeToNext:
            new = self + ((next - self) * (time / self.timeToNext))
            new.nextNode = self.nextNode
            new.timeToNext = self.timeToNext - time

            self.nextNode = new
            self.timeToNext = time

            if self.group is not None:
                self.group.add(new)
            return new
        else:
            return next.split_chain(time - self.timeToNext)


    @staticmethod
    def tests():
        from math import cos, sin, radians
        cc = PathNode("circle", timeToNext=100).chain_of_copies(
            ("position.x", "position.y"),
            [(cos(radians(theta)), sin(radians(theta))) for theta in range(0, 360, 90)]
        )

        assert len(cc) == 4
        assert cc[0].nextNode == cc[1]

        from mb_editor.simgroup import SimGroup
        SimGroup(cc)

        cc[0].split_chain(150)
        cc = cc[0].get_chain()
        assert len(cc) == 5
        assert cc[1].timeToNext == 50
        assert abs(cc[2].position - "-0.5 0.5 0") < 0.01



if __name__ == '__main__':
    PathNode.tests()
