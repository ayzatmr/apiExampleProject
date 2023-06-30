import decimal
import logging
import math

import requests

from utils.decorator import func_once

logger = logging.getLogger(__name__)


def join_url_paths(*args):
    """Joins given arguments into a url. Trailing but not leading slashes are stripped for each argument. """
    return "/".join(map(lambda x: str(x).rstrip('/'), args))


"""Custom rounder of value, because there are can be different behaviour in Java/Python"""


def round_value(number, decimals=1, method="half"):
    multiplier = 10 ** decimals
    if method == "down":
        return math.floor(number * multiplier) / multiplier
    elif method == "up":
        return math.ceil(number * multiplier) / multiplier
    # wrapper for java half_down. (python makes up starting from 5)
    elif method == "half":
        val = decimal.Decimal(number).quantize(decimal.Decimal('.001'), rounding=decimal.ROUND_HALF_DOWN)
        first_val, second_val = str(val).split('.')
        if second_val[2] == '5':
            second_val = second_val[0:2]
            val = float(first_val + '.' + second_val)
        else:
            val = float(decimal.Decimal(number).quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_HALF_DOWN))
        return val
    else:
        raise ValueError('Invalid rounding method')


""" create http session for tests """


@func_once
def my_session():
    return requests.Session()
