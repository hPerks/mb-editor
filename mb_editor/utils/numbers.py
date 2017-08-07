def int_or_float(string):
    try:
        return int(string)
    except ValueError:
        return float(string)