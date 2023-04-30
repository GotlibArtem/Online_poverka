import math


def round_half_up(num, decimals=0) -> int:
    """
    Function for rounding to an integer according to the rules of mathematics

    :param num: number
    :param decimals: rounding format
    :return: rounded number
    """
    multiplier = 10 ** decimals

    return int(math.floor(num * multiplier + 0.5) / multiplier)


def get_value_without_postfix(value: str) -> float:
    """
    Function to convert number with postfix to standard number

    :param value: number with postfix
    :return: number without postfix
    """
    postfixes = {
        'п': 10**-12,
        'н': 10**-9,
        'мк': 10**-6,
        'м': 10**-3,
        'к': 10**3,
        'М': 10**6,
        'Г': 10**9,
        'Т': 10**12
    }
    for postfix, multiplier in postfixes.items():
        if postfix in value:
            value = value.replace(postfix, '')
            value = float(value) * multiplier
            break
    else:
        value = float(value)

    return round(value, 19)


def add_postfix_to_value(value: float, reference_value: str) -> str:
    """
    Function to convert standard number to number with postfix

    :param value: number without postfix
    :param reference_value: reference value for formatting
    :return: number formatted by the reference value
    """
    postfixes = {
        'п': 10**12,
        'н': 10**9,
        'мк': 10**6,
        'м': 10**3,
        'к': 10**-3,
        'М': 10**-6,
        'Г': 10**-9,
        'Т': 10**-12
    }
    for postfix, multiplier in postfixes.items():
        if postfix in reference_value:
            value = round(value * multiplier, 19)
            reference_value = reference_value.replace(postfix, '')
            if '0.' in reference_value:
                num_signs = len(reference_value.replace('0.', ''))
                value = f'{value:.{num_signs}f}'
            else:
                value = round_half_up(value)
            value = str(value) + postfix
            break
    else:
        num_signs = len(reference_value.replace('0.', ''))
        value = f'{value:.{num_signs}f}'

    return value
