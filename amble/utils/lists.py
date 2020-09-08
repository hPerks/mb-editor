from functools import reduce
from operator import add


def flatlist(*args):
    def __flatlist(lst):
        return [lst] if not isinstance(lst, list) else list(reduce(add, map(__flatlist, lst), []))
    return list(reduce(add, map(__flatlist, args), []))


def is_list_of_tuples(lst):
    return all(isinstance(item, tuple) for item in lst)


def drange(*args, include_end=False):
    if len(args) == 3:
        start, stop, step = tuple(args)
    elif len(args) == 2:
        start, stop, step = args[0], args[1], 1.0
    elif len(args) == 1:
        start, stop, step = 0.0, args[0], 1.0
    else:
        raise StopIteration

    r = start
    while r < stop - 0.000000001:
        yield r
        r += step

    if include_end and r < stop + 0.000000001:
        yield r


def tests():
    f = flatlist([[4, 2, [0]], 6, []], 9)
    assert flatlist(f) == [4, 2, 0, 6, 9]

    assert is_list_of_tuples([(1, 3), (3, 7)])
    assert not is_list_of_tuples([(4, 2, 0), 6, (9,)])


if __name__ == '__main__':
    tests()

__all__ = ['drange', 'flatlist', 'is_list_of_tuples', 'tests']
