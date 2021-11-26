from collections import OrderedDict


def merge(dct1, dct2):
    """
    :param dct1: ordered dict by key string value with form key: value or key: [value]
    :param dct2: ordered dict by key string value to be added to first one to be key: [value, new_value]
    :return: an ordered dict by key string value, with the form key: [value1, value2] and paired by the same key as groups
    """
    result = OrderedDict()
    before_size = False
    last_2_value = None

    # we loop over the dict 1 (which has the most indexes) and group data by key
    for key, value in dct1.items():
        if type(value) != list:
            values = [value]
        else:
            values = value

        if not before_size:
            before_size = len(values)

        if key in dct2:
            values.append(dct2[key])
            last_2_value = dct2[key]
        else:
            values.append(last_2_value)
        result[key] = values

    # we loop over the dict 2 to avoid possible missing data
    for key, value in dct2.items():
        if type(value) != list:
            values = [value]
        else:
            values = value

        if key not in dct1:
            values.append([None for _ in range(before_size)] + dct2[key])
            result[key] = values
    return result


def unpack(dct):
    """
    :param dct: dict with the form key: [..values]
    :return: list with the parse for from key: [..values] to [key, *values]
    """
    return [[key, *value] for key, value in dct.items()]
