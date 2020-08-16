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

    rounded = round(float, 6)
    if rounded == int(rounded):
        return repr(int(rounded))
    return repr(rounded)


def mean_of_angles(*angles):
    from amble.numberlists.vector2d import Vector2D
    return sum(Vector2D.i.rotated(angle) for angle in angles).angle


if __name__ == '__main__':
    assert repr_float(0.300000000000004) == '0.3'
    assert repr_float(-0.399999999999999) == '-0.4'
    assert repr_float(1000000.0000000001) == '1000000'
    assert repr_float(103.97999999999999) == '103.98'
    assert repr_float(-0.0) == '0'

    assert repr_float(mean_of_angles(69, 420)) == '64.5'
