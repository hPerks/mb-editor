from amble.utils.numbers import int_or_float, str_float, approx_eq

from operator import add, sub, mul


class NumberList:

    def __init__(self, *args, size=None):
        if len(args) != 1:
            self.values = list(args)
        elif isinstance(args[0], str):
            self.values = list(map(int_or_float, args[0].split(' ')))
        elif isinstance(args[0], int) or isinstance(args[0], float):
            self.values = [args[0]]
        else:
            self.values = list(args[0])

        if size is not None:
            for i in range(len(self.values), size):
                self.values.append(0)

    def __getitem__(self, item):
        return self.values[item]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __len__(self):
        return len(self.values)

    def __eq__(self, other):
        return all(map(approx_eq, self, NumberList(other)))

    def __copy__(self):
        return NumberList(self)

    def __repr__(self):
        args_string = ', '.join(map(str_float, self))
        return f'{self.__class__.__name__}({args_string})'

    def __str__(self):
        return ' '.join(map(str_float, self))

    def map(self, function, *others):
        return self.__class__(map(function, *([self] + [NumberList(other, size=len(self.values)) for other in others])))

    def __add__(self, other):
        return self.map(add, other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self.map(sub, other)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.map(lambda x: x * other)
        other = NumberList(other)
        return self.__class__(self[i] * other[i] for i in range(len(self.values)))

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.map(lambda x: x / other)
        other = NumberList(other)
        return self.__class__(self[i] / other[i] for i in range(len(self.values)))

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

    def dot(self, other):
        other = NumberList(other)
        return sum(map(mul, self, other))

    def is_perpendicular(self, other):
        return approx_eq(self.dot(other), 0)

    def is_parallel(self, other):
        return self.is_facing(other) or (-self).is_facing(other)

    def is_facing(self, other):
        return self.normalized() == NumberList(other).normalized()

    def append(self, item):
        return self.__class__(list(self) + [item])

    def to_basis(self, *basis):
        basis = [NumberList(basis_vector) for basis_vector in basis]
        rows = [NumberList(row).append(self[i]) for i, row in enumerate(zip(*basis))]
        for i in range(len(rows)):
            if approx_eq(rows[i][i], 0):
                rows[i] += next(row for row in rows[i + 1:] if not approx_eq(row[i], 0))
            rows[i] /= rows[i][i]
            for j in range(len(rows)):
                if j != i:
                    rows[j] -= rows[i] * rows[j][i]
        return self.__class__(row[-1] for row in rows)

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
        assert '2 0 3' * m == '6 0 9'
        assert m + 2 == '5 4 3'
        assert m.dot('-2 3 -2') == 0

        assert m.to_basis('0 1 2', '1 4 -1', '-1 1 0') == '2 1 -2'


if __name__ == '__main__':
    NumberList.tests()


__all__ = ['NumberList']
