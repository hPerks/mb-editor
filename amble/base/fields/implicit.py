typeof = type


class Implicit:
    def __init__(self, value, type=None):
        self.type = typeof(value) if type is None else type
        self.value = self.type(value)

    def __repr__(self):
        return f'Implicit({self.value!r}, {self.type.__name__})'

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other


__all__ = ['Implicit']
