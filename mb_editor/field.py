class Field:

    def __init__(self, key, value, type):
        self.key, self._value, self.type = key, value, type
        self.value = value

    def __repr__(self):
        return '{} = "{}";'.format(self.key, self.value)

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


    @staticmethod
    def tests():
        f = Field("name", "EdBeacham", str)
        assert (f.key, f.value, f.type) == ("name", "EdBeacham", str)

        from mb_editor.numberlists.vector3d import Vector3D
        f.key, f.type, f.value = "areaCode", Vector3D, [2, 1, 4]
        assert f.value == "2 1 4"

        from mb_editor.objectname import ObjectName
        f.key, f.type, f.value = "client", ObjectName, "RichardSwiney"
        from mb_editor.scriptobject import ScriptObject
        assert f.value == ScriptObject("RichardSwiney")


if __name__ == '__main__':
    Field.tests()
