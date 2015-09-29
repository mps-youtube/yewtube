import collections
import re

from . import g


Command = collections.namedtuple('Command', 'regex category usage function')

# input types
word = r'[^\W\d][-\w\s]{,100}'
rs = r'(?:repeat\s*|shuffle\s*|-a\s*|-v\s*|-f\s*|-w\s*)'
pl = r'\S*((?:RD|PL)[-_0-9a-zA-Z]+)$\S*'


def command(regex):
    """ Decorator to register an mps-youtube command. """

    def decorator(function):
        command = Command(re.compile(regex), None, None, function)
        g.commands.append(command)
        return function
    return decorator
