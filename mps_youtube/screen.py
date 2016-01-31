import subprocess
import collections
import os
import sys

from . import g, terminalsize, content
from .util import xprint, has_exefile
from .config import Config


mswin = os.name == "nt"

XYTuple = collections.namedtuple('XYTuple', 'width height max_results')


def getxy():
    """ Get terminal size, terminal width and max-results. """
    if g.detectable_size:
        x, y = terminalsize.get_terminal_size()
        max_results = y - 4 if y < 54 else 50
        max_results = 1 if y <= 5 else max_results

    else:
        x, max_results = Config.CONSOLE_WIDTH.get, Config.MAX_RESULTS.get
        y = max_results + 4

    return XYTuple(x, y, max_results)


def update(fill_blank=True):
    """ Display content, show message, blank screen."""
    clear()

    if isinstance(g.content, content.PaginatedContent):
        xprint(g.content.getPage(g.current_page))
        g.rprompt = content.page_msg(g.current_page)
    elif g.content:
        xprint(g.content)
        g.content = False

    if g.message or g.rprompt:
        out = g.message or ''
        blanks = getxy().width - len(out) - len(g.rprompt or '')
        out += ' ' * blanks + (g.rprompt or '')
        xprint(out)

    elif fill_blank:
        xprint("")

    g.message = g.rprompt = False


def clear():
    """Clear all text from screen."""
    if g.no_clear_screen:
        xprint('--\n')
    else:
        xprint('\n' * 200)


def reset_terminal():
    """ Reset terminal control character and modes for non Win OS's. """
    if not mswin:
        subprocess.call(["tset", "-c"])


def writestatus(text, mute=False):
    """ Update status line. """
    if not mute and Config.SHOW_STATUS.get:
        _writeline(text)


def _writeline(text):
    """ Print text on same line. """
    width = getxy().width
    spaces = width - len(text) - 1
    if mswin:
        # Avoids creating new line every time it is run
        # TODO: Figure out why this is needed
        spaces =- 1
    text = text[:width - 3]
    sys.stdout.write(" " + text + (" " * spaces) + "\r")
    sys.stdout.flush()


def msgexit(msg, code=0):
    """ Print a message and exit. """
    xprint(msg)
    sys.exit(code)
