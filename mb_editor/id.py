class ID:

    def __init__(self, arg):
        if isinstance(arg, str):
            self._id = arg
        else:
            self._id = arg.id

    @property
    def id(self):
        return self._id

    def __repr__(self):
        return self.id

    def __eq__(self, other):
        try:
            return self.id == other.id
        except AttributeError:
            return self.id == other

ID.none = ID("")
