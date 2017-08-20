from functools import reduce
from operator import add


def __flatlist(l):
    return [l] if not isinstance(l, list) else list(reduce(add, map(__flatlist, l), []))


def flatlist(*args):
    return list(reduce(add, map(__flatlist, args), []))


def is_list_of_tuples(list):
    return all(isinstance(item, tuple) for item in list)


def drange(*args):
    if len(args) == 3:
        start, stop, step = tuple(args)
    elif len(args) == 2:
        start, stop, step = args[0], args[1], 1.0
    elif len(args) == 1:
        start, stop, step = 0.0, args[0], 1.0

    r = start
    while r < stop - 0.000000001:
        yield r
        r += step


def tests():
    f = flatlist([[4, 2, [0]], 6, []], 9)
    assert flatlist(f) == [4, 2, 0, 6, 9]

    assert is_list_of_tuples([(1, 3), (3, 7)])
    assert not is_list_of_tuples([(4, 2, 0), 6, (9)])


if __name__ == '__main__':
    tests()
