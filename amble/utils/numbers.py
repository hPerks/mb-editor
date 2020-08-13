def int_or_float(string):
    try:
        return int(string)
    except ValueError:
        try:
            return float(string)
        except ValueError:
            return 0


def approx_eq(left, right):
    return abs(left - right) < 0.000000000001


def approx_div(dividend, divisor):
    return approx_eq(dividend % divisor, 0) or approx_eq(dividend % divisor, divisor)


def repr_float(float):
    if approx_eq(float, 0):
        return '0'

    r = repr(float)
    if r.startswith('-'):
        return '-' + repr_float(-float)
    elif r.endswith('.0'):
        return repr(float)[:-2]
    elif '.' in r and (r[:-1].endswith('99999') or r[:-1].endswith('00000')):
        decimal_places = 0
        while not ('.99999' in repr(float) or '.00000' in repr(float) or repr(float).endswith('.0')):
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
    assert repr_float(-0.399999999999999) == '-0.4'
    assert repr_float(1000000.0000000001) == '1000000'
    assert repr_float(103.97999999999999) == '103.98'
    assert repr_float(-0.0) == '0'
