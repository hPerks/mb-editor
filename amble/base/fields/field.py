import amble
from amble.base.fields.implicit import Implicit
from amble.utils.text import escape


class Field:
    def __init__(self, key, value, type):
        self.key = key

        self.implicit_default = None
        if type == Implicit:
            self.type = value.type
        else:
            self.type = type

        self.value = value

    def __str__(self):
        return f'{self.key} = "{escape(self.value) if self.type == str else self.value}";'

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value.lower()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if type(value) == Implicit:
            self.type = value.type
            self._value = value.type(value.value)
            self.implicit_default = self._value
        else:
            if isinstance(value, amble.ScriptObject):
                self._value = value
            else:
                self._value = self.type(value)

    def is_explicit(self):
        return (
            (self.value is not None and self.implicit_default is None)
            or (self.value is None and self.implicit_default is not None)
            or self.value != self.implicit_default
        ) and not isinstance(self.value, amble.ScriptObject)


    @staticmethod
    def tests():
        f = Field('name', 'EdBeacham', str)
        assert (f.key, f.value, f.type) == ('name', 'EdBeacham', str)

        from amble import Vector3D
        f.key, f.type, f.value = 'areaCode', Vector3D, [2, 1, 4]
        assert f.key == 'areacode'
        assert f.value == '2 1 4'

        from amble import ID
        f.key, f.type, f.value = 'client', ID, 'RichardSwiney'
        assert f.value == amble.ScriptObject('RichardSwiney')

        g = Field('timeBonus', Implicit(5000), Implicit)
        assert (g.value, g.type, g.implicit_default) == (5000, int, 5000)

        g.value = Implicit(3000)
        assert (g.value, g.type, g.implicit_default) == (3000, int, 3000)

        g.value = 1000
        assert (g.value, g.type, g.implicit_default) == (1000, int, 3000)


if __name__ == '__main__':
    Field.tests()

__all__ = ['Field']
