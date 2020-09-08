from amble.numberlists.numberlist import NumberList


class Color(NumberList):

    @property
    def r(self):
        return self[0]

    @r.setter
    def r(self, value):
        self[0] = value

    @property
    def g(self):
        return self[1]

    @g.setter
    def g(self, value):
        self[1] = value

    @property
    def b(self):
        return self[2]

    @b.setter
    def b(self, value):
        self[2] = value

    @property
    def a(self):
        return self[3]

    @a.setter
    def a(self, value):
        self[3] = value


__all__ = ['Color']
