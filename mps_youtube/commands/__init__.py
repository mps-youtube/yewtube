import collections
import re

from .. import g
from ..main import completer

Command = collections.namedtuple('Command', 'regex category usage function')

# input types
WORD = r'[^\W\d][-\w\s]{,100}'
RS = r'(?:(?:repeat|shuffle|-[avfw])\s*)'
PL = r'\S*?((?:RD|PL|LL)[-_0-9a-zA-Z]+)\s*'

## @command decorator
##
## The @command decorator takes two arguments, one is a regex that
## is used to match the text command. All following arguments 
## are strings that match the regex that is going to be added to
## tab completion. 
##
## If your command has short-forms, only register the longer
## forms.
## If you use several functions for the same command but different
## arguments, append the completion string on EACH function, not only
## the first time you register it.
def command(regex, *commands):
    """ Decorator to register an mps-youtube command. """
    for command in commands:
        completer.add_cmd(command)
    def decorator(function):
        cmd = Command(re.compile(regex), None, None, function)
        g.commands.append(cmd)
        return function
    return decorator


# Placed at bottom to deal with cyclic imports
from . import download, search, album_search, spotify_playlist, misc, config, local_playlist
from . import play, songlist, generate_playlist, lastfm
