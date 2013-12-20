from math import log10

__author__ = 'thanatv'
from linkbudget.linkcalc import SPEED_OF_LIGHT


def wavelength(frequency):
    """
    Returns wavelength in m
    :param frequency: Frequency in GHz
    :return: wavelength in metres
    """
    return SPEED_OF_LIGHT / (frequency * 10 ** 9)


def cn_operation(*args):
        result = 0
        for cn in args:
            result += 1 / (10.0 ** (cn / 10.0))
        return -10 * log10(result)
