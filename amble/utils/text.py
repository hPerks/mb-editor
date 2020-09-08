import codecs
import re


def unescape(string):
    return re.sub(r'\\[\\\'"abfnrtv]', lambda match: codecs.decode(match.group(0), 'unicode-escape'), string)


def escape(string):
    for char in '\\\'\"abfnrtv':
        string = string.replace(unescape(f'\\{char}'), f'\\{char}')
    return string


def tests():
    assert unescape('hellø \\t\\n \\\"wőrld\\\"') == 'hellø \t\n \"wőrld\"'
    assert escape('hellø \t\n \'wőrld\'') == 'hellø \\t\\n \\\'wőrld\\\''


if __name__ == '__main__':
    tests()


__all__ = ['unescape', 'escape', 'tests']
