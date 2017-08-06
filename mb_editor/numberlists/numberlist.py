from operator import eq, add, sub


class NumberList:

    def __init__(self, *args):
        if len(args) > 1:
            self.values = list(args)
        elif isinstance(args[0], str):
            self.values = list(map(float, args[0].split(" ")))
        else:
            self.values = list(args[0])

    def __getitem__(self, item):
        return self.values[item]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __eq__(self, other):
        return all(map(eq, self, NumberList(other)))

    def __copy__(self):
        return NumberList(self)

    def __repr__(self):
        return " ".join(map(repr, self))

    def __add__(self, other):
        return self.__class__(map(add, self, NumberList(other)))

    def __sub__(self, other):
        return self.__class__(map(sub, self, NumberList(other)))

    def __mul__(self, other):
        return self.__class__(map(lambda x: x * other, self))

    def __truediv__(self, other):
        return self.__class__(map(lambda x: x / other, self))


    @staticmethod
    def tests():
        n = NumberList(3, 1, 4)
        assert n == [3, 1, 4] and n == (3, 1, 4) and n == "3 1 4"

        n[2] = 3
        assert n == "3 1 3"

        from copy import copy
        m = copy(n)
        assert m == n

        m[1] = 4
        assert m != n

        assert m + n == "6 5 6"
        assert m - n == "0 3 0"
        assert n * 2 == "6 2 6"
        assert n / 0.5 == "6 2 6"


if __name__ == '__main__':
    NumberList.tests()
