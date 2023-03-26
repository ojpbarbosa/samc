from math import log, floor


def human_format(number):
    if number == 0:
        return '0'

    units = ['', 'K', 'M', 'G', 'T', 'P']
    k = 1000.0
    magnitude = int(floor(log(number, k)))

    return ('%.0f%s' if number < 1000 else '%.1f%s') % (number / k**magnitude, units[magnitude])
