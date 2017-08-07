from mb_editor.field import Field
from mb_editor.utils.lists import flatlist


class ScriptObject:
    classname = "ScriptObject"

    def __init__(self, name="", **fields):
        self._name = name
        self._fields = []
        self._group = None
        self._friends = []

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
        copy._friends = self._friends
        return copy

    def copies(self, keys_tuple, *values_tuples, name="(name)_(i)"):
        values_tuples = flatlist(*values_tuples)
        if isinstance(keys_tuple, str):
            keys_tuple = tuple([keys_tuple])
            values_tuples = [tuple([values_tuple]) for values_tuple in values_tuples]
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


    @property
    def group(self):
        return self._group

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


    @property
    def friends(self):
        return list(self._friends)

    def with_friend(self, friend):
        copy = self.copy("{name}")
        copy._friends.append(friend)
        return copy


    @staticmethod
    def tests():
        w = ScriptObject("WesleySeeton", catchphrase="do it all over again")
        assert w.catchphrase == "do it all over again"

        e = ScriptObject("EdBeacham", catchphrase="lift the house", rating="A+")
        c = e.copy(catchphrase="i'm beaming up")
        assert (e.catchphrase, c.catchphrase, c.rating) == ("lift the house", "i'm beaming up", "A+")

        cc = c.copies(
            ("satisfaction", "catchphrase"),
            "75", "we no longer care about customer satisfaction",
            ["50", "and my guys no longer care about the joj and doing the joj right"],
            "25", "i'm going to take a sh!t on the house",
            "0",

            name="(name)_dialogue(i)",
        )

        assert len(cc) == 4
        assert cc[0].rating == "A+"
        assert cc[1].name == "EdBeacham_copy_dialogue1"
        assert "!" in cc[2].catchphrase
        assert cc[3].catchphrase == "i'm beaming up"

        we = w.with_friend(e)
        wer = we.with_friend(c)
        assert len(we.friends) == 2

if __name__ == '__main__':
    ScriptObject.tests()
