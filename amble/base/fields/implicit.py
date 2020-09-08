typeof = type


class Implicit:
    def __init__(self, value, type=None):
        self.value = value
        self.type = typeof(value) if type is None else type

    def __str__(self):
        return str(self.value)


__all__ = ['Implicit']
