from mb_editor.implicit import Implicit
from mb_editor.id import ID
from mb_editor.staticshapes import StaticShape

class PathNode(StaticShape):
    defaults = dict(
        datablock="PathNode",
        nextNode=Implicit(ID.none),
        timeToNext=0  # Implicit(5000) - my rec breaks with or without this, rip
    )

    def __init__(self, *args, **fields):
        super().__init__(*args, **fields)

    @property
    def distanceToNext(self):
        next = self.deref("nextNode")
        if next is None:
            return 0

        return abs((next - self).position)

    @property
    def speedToNext(self):
        return self.distanceToNext / self.timeToNext

    @speedToNext.setter
    def speedToNext(self, value):
        self.timeToNext = self.distanceToNext / value

    def path_next(self):
        return self.deref("nextNode")

    def path_node_at(self, index):
        if index == 0:
            return self

        next = self.path_next()
        if next is None:
            return None
        else:
            return next.path_node_at(index - 1)

    def path_add(self, node, after=None, before=None):
        if node == None:
            return

        next = self.path_next()
        if after == self or (next is None and after is None):
            if next is not None:
                for friend in next.path(before):
                    friend.friends.remove_all()

            self.nextNode = node
            self.friends.add(node)
            node.path_add(before)
            return

        next.path_add(node, after, before)

        return self

    def with_path_of_copies(self, keys_tuple, *values_tuples, id="(id)_(i)"):
        copies = self.copies(keys_tuple, *values_tuples, id=id)

        if len(copies) > 0:
            self.nextNode = copies[0]

            for index, copy in enumerate(copies[:-1]):
                copy.nextNode = copies[index + 1]

        return self.with_friends(copies)

    def path(self, end=None):
        next = self.path_next()
        if next is None or next == end:
            return [self]

        return [self] + next.path(end=self if end is None else end)

    def path_loop(self):
        return self.path_add(self)

    def path_node_at_time(self, time):
        next = self.path_next()
        if next is None:
            return None

        if time == 0:
            return self
        elif time < self.timeToNext:
            new = self + ((next - self) * (time / self.timeToNext))
            new.nextNode = self.nextNode
            new.timeToNext = self.timeToNext - time

            self.nextNode = new
            self.timeToNext = time

            self.friends.add(new)
            return new
        else:
            return next.path_node_at_time(time - self.timeToNext)

    def path_time(self, end=None):
        return sum(node.timeToNext for node in self.path(end))

    def path_distance(self, end=None):
        return sum(node.distanceToNext for node in self.path(end))

    def path_set_time(self, time, end=None):
        speed = self.path_distance(end) / time
        for node in self.path(end):
            node.speedToNext = speed

    def path_node_at_position(self, position):
        return next(filter(lambda node: node.position == position, self.path()))

    @staticmethod
    def tests():
        from math import cos, sin, radians
        p = PathNode("circle", position="1 0 0", timeToNext=100).with_path_of_copies(
            ("position.x", "position.y"),
            [(cos(radians(theta)), sin(radians(theta))) for theta in range(90, 360, 90)]
        ).path_loop()

        assert len(p.friends.list) == 3
        assert p.deref("nextNode") == p.path_node_at(1)

        p.path_node_at_time(150)
        assert len(p.friends.list) == 4
        assert p.path_node_at(1).timeToNext == 50
        assert abs(p.path_node_at(2).position - "-0.5 0.5 0") < 0.01

        assert p.path_node_at(1).path_node_at_position("1 0 0") == p.path_node_at(5)


if __name__ == '__main__':
    PathNode.tests()
