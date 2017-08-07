from functools import reduce
from operator import add


def __flatlist(l):
    return [l] if not isinstance(l, list) else list(reduce(add, map(__flatlist, l), []))


def flatlist(*args):
    return list(reduce(add, map(__flatlist, args), []))


def tests():
    f = flatlist([[4, 2, [0]], 6, []], 9)
    print(f)
    assert flatlist(f) == [4, 2, 0, 6, 9]


if __name__ == '__main__':
    tests()
