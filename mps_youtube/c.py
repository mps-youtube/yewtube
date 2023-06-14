""" Module for holding colour code values. """

import os
import re
import sys

if sys.stdout.isatty():
    white = "\x1b[%sm" % 0
    ul = "\x1b[%sm" * 2 % (2, 4)

    if not os.getenv('NO_COLOR'):
        ul += "\x1b[%33m"

    cols = ["\x1b[%sm" % n for n in range(91, 96)]
    red, green, yellow, blue, pink = [""]*5 if os.getenv('NO_COLOR') else cols
else:
    ul = red = green = yellow = blue = pink = white = ""

r, g, y, b, p, w = red, green, yellow, blue, pink, white

ansirx = re.compile(r'\x1b\[\d*m', re.UNICODE)

def c(colour, text):
    """ Return coloured text. """
    colours = {'r': r, 'g': g, 'y': y, 'b':b, 'p':p}
    return colours[colour] + text + w

def charcount(s):
    """ Return number of characters in string, with ANSI color codes excluded. """
    return len(ansirx.sub('', s))
