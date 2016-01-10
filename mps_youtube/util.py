# python2 compatibility (for landscape)
from __future__ import print_function

import os
import re
import sys
import ctypes
import subprocess
import logging
import time

import pafy

from . import g, c


mswin = os.name == "nt"
not_utf8_environment = mswin or "UTF-8" not in sys.stdout.encoding
 

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
    re_ver = re.compile(r"%s (\d+)\.(\d+)\.(\d+)" % "mpv")

    for line in o.split("\n"):
        m = re_ver.match(line)

        if m:
            v = tuple(map(int, m.groups()))
            dbg("%s version %s.%s.%s detected", exename, *v)
            return v

    dbg("%sFailed to detect mpv version%s", c.r, c.w)
    return -1, 0, 0


def get_mplayer_version(exename):
    o = subprocess.check_output([exename]).decode()
    m = re.search('^MPlayer SVN[\s-]r([0-9]+)', o, re.MULTILINE|re.IGNORECASE)

    ver = 0
    if m:
        ver = int(m.groups()[0])
    else:
        m = re.search('^MPlayer ([0-9])+.([0-9]+)', o, re.MULTILINE)
        if m: 
            ver = tuple(int(i) for i in m.groups())

        else:
            dbg("%sFailed to detect mplayer version%s", c.r, c.w)

    return ver


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
    return utf8_replace(stuff) if not_utf8_environment else stuff


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
        ctypes.windll.kernel32.SetConsoleTitleW(xenc(title))
    else:
        sys.stdout.write(xenc('\x1b]2;' + title + '\x07'))


def list_update(item, lst, remove=False):
    """ Add or remove item from list, checking first to avoid exceptions. """
    if not remove and item not in lst:
        lst.append(item)

    elif remove and item in lst:
        lst.remove(item)


def get_near_name(begin, items):
    """ Return the closest matching playlist name that starts with begin. """
    for name in sorted(items):
        if name.lower().startswith(begin.lower()):
            break

    else:
        return begin

    return name


def F(key, nb=0, na=0, textlib=None):
    """Format text.

    nb, na indicate newlines before and after to return
    percent is the delimter for %s
    nums is the delimiter for the str.format command (**1 will become {1})
    textlib is the dictionary to use (defaults to g.text if not given)

    """
    textlib = textlib or g.text

    assert key in textlib
    text = textlib[key]
    percent_fmt = textlib.get(key + "_")

    if percent_fmt:
        text = re.sub(r"\*", r"%s", text) % percent_fmt

    text = text.replace("&&", "%s")

    return "\n" * nb + text + c.w + "\n" * na


def get_pafy(item, force=False, callback=None):
    """ Get pafy object for an item. """

    callback_fn = callback or (lambda x: None)
    cached = g.pafs.get(item.ytid)

    if not force and cached and cached.expiry > time.time():
        dbg("get pafy cache hit for %s", cached.title)
        cached.fresh = False
        return cached

    else:

        try:
            p = pafy.new(item.ytid, callback=callback_fn)

        except IOError as e:

            if "pafy" in str(e):
                dbg(c.p + "retrying failed pafy get: " + item.ytid + c.w)
                p = pafy.new(item.ytid, callback=callback)

            else:
                raise

        g.pafs[item.ytid] = p
        p.fresh = True
        thread = "preload: " if not callback else ""
        dbg("%s%sgot new pafy object: %s%s" % (c.y, thread, p.title[:26], c.w))
        dbg("%s%sgot new pafy object: %s%s" % (c.y, thread, p.videoid, c.w))
        return p
