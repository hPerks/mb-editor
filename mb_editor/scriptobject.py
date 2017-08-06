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

    def copy(self, name="(name)_copy", **fields):
        return self.__class__(
            name=name.replace("(name)", self.name),
            **fields
        )

    def copies(self, keys_tuple, *values_tuples, name="(name)_(i)"):
        if not isinstance(keys_tuple, tuple):
            keys_tuple = tuple(keys_tuple)
            values_tuples = map(tuple, values_tuples)

        return [
            self.copy(
                name=name.replace("(i)", str(values_tuple_index)),
                **{
                    key: values_tuple[key_index]
                    for key_index, key in enumerate(keys_tuple)
                }
            )
            for values_tuple_index, values_tuple in enumerate(values_tuples)
        ]

if __name__ == '__main__':
    s = ScriptObject(
        name="WesleySeeton",
        catchphrase="do it all over again",
    )

    assert s.catchphrase == "do it all over again"

    s._name = "EdBeacham"
    assert s.name == "EdBeacham"

    copies = s.copies(
        ("some_random_property", "catchphrase"),
        ("0001", "we no longer care about customer satisfaction"),
        ("0002", "and my guys no longer care about the joj and doing the joj right"),
        ("0003", "i'm going to take a sh!t on the house"),
    )

    assert len(copies) == 3
    assert copies[1].name == "EdBeacham_1"
    assert "!" in copies[2].catchphrase

    print(s)
