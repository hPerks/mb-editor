from amble.utils.numbers import int_or_float, repr_float

from operator import eq, add, sub


class NumberList:

    def __init__(self, *args):
        if len(args) > 1 or len(args) == 0:
            self.values = list(args)
        elif isinstance(args[0], str):
            self.values = list(map(int_or_float, args[0].split(' ')))
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
        return ' '.join(map(repr_float, self))

    def map(self, function, *others):
        return self.__class__(map(function, *([self] + [NumberList(other) for other in others])))

    def __add__(self, other):
        return self.map(add, other)

    def __sub__(self, other):
        return self.map(sub, other)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.map(lambda x: x * other)
        other = NumberList(other)
        return self.__class__(self[i] * other[i] for i in range(len(self.values)))

    def __truediv__(self, other):
        return self.map(lambda x: x / other)

    def __pow__(self, power, modulo=None):
        return self.map(lambda x: pow(x, power, modulo))

    def __neg__(self):
        return self.map(lambda x: -x)

    def __abs__(self):
        return pow(sum(map(lambda i: i ** 2, self)), 0.5)

    def normalized(self):
        try:
            return self / abs(self)
        except ZeroDivisionError:
            return self


    @staticmethod
    def tests():
        n = NumberList(3, 1, 4)
        assert n == [3, 1, 4] and n == (3, 1, 4) and n == '3 1 4'

        n[2] = 3
        assert n == '3 1 3'

        from copy import copy
        m = copy(n)
        assert m == n

        m[1] = 4
        assert m != n

        assert m + n == '6 5 6'
        assert m - n == '0 3 0'
        assert n * 2 == '6 2 6'
        assert n / 0.5 == '6 2 6'
        assert m * '2 0 3' == '6 0 9'


if __name__ == '__main__':
    NumberList.tests()
