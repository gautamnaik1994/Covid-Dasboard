import time
import datetime


def date_to_utc(date):
    return time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple())*1000


def convert_dateformat(date):
    return str(date.strftime('%d/%m/%Y'))


def comma_number(value):
    return "{:,}".format(value)


def color_variant(hex_color, brightness_offset=1):
    """ takes a color like #87c95f and produces a lighter or darker variant """
    if len(hex_color) != 7:
        raise Exception(
            "Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
    rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
    new_rgb_int = [int(hex_value, 16) +
                   brightness_offset for hex_value in rgb_hex]
    # make sure new values are between 0 and 255
    new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int]
    # hex() produces "0x88", we want just "88"
    return "#" + "".join([hex(i)[2:] for i in new_rgb_int])
