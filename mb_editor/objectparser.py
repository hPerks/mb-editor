from mb_editor.scriptobject import ScriptObject

import re


def class_with_name(classname):
    return ScriptObject

def parse_object(string):
    regex = re.compile("new ([a-z_A-Z]+)\(([a-z_A-Z]+)\) {(.*)};", re.DOTALL)

    classname, name, inner_str = re.fullmatch(regex, string).groups()

    obj = class_with_name(classname)(name=name)
    return parse_fields(obj, inner_str)


def parse_fields(obj, inner_str):
    regex = re.compile("([a-z_A-Z]+) = \"(.*)\";\n")

    for match in re.findall(regex, inner_str):
        field_name, field_value_str = match
        obj.set(**{ field_name: field_value_str })
    
    return obj

def tests():
    print(parse_object("new ScriptObject(JojObject) {"
                       "\n   text = \"I have a mustache! :}\";"
                       "\n};"))


if __name__ == '__main__':
    tests()
