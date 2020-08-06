def int_or_float(string):
    try:
        return int(string)
    except ValueError:
        try:
            return float(string)
        except ValueError:
            return 0


def mod(x, m):
    return ((x % m) + m) % m


def repr_float(float):
    bad_decimals = ['999996', '999997', '999998', '999999', '000001', '000002', '000003', '000004']

    if repr(float) == '-0.0':
        return '0'
    elif repr(float).endswith('.0'):
        return repr(float)[:-2]
    elif '.' in repr(float) and any(repr(float).endswith(decimal) for decimal in bad_decimals):
        decimal_places = 0
        while not any('.' + decimal in repr(float) for decimal in bad_decimals):
            float *= 10
            decimal_places += 1
        digits = repr(int(round(float)))
        if decimal_places == 0:
            return digits
        else:
            whole_digits, decimal_digits = digits[:-decimal_places], digits[-decimal_places:].rstrip('0')
            if whole_digits == '':
                return '0.' + decimal_digits
            elif decimal_digits == '':
                return whole_digits
            else:
                return whole_digits + '.' + decimal_digits
    else:
        return repr(float)


if __name__ == '__main__':
    assert repr_float(0.300000000000004) == '0.3'
    assert repr_float(0.399999999999999) == '0.4'
    assert repr_float(1000000.0000000001) == '1000000'
