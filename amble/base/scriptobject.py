import re
from textwrap import indent

from amble.base.fields import Fields
from amble.base.friends import Friends
from amble.utils.lists import flatlist, is_list_of_tuples
from amble.utils.text import unescape


class ScriptObject:
    classname = 'ScriptObject'

    def __init__(self, id='', **fields):
        self._id = id
        self._fields = Fields()
        self._group = None
        self._friends = Friends(self)

        self.set(**self.all_defaults())
        self.set(**fields)

    def __getattr__(self, item):
        return self.fields.get(item)

    def __setattr__(self, key, value):
        if key[0] == '_' or isinstance(getattr(self.__class__, key, None), property):
            object.__setattr__(self, key, value)
            return

        self.fields.set(key, value)

    def __repr__(self):
        defaults = self.all_defaults()

        id_string = repr(self.id) if self.id else ''
        fields_string = ', '.join(
            f'{field.key}={field.value!r}'
            for field in self.fields.list
            if defaults.get(field.key, None) != field.value
        )
        params_string = ', '.join(
            ([id_string] if id_string else []) +
            ([fields_string] if fields_string else [])
        )

        return f'{self.__class__.__name__}({params_string})'

    def __str__(self):
        inner = indent(self.inner_str(), '   ')
        return f'new {self.classname}({self.id}) {{\n{inner}\n}};'

    defaults = {}

    @classmethod
    def all_defaults(cls):
        try:
            return dict(
                cls.__bases__[0].all_defaults(),
                **cls.defaults
            )
        except AttributeError:
            return cls.defaults

    @property
    def fields(self):
        return self._fields

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def written_fields(self):
        return self.fields

    def inner_repr(self):
        defaults = self.all_defaults()
        return ', '.join(
            f'{field.key}={field.value!r}'
            for field in self.fields.list
            if defaults.get(field.key, None) != field.value
        )

    def inner_str(self):
        return str(self.written_fields())

    def set(self, **fields):
        for key, value in fields.items():
            self.__setattr__(key, value)
        return self

    def merge(self, object):
        self.set(**object.fields.dict)


    def copy(self, id='(id)_copy', **fields):
        copy = self.__class__(
            id='' if self.id == '' else id.replace('(id)', self.id),
            **self.fields.dict
        )
        copy.set(**fields)
        return copy

    def copies(self, keys_tuple, *values_tuples, id='(id)_(i)'):
        values_tuples = flatlist(*values_tuples)

        if isinstance(keys_tuple, str):
            keys_tuple = tuple([keys_tuple])
            values_tuples = [tuple([values_tuple]) for values_tuple in values_tuples]

        elif not is_list_of_tuples(values_tuples):
            tuple_size = len(keys_tuple)
            num_complete_tuples = len(values_tuples) // tuple_size

            complete_tuples = [
                values_tuples[index * tuple_size: (index + 1) * tuple_size]
                for index in range(num_complete_tuples)
            ]
            if len(values_tuples) > num_complete_tuples * tuple_size:
                values_tuples = complete_tuples + [values_tuples[num_complete_tuples * tuple_size:]]
            else:
                values_tuples = complete_tuples

        return [
            self.copy(
                id=id.replace('(i)', str(values_tuple_index)),
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

    def descendant(self, id):
        if id == '':
            return None

        return next(filter(lambda d: d.id == id, self.descendants()), None)

    def object(self, id):
        return self.root().descendant(id) or self.friends[id]

    def deref(self, field_name):
        return self.object(self.fields.get(field_name).id)


    @property
    def friends(self):
        return self._friends

    def with_friends(self, *friends):
        self.friends.add(*friends)
        return self

    def with_copies(self, keys_tuple, *values_tuples, id='(id)_(i)'):
        return self.with_friends(self.copies(keys_tuple, *values_tuples, id=id))


    @classmethod
    def subclasses_with(cls, classname, **defaults):
        classes = []

        if cls.classname.lower() == classname.lower():
            class_defaults = cls.all_defaults()
            if all(
                (value is None) or (key in class_defaults and class_defaults[key].lower() == value.lower())
                for key, value in defaults.items()
            ):
                classes.append(cls)

        classes += flatlist([subclass.subclasses_with(classname, **defaults) for subclass in cls.__subclasses__()])
        return classes


    RE_OBJECT_BEGIN = re.compile(r'new \s*(?P<classname>[a-z_A-Z0-9]+)\s*\(\s*(?P<id>[a-z_A-Z0-9]*)\s*\)\s*{')
    RE_OBJECT_END = re.compile(r'}\s*;')
    RE_FIELD = re.compile(r'(?P<name>[a-z_A-Z0-9]+)\s*=\s*\"(?P<value>(?:(?:[^\"])|(?:\\\"))*(?:(?:[^\\])|(?:\\\\)))\"\s*;')

    @classmethod
    def from_string(cls, string):
        string = string.replace('$usermods @ "', '"~')

        children = []
        fields = Fields()

        stack = []

        matches = sorted(
            list(re.finditer(cls.RE_OBJECT_BEGIN, string)) +
            list(re.finditer(cls.RE_OBJECT_END, string)) +
            list(re.finditer(cls.RE_FIELD, string)),

            key=lambda m: m.start()
        )

        for match in matches:
            pos = match.start()

            if match.re == cls.RE_OBJECT_BEGIN:
                stack.append(pos)
            elif match.re == cls.RE_OBJECT_END:
                begin_pos = stack.pop()
                if len(stack) == 1:
                    children.append(ScriptObject.from_string(string[begin_pos:pos + 1]))
            elif match.re == cls.RE_FIELD:
                if len(stack) == 1:
                    field_name, field_value_str = match.groups()
                    fields.set(field_name.lower(), unescape(field_value_str))

        classname, id = matches[0].groups()

        try:
            subclass = cls.subclasses_with(classname, id=id)[0]
        except IndexError:
            try:
                subclass = cls.subclasses_with(classname, datablock=fields.get('datablock'))[0]
            except IndexError:
                return ScriptObject(id=id, **fields.dict)

        obj = subclass(id=id, **fields.dict)

        if len(children) > 0:
            obj.add(children)

        return obj


    @staticmethod
    def tests():
        w = ScriptObject('WesleySeeton', catchphrase="do it all over again")
        assert w.catchphrase == "do it all over again"

        e = ScriptObject('EdBeacham', catchphrase="lift the house", rating='A+')
        c = e.copy(catchphrase="i'm beaming up")
        assert (e.catchphrase, c.catchphrase, c.rating) == ("lift the house", "i'm beaming up", 'A+')

        cc = c.copies(
            ('satisfaction', 'catchphrase'),
            75, "we no longer care about customer satisfaction",
            [50, "and my guys no longer care about the joj and doing the joj right"],
            25, "i'm going to take a sh!t on the house",
            0,

            id='(id)_dialogue(i)',
        )

        assert len(cc) == 4
        assert cc[0].rating == 'A+'
        assert cc[1].id == 'EdBeacham_copy_dialogue1'
        assert '!' in cc[2].catchphrase
        assert (cc[3].satisfaction, cc[3].catchphrase) == (0, "i'm beaming up")

        we = w.with_friends(e)
        wer = w.with_friends(c)
        assert len(we.friends.list) == len(wer.friends.list) == 2


if __name__ == '__main__':
    ScriptObject.tests()

__all__ = ['ScriptObject']
