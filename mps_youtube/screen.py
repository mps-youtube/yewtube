import subprocess
import os
import sys

from . import g, content, config
from .util import xprint, getxy


mswin = os.name == "nt"


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
    if not mute and config.SHOW_STATUS.get:
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
