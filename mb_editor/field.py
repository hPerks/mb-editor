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


class Fields:
    def __init__(self, fields_list=None):
        self.list = [] if fields_list is None else fields_list

    def __repr__(self):
        return "\n".join(map(repr, self.list))

    @property
    def dict(self):
        return {
            field.key: field.value for field in self.list
        }

    def field_with_key(self, key):
        return next(filter(lambda field: field.key == key, self.list))

    def get(self, key):
        try:
            return self.field_with_key(key).value
        except StopIteration:
            return None

    def set(self, key, value, field_type=None):
        if "." in key:
            before_dot, after_dot = tuple(key.split(".", 1))
            self.get(before_dot).__setattr__(after_dot, value)
            return

        try:
            self.field_with_key(key).value = value
        except StopIteration:
            self.list.append(Field(key, value, type(value) if field_type is None else field_type))


if __name__ == '__main__':
    Field.tests()
