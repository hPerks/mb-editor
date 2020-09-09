class ID:
    def __init__(self, arg):
        if isinstance(arg, str):
            self._id = arg
        else:
            self._id = arg.id

    def __repr__(self):
        return f'ID({self.id!r})'

    def __str__(self):
        return self.id

    def __eq__(self, other):
        try:
            return self.id == other.id
        except AttributeError:
            return self.id == other

    @property
    def id(self):
        return self._id

    none = None


ID.none = ID('')

__all__ = ['ID']
