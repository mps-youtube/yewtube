import collections
import re

from .. import g


Command = collections.namedtuple('Command', 'regex category usage function')

# input types
WORD = r'[^\W\d][-\w\s]{,100}'
RS = r'(?:(?:repeat|shuffle|-[avfw])\s*)'
PL = r'\S*?((?:RD|PL)[-_0-9a-zA-Z]+)\s*'


def command(regex):
    """ Decorator to register an mps-youtube command. """

    def decorator(function):
        cmd = Command(re.compile(regex), None, None, function)
        g.commands.append(cmd)
        return function
    return decorator


# Placed at bottom to deal with cyclic imports
from . import download, search, album_search, misc, config, local_playlist
from . import play, songlist
