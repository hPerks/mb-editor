class Field:

    def __init__(self, key, value, type):
        self.key, self._value, self.type = key, value, type
        self.value = value

    def __repr__(self):
        return '"{}" = "{}";'.format(self.key, self.value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.type(value)

    def addto(self, obj):
        print("{} addto".format(self))
        obj.fields.append(self)
        return self


if __name__ == '__main__':
    f = Field("name", "Icy Tightrope Battlecube", str)
    assert f.key == "name"
    assert f.value == "Icy Tightrope Battlecube"
    assert repr(f) == '"name" = "Icy Tightrope Battlecube";'

    f.key = "position"

    from mb_editor.numberlists.vector3d import Vector3D
    f.type = Vector3D
    f.value = [3, 1, 4]
    assert f.value == "3 1 4"
    assert repr(f) == '"position" = "3 1 4";'

    print(f)
