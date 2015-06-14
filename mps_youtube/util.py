# python2 compatibility (for landscape)
from __future__ import print_function

import os
import re
import sys
import subprocess
import logging

from . import g, c


mswin = os.name == "nt"
not_utf8_environment = mswin or "UTF-8" not in os.environ.get("LANG", "")
 

def has_exefile(filename):
    """ Check whether file exists in path and is executable.

    Return path to file or False if not found
    """
    paths = [os.getcwd()] + os.environ.get("PATH", '').split(os.pathsep)
    paths = [i for i in paths if i]
    dbg("searching path for %s", filename)

    for path in paths:
        exepath = os.path.join(path, filename)

        if os.path.isfile(exepath):
            if os.access(exepath, os.X_OK):
                dbg("found at %s", exepath)
                return exepath

    return False


def get_mpv_version(exename):
    """ Get version of mpv as 3-tuple. """
    o = subprocess.check_output([exename, "--version"]).decode()
    re_ver = re.compile(r"%s (\d+)\.(\d+)\.(\d+)" % exename)

    for line in o.split("\n"):
        m = re_ver.match(line)

        if m:
            v = tuple(map(int, m.groups()))
            dbg("%s version %s.%s.%s detected", exename, *v)
            return v

    dbg("%sFailed to detect mpv version%s", c.r, c.w)
    return -1, 0, 0


def dbg(*args):
    """Emit a debug message."""
    # Uses xenc to deal with UnicodeEncodeError when writing to terminal
    logging.debug(xenc(i) for i in args)


def utf8_replace(txt):
    """ Replace unsupported characters in unicode string, returns unicode. """
    sse = sys.stdout.encoding
    txt = txt.encode(sse, "replace").decode(sse)
    return txt


def xenc(stuff):
    """ Replace unsupported characters. """
    if sys.stdout.isatty():
        return utf8_replace(stuff) if not_utf8_environment else stuff

    else:
        return stuff.encode("utf8", errors="replace")


def xprint(stuff, end=None):
    """ Compatible print. """
    print(xenc(stuff), end=end)


def mswinfn(filename):
    """ Fix filename for Windows. """
    if mswin:
        filename = utf8_replace(filename) if not_utf8_environment else filename
        allowed = re.compile(r'[^\\/?*$\'"%&:<>|]')
        filename = "".join(x if allowed.match(x) else "_" for x in filename)

    return filename


def set_window_title(title):
    """ Set terminal window title. """
    if mswin:
        os.system(xenc("title " + title))
    else:
        sys.stdout.write(xenc('\x1b]2;' + title + '\x07'))


def clear_screen():
    """Clear all text from screen."""
    if g.no_clear_screen:
        xprint('--\n')
    elif mswin:
        os.system('cls')
    elif has_exefile('tput'):
        subprocess.call(['tput', 'reset'])
    else:
        xprint('\n' * 200)
