from mb_editor.field import Field


class ScriptObject:
    classname = "ScriptObject"

    def __init__(self, name="", **fields):
        self._name = name
        self._fields = []

        self.set(**self.__defaults())
        self.set(**fields)

    def __fieldwithkey(self, key):
        return next(filter(lambda f: f.key == key, self._fields))

    def __getattr__(self, item):
        return self.__fieldwithkey(item).value

    def __setattr__(self, key, value):
        if key[0] == "_":
            object.__setattr__(self, key, value)
            return

        try:
            self.__fieldwithkey(key).value = value
        except StopIteration:
            self._fields.append(Field(key, value, type(value)))

    def __repr__(self):
        return 'new {classname}({name}) {{\n{fields}\n}};'.format(
            classname=self.classname,
            name=self._name,
            fields=self.inner_str()
        )

    defaults = {}

    @classmethod
    def __defaults(cls):
        try:
            return dict(cls.__bases__[0].__defaults(),
                        **cls.defaults
            )
        except:
            return cls.defaults

    @property
    def name(self):
        return self._name

    def inner_str(self):
        return "\n".join(map(repr, self._fields))

    def set(self, **fields):
        for key, value in fields.items():
            self.__setattr__(key, value)
        return self


if __name__ == '__main__':
    s = ScriptObject(
        name="WesleySeeton",
        catchphrase="do it all over again",
    )

    assert s.catchphrase == "do it all over again"

    s.name = "EdBeacham"
    assert s.name == "EdBeacham"

    print(s)
