from mb_editor.field import Field


class ScriptObject:
    classname = "ScriptObject"

    def __init__(self, name="", **fields):
        self._name = name
        self._fields = []
        self._group = None

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
    def fields(self):
        return {
            field.key: field.value for field in self._fields
        }

    @property
    def name(self):
        return self._name

    @property
    def group(self):
        return self._group

    def inner_str(self):
        return "\n".join(map(repr, self._fields))

    def set(self, **fields):
        for key, value in fields.items():
            self.__setattr__(key, value)
        return self

    def copy(self, name="(name)_copy", **fields):
        copy = self.__class__(
            name="" if self.name == "" else name.replace("(name)", self.name),
            **self.fields
        )
        copy.set(**fields)
        return copy

    def copies(self, keys_tuple, *values_tuples, name="(name)_(i)"):
        if not isinstance(keys_tuple, tuple):
            keys_tuple = tuple(keys_tuple)
            values_tuples = map(tuple, values_tuples)
        elif not isinstance(values_tuples[0], tuple):
            num_complete_tuples = len(values_tuples) // len(keys_tuple)
            values_tuples = [
                values_tuples[index * len(keys_tuple): (index + 1) * len(keys_tuple)]
                for index in range(num_complete_tuples)
            ] + [values_tuples[num_complete_tuples * len(keys_tuple):]]

        return [
            self.copy(
                name=name.replace("(i)", str(values_tuple_index)),
                **{
                    keys_tuple[value_index]: value
                    for value_index, value in enumerate(values_tuple)
                }
            )
            for values_tuple_index, values_tuple in enumerate(values_tuples)
        ]

    def root(self):
        return self if self.group is None else self.group.root()

    def descendants(self):
        return []

    def descendant_named(self, name):
        return next(filter(lambda d: d.name == name, self.descendants()))

    def object_named(self, name):
        return self.root().descendant_named(name)

    def deref(self, field_name):
        return self.object_named(self.fields[field_name].name)


if __name__ == '__main__':
    s = ScriptObject(
        name="WesleySeeton",
        catchphrase="do it all over again",
    )

    assert s.catchphrase == "do it all over again"

    s._name = "EdBeacham"
    assert s.name == "EdBeacham"

    copy = s.copy(catchphrase="lift the house", rating="A+")
    assert copy.fields["catchphrase"] == "lift the house"

    copies = s.copies(
        ("some_random_property", "catchphrase"),
        "0001", "we no longer care about customer satisfaction",
        "0002", "and my guys no longer care about the joj and doing the joj right",
        "0003", "i'm going to take a sh!t on the house",
        "0004"
    )

    assert len(copies) == 4
    assert copies[1].name == "EdBeacham_1"
    assert "!" in copies[2].catchphrase
    assert copies[3].catchphrase == "do it all over again"

    print(*copies, sep="\n")
