from amble.base import ID, Implicit
from amble.staticshapes import StaticShape


class PathNode(StaticShape):
    defaults = dict(
        datablock='PathNode',
        nextnode=Implicit(ID.none),
        timetonext=0,
    )

    def __init__(self, *args, **fields):
        super().__init__(*args, **fields)

    @property
    def distancetonext(self):
        path_next = self.path_next()
        if path_next is None:
            return 0

        return abs((path_next - self).position)

    @property
    def speedtonext(self):
        return self.distancetonext / self.timetonext

    @speedtonext.setter
    def speedtonext(self, value):
        self.timetonext = self.distancetonext / value

    def path_next(self):
        return self.deref('nextnode')

    def path_node_at(self, index):
        if index == 0:
            return self

        path_next = self.path_next()
        if path_next is None:
            return None
        else:
            return path_next.path_node_at(index - 1)

    def path_add(self, node, after=None, before=None):
        if node is None:
            return

        path_next = self.path_next()
        if after == self or (path_next is None and after is None):
            if path_next is not None:
                for friend in path_next.path(before):
                    friend.friends.remove_all()

            self.nextnode = node
            self.friends.add(node)
            node.path_add(before)
            return

        path_next.path_add(node, after, before)

        return self

    def with_path_of_copies(self, keys_tuple, *values_tuples, id='(id)_(i)'):
        copies = self.copies(keys_tuple, *values_tuples, id=id)

        if len(copies) > 0:
            self.nextnode = copies[0]

            for index, copy in enumerate(copies[:-1]):
                copy.nextnode = copies[index + 1]

        return self.with_friends(copies)

    def path(self, end=None):
        path_next = self.path_next()
        if path_next is None or path_next == end:
            return [self]

        return [self] + path_next.path(end=self if end is None else end)

    def path_loop(self):
        return self.path_add(self)

    def path_node_at_time(self, time):
        path_next = self.path_next()
        if path_next is None:
            return None

        if time == 0:
            return self
        elif time < self.timetonext:
            new = self + ((path_next - self) * (time / self.timetonext))
            new.nextnode = self.nextnode
            new.timetonext = self.timetonext - time

            self.nextnode = new
            self.timetonext = time

            self.friends.add(new)
            return new
        else:
            return path_next.path_node_at_time(time - self.timetonext)

    def path_time(self, end=None):
        return sum(node.timetonext for node in self.path(end))

    def path_distance(self, end=None):
        return sum(node.distancetonext for node in self.path(end))

    def path_set_time(self, time, end=None):
        speed = self.path_distance(end) / time
        for node in self.path(end):
            node.speedtonext = speed

    def path_node_at_position(self, position):
        return next(filter(lambda node: node.position == position, self.path()))


    @classmethod
    def show(cls, object):
        return cls(position=object.position)

    @classmethod
    def hide(cls, object):
        return cls(position=object.position - '0 0 32768')


    @staticmethod
    def tests():
        from math import cos, sin, radians
        p = PathNode('circle', position='1 0 0', timetonext=100).with_path_of_copies(
            ('position.x', 'position.y'),
            [(cos(radians(theta)), sin(radians(theta))) for theta in range(90, 360, 90)]
        ).path_loop()

        assert len(p.friends.list) == 3
        assert p.deref('nextnode') == p.path_node_at(1)

        p.path_node_at_time(150)
        assert len(p.friends.list) == 4
        assert p.path_node_at(1).timetonext == 50
        assert abs(p.path_node_at(2).position - '-0.5 0.5 0') < 0.01

        assert p.path_node_at(1).path_node_at_position('1 0 0') == p.path_node_at(5)


if __name__ == '__main__':
    PathNode.tests()

__all__ = ['PathNode']
