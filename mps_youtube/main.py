#!/usr/bin/env python

"""
mps-youtube.

https://github.com/np1/mps-youtube

Copyright (C) 2014 nagev

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from __future__ import print_function

__version__ = "0.01.46"
__author__ = "nagev"
__license__ = "GPLv3"

from xml.etree import ElementTree as ET
import unicodedata
import collections
import subprocess
import threading
import __main__
import tempfile
import difflib
import logging
import random
import locale
import socket
import time
import math
import pafy
import json
import sys
import re
import os


try:
    # pylint: disable=F0401
    from colorama import init as init_colorama, Fore, Style
    has_colorama = True

except ImportError:
    has_colorama = False

try:
    import readline
    readline.set_history_length(2000)
    has_readline = True

except ImportError:
    has_readline = False


# Python 3 compatibility hack

if sys.version_info[:2] >= (3, 0):
    # pylint: disable=E0611,F0401
    uni = str
    import pickle
    from urllib.request import build_opener
    from urllib.error import HTTPError, URLError
    from urllib.parse import urlencode
    uni, byt, xinput = str, bytes, input

else:
    from urllib2 import build_opener, HTTPError, URLError
    import cPickle as pickle
    from urllib import urlencode
    uni, byt, xinput = unicode, str, raw_input
    uni = unicode

utf8_encode = lambda x: x.encode("utf8") if type(x) == uni else x
utf8_decode = lambda x: x.decode("utf8") if type(x) == byt else x
mswin = os.name == "nt"
not_utf8_environment = mswin or not "UTF-8" in os.environ.get("LANG", "")
member_var = lambda x: not(x.startswith("__") or callable(x))
locale.setlocale(locale.LC_ALL, "")  # for date formatting


def utf8_replace(txt):
    """ Replace unsupported characters in unicode string, returns unicode. """

    sse = sys.stdout.encoding
    txt = txt.encode(sse, "replace").decode("utf8", "ignore")
    return txt


def xenc(stuff):
    """ Replace unsupported characters. """
    stuff = utf8_replace(stuff) if not_utf8_environment else stuff
    return stuff


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


def get_default_ddir():
    """ Get system default Download directory, append mps dir. """

    user_home = os.path.expanduser("~")
    join, exists = os.path.join, os.path.exists

    if mswin:
        return join(user_home, "Downloads", "mps")

    USER_DIRS = join(user_home, ".config", "user-dirs.dirs")
    DOWNLOAD_HOME = join(user_home, "Downloads")

    # define ddir by (1) env var, (2) user-dirs.dirs file,
    #                (3) existing ~/Downloads dir (4) ~

    if 'XDG_DOWNLOAD_DIR' in os.environ:
        ddir = os.environ['XDG_DOWNLOAD_DIR']

    elif exists(USER_DIRS):
        lines = open(USER_DIRS).readlines()
        defn = [x for x in lines if x.startswith("XDG_DOWNLOAD_DIR")]

        if len(defn) == 1:
            ddir = defn[0].split("=")[1].replace('"', '')
            ddir = ddir.replace("$HOME", user_home).strip()

        else:
            ddir = DOWNLOAD_HOME if exists(DOWNLOAD_HOME) else user_home

    else:
        ddir = DOWNLOAD_HOME if exists(DOWNLOAD_HOME) else user_home

    ddir = utf8_decode(ddir)
    return os.path.join(ddir, "mps")


def get_config_dir():
    """ Get user's configuration directory. Migrate to new mps name if old."""

    if mswin:
        confdir = os.environ["APPDATA"]

    elif 'XDG_CONFIG_HOME' in os.environ:
        confdir = os.environ['XDG_CONFIG_HOME']

    else:
        confdir = os.path.join(os.path.expanduser("~"), '.config')

    mps_confdir = os.path.join(confdir, "mps-youtube")
    old_confdir = os.path.join(confdir, "pms-youtube")

    if os.path.exists(old_confdir) and not os.path.exists(mps_confdir):
        os.rename(old_confdir, mps_confdir)

    elif not os.path.exists(mps_confdir):
        os.makedirs(mps_confdir)

    return mps_confdir


def has_exefile(filename):
    """ Check whether file exists in path and is executable. """

    paths = os.environ.get("PATH", []).split(os.pathsep)
    dbg("searching path for %s", filename)

    for path in paths:
        exepath = os.path.join(path, filename)

        if os.path.exists(exepath):
            if os.path.isfile(exepath):

                if os.access(exepath, os.X_OK):
                    dbg("found at %s", exepath)
                    return exepath

    return False


def get_content_length(url, preloading=False):
    """ Return content length of a url. """

    prefix = "preload: " if preloading else ""
    dbg(c.y + prefix + "getting content-length header" + c.w)
    response = utf8_decode(g.urlopen(url))
    headers = response.headers
    cl = headers['content-length']
    return int(cl)


class Video(object):

    """ Class to represent a YouTube video. """

    def __init__(self, ytid=None, title=None, length=None):
        self.ytid = ytid
        self.title = title
        self.length = int(length)


def prune_streams():
    """ Keep cache size in check. """

    while len(g.pafs) > g.max_cached_streams:
        g.pafs.popitem(last=False)

    while len(g.streams) > g.max_cached_streams:
        g.streams.popitem(last=False)

    # prune time expired items

    now = time.time()
    oldpafs = [k for k in g.pafs if g.pafs[k].expiry < now]

    if len(oldpafs):
        dbg(c.r + "%s old pafy items pruned%s", len(oldpafs), c.w)

    for oldpaf in oldpafs:
        g.pafs.pop(oldpaf, 0)

    oldstreams = [k for k in g.streams if g.streams[k]['expiry'] < now]

    if len(oldstreams):
        dbg(c.r + "%s old stream items pruned%s", len(oldstreams), c.w)

    for oldstream in oldstreams:
        g.streams.pop(oldstream, 0)

    dbg(c.b + "paf: %s, streams: %s%s", len(g.pafs), len(g.streams), c.w)


def get_pafy(item, force=False, callback=None):
    """ Get pafy object for an item. """

    nullfunc = lambda x: None
    callback_fn = callback or nullfunc
    cached = g.pafs.get(item.ytid)

    if not force and cached and cached.expiry > time.time():
        dbg("get pafy cache hit for %s", cached.title)
        cached.fresh = False
        return cached

    else:

        try:
            p = pafy.new(item.ytid, callback=callback_fn)

        except IOError as e:

            if "pafy" in uni(e):
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


def get_streams(vid, force=False, callback=None, threeD=False):
    """ Get all streams as a dict.  callback function passed to get_pafy. """

    now = time.time()
    ytid = vid.ytid
    have_stream = g.streams.get(ytid) and g.streams[ytid]['expiry'] > now
    prfx = "preload: " if not callback else ""

    if not force and have_stream:
        ss = uni(int(g.streams[ytid]['expiry'] - now) // 60)
        dbg("%s%sGot streams from cache (%s mins left)%s", c.g, prfx, ss, c.w)
        return g.streams.get(ytid)['meta']

    p = get_pafy(vid, force=force, callback=callback)
    ps = p.allstreams if threeD else [x for x in p.allstreams if not x.threed]

    try:
        # test urls are valid
        [x.url for x in ps]

    except TypeError:
        # refetch if problem
        dbg("%s****Type Error in get_streams. Retrying%s", c.r, c.w)
        p = get_pafy(vid, force=True, callback=callback)
        ps = p.allstreams if threeD else [x for x in p.allstreams
                                          if not x.threed]

    streams = []

    for s in ps:
        x = dict(url=s.url,
                 ext=s.extension,
                 quality=s.quality,
                 mtype=s.mediatype,
                 size=-1)
        streams.append(x)

    g.streams[ytid] = dict(expiry=p.expiry, meta=streams)
    prune_streams()
    return streams


def select_stream(slist, q=0, audio=False, m4a_ok=True, maxres=None):
    """ Select a stream from stream list. """

    maxres = maxres or Config.MAX_RES.get
    slist = slist['meta'] if type(slist) == dict else slist
    au_streams = [x for x in slist if x['mtype'] == "audio"]

    okres = lambda x: int(x['quality'].split("x")[1]) <= maxres
    getq = lambda x: int(x['quality'].split("x")[1])
    vo_streams = [x for x in slist if x['mtype'] == "normal" and okres(x)]
    vo_streams = sorted(vo_streams, key=getq, reverse=True)

    if not m4a_ok:
        au_streams = [x for x in au_streams if not x['ext'] == "m4a"]

    streams = au_streams if audio else vo_streams
    dbg("select stream, q: %s, audio: %s, len: %s", q, audio, len(streams))

    try:
        ret = streams[q]

    except IndexError:
        ret = streams[0] if q and len(streams) else None

    return ret


def get_size(ytid, url, preloading=False):
    """ Get size of stream, try stream cache first. """

    # try cached value
    stream = [x for x in g.streams[ytid]['meta'] if x['url'] == url][0]
    size = stream['size']
    prefix = "preload: " if preloading else ""

    if not size == -1:
        dbg("%s%susing cached size: %s%s", c.g, prefix, size, c.w)

    else:
        writestatus("Getting content length", mute=preloading)
        stream['size'] = get_content_length(url, preloading=preloading)
        dbg("%s%s - content-length: %s%s", c.y, prefix, stream['size'], c.w)

    return stream['size']


class ConfigItem(object):

    """ A configuration item. """

    def __init__(self, name, value, minval=None, maxval=None, check_fn=None):
        """ If specified, the check_fn should return a dict.

        {valid: bool, message: success/fail mesage, value: value to set}

        """

        self.default = self.value = value
        self.name = name
        self.type = type(value)
        self.maxval, self.minval = maxval, minval
        self.check_fn = check_fn
        self.require_known_player = False
        self.allowed_values = []

    @property
    def get(self):
        """ Return value. """

        return self.value

    @property
    def display(self):
        """ Return value in a format suitable for display. """

        retval = self.value

        if self.name == "max_res":
            retval = uni(retval) + "p"

        return retval

    def set(self, value):
        """ Set value with checks. """

        # note: fail_msg should contain %s %s for self.name, value
        #       success_msg should not
        # pylint: disable=R0912
        # too many branches

        success_msg = fail_msg = ""
        value = value.strip()
        value_orig = value
        green = lambda x: "%s%s%s" % (c.g, x, c.w)

        # handle known player not set

        if self.allowed_values and not value in self.allowed_values:
            fail_msg = "%s must be one of * - not %s"
            fail_msg = fail_msg.replace("*", ", ".join(self.allowed_values))

        if self.require_known_player and not known_player_set():
            fail_msg = "%s requires mpv or mplayer, can't set to %s"

        # handle true / false values

        elif self.type == bool:

            if value.upper() in "0 OFF NO DISABLED FALSE".split():
                value = False
                success_msg = "%s set to False" % green(self.name)

            elif value.upper() in "1 ON YES ENABLED TRUE".split():
                value = True
                success_msg = "%s set to True" % green(self.name)

            else:
                fail_msg = "%s requires True/False, got %s"

        # handle int values

        elif self.type == int:

            if not value.isdigit():
                fail_msg = "%s requires a number, got %s"

            else:
                value = int(value)

                if self.maxval and self.minval:

                    if not self.minval <= value <= self.maxval:
                        m = " must be between %s and %s, got "
                        m = m % (self.minval, self.maxval)
                        fail_msg = "%s" + m + "%s"

                if not fail_msg:
                    dispval = value or "None"
                    success_msg = "%s set to %s" % (green(self.name), dispval)

        # handle space separated list

        elif self.type == list:
            success_msg = "%s set to %s" % (green(self.name), value)
            value = value.split()

        # handle string values

        elif self.type == str:
            dispval = value or "None"
            success_msg = "%s set to %s" % (green(self.name), green(dispval))

        # handle failure

        if fail_msg:
            failed_val = value_orig.strip() or "<nothing>"
            colvals = c.y + self.name + c.w, c.y + failed_val + c.w
            return fail_msg % colvals

        elif self.check_fn:
            checked = self.check_fn(value)
            value = checked.get("value") or value

            if checked['valid']:
                value = checked.get("value", value)
                self.value = value
                saveconfig()
                return checked.get("message", success_msg)

            else:
                return checked.get('message', fail_msg)

        elif success_msg:
            self.value = value
            saveconfig()
            return success_msg


def check_console_width(val):
    """ Show ruler to check console width. """
    valid = True
    message = "-" * val + "\n"
    message += "console_width set to %s, try a lower value if above line ove"\
        "rlaps" % val
    return dict(valid=valid, message=message)


def check_ddir(d):
    """ Check whether dir is a valid directory. """

    if os.path.isdir(d):
        message = "Downloads will be saved to " + c.y + d + c.w
        return dict(valid=True, message=message)

    else:
        message = "Not a valid directory: " + c.r + d + c.w
        return dict(valid=False, message=message)


def check_win_pos(pos):
    """ Check window position input. """

    if not pos.strip():
        return dict(valid=True, message="Window position not set (default)")

    pos = pos.lower()
    reg = r"(TOP|BOTTOM).?(LEFT|RIGHT)"

    if not re.match(reg, pos, re.I):
        msg = "Try something like top-left or bottom-right (or default)"
        return dict(valid=False, message=msg)

    else:
        p = re.match(reg, pos, re.I).groups()
        p = "%s-%s" % p
        msg = "Window position set to %s" % p
        return dict(valid=True, message=msg, value=p)


def check_win_size(size):
    """ Check window size input. """

    if not size.strip():
        return dict(valid=True, message="Window size not set (default)")

    size = size.lower()
    reg = r"\d{1,4}x\d{1,4}"

    if not re.match(reg, size, re.I):
        msg = "Try something like 720x480"
        return dict(valid=False, message=msg)

    else:
        return dict(valid=True, value=size)


def check_colours(val):
    """ Check whether colour config value can be set. """

    if val and mswin and not has_colorama:
        message = "The colorama module needs to be installed for colour output"
        return dict(valid=False, message=message)

    else:
        return dict(valid=True)


class Config(object):

    """ Holds various configuration values. """

    ORDER = ConfigItem("order", "relevance")
    ORDER.allowed_values = "relevance date views rating".split()
    MAX_RESULTS = ConfigItem("max_results", 19, maxval=50, minval=1)
    CONSOLE_WIDTH = ConfigItem("console_width", 80, minval=70, maxval=880,
                               check_fn=check_console_width)
    MAX_RES = ConfigItem("max_res", 2160, minval=192, maxval=2160)
    PLAYER = ConfigItem("player", "mplayer")
    PLAYERARGS = ConfigItem("playerargs", "")
    CHECKUPDATE = ConfigItem("checkupdate", True)
    SHOW_MPLAYER_KEYS = ConfigItem("show_mplayer_keys", True)
    SHOW_MPLAYER_KEYS.require_known_player = True
    FULLSCREEN = ConfigItem("fullscreen", False)
    FULLSCREEN.require_known_player = True
    SHOW_STATUS = ConfigItem("show_status", True)
    COLUMNS = ConfigItem("columns", "")
    DDIR = ConfigItem("ddir", get_default_ddir(), check_fn=check_ddir)
    SHOW_VIDEO = ConfigItem("show_video", False)
    SEARCH_MUSIC = ConfigItem("search_music", True)
    WINDOW_POS = ConfigItem("window_pos", "", check_fn=check_win_pos)
    WINDOW_POS.require_known_player = True
    WINDOW_SIZE = ConfigItem("window_size", "", check_fn=check_win_size)
    WINDOW_SIZE.require_known_player = True
    COLOURS = ConfigItem("colours",
                         False if mswin and not has_colorama else True,
                         check_fn=check_colours)


class Playlist(object):

    """ Representation of a playist, has list of songs. """

    def __init__(self, name=None, songs=None):
        self.name = name
        self.creation = time.time()
        self.songs = songs or []

    @property
    def is_empty(self):
        """ Return True / False if songs are populated or not. """

        return bool(not self.songs)

    @property
    def size(self):
        """ Return number of tracks. """

        return len(self.songs)

    @property
    def duration(self):
        """ Sum duration of the playlist. """

        duration = sum(s.length for s in self.songs)
        duration = time.strftime('%H:%M:%S', time.gmtime(int(duration)))
        return duration


class g(object):

    """ Class for holding globals that are needed throught the module. """

    meta = {}
    command_line = False
    debug_mode = False
    urlopen = None
    ytpls = []
    browse_mode = "normal"
    preloading = []
    #expiry = 5 * 60 * 60  # 5 hours
    blank_text = "\n" * 200
    helptext = []
    max_retries = 3
    max_cached_streams = 1500
    url_memo = collections.OrderedDict()
    model = Playlist(name="model")
    last_search_query = {}
    current_page = 1
    active = Playlist(name="active")
    text = {}
    userpl = {}
    ytpl = {}
    pafs = collections.OrderedDict()
    streams = collections.OrderedDict()
    pafy_pls = {}  #
    last_opened = message = content = ""
    config = [x for x in sorted(dir(Config)) if member_var(x)]
    configbool = [x for x in config if type(getattr(Config, x)) is bool]
    defaults = {setting: getattr(Config, setting) for setting in config}
    suffix = "3" if sys.version_info[:2] >= (3, 0) else ""
    CFFILE = os.path.join(get_config_dir(), "config")
    OLD_PLFILE = os.path.join(get_config_dir(), "playlist" + suffix)
    PLFILE = os.path.join(get_config_dir(), "playlist_v2")
    CACHEFILE = os.path.join(get_config_dir(), "cache_py_" + sys.version[0:5])
    READLINE_FILE = None
    playerargs_defaults = {
        "mpv": {"title": "--title",
                "fs": "--fs",
                "novid": "--no-video",
                "ignidx": "--demuxer-lavf-o=fflags=+ignidx",
                "geo": "--geometry"
                },
        "mplayer": {"title": "-title",
                    "fs": "-fs",
                    "novid": "-novideo",
                    #"ignidx": "-lavfdopts o=fflags=+ignidx".split()
                    "ignidx": "",
                    "geo": "-geometry"
                    }
    }


def get_version_info():
    """ Return version and platform info. """

    import platform
    out = ("\nmpsyt version  : %s " % __version__)
    out += ("\npafy version   : %s" % pafy.__version__)
    out += ("\nPython version : %s" % sys.version)
    out += ("\nProcessor      : %s" % platform.processor())
    out += ("\nMachine type   : %s" % platform.machine())
    out += ("\nArchitecture   : %s, %s" % platform.architecture())
    out += ("\nPlatform       : %s" % platform.platform())
    envs = "TERM SHELL LANG LANGUAGE".split()

    for env in envs:
        value = os.environ.get(env)
        out += "\nenv:%-11s: %s" % (env, value) if value else ""

    return out


def process_cl_args(args):
    """ Process command line arguments. """

    if "--version" in args:
        print(get_version_info())
        print("")
        sys.exit()

    if "--help" in args:

        for x in g.helptext:
            print(x[2])

        sys.exit()

    g.command_line = "playurl" in args or "dlurl" in args
    g.blank_text = "" if g.command_line else g.blank_text


def init():
    """ Initial setup. """

    __main__.Playlist = Playlist
    __main__.Video = Video

    init_text()
    init_readline()
    init_opener()
    init_cache()

    # set player to mpv if no config file exists and mpv is installed
    E = os.path.exists
    if not E(g.CFFILE) and not has_exefile("mplayer") and has_exefile("mpv"):
        Config.PLAYER = ConfigItem("player", "mpv")
        saveconfig()

    else:
        import_config()

    # setup colorama
    if has_colorama and mswin:
        init_colorama()

    process_cl_args(sys.argv)


def init_cache():
    """ Import cache file. """

    if os.path.isfile(g.CACHEFILE):

        try:

            with open(g.CACHEFILE, "rb") as cf:
                g.streams = pickle.load(cf)

            dbg(c.g + "%s cached streams imported%s", uni(len(g.streams)), c.w)

        except (EOFError, IOError):
            dbg(c.r + "Cache file failed to open" + c.w)

        prune_streams()


def init_readline():
    """ Enable readline for input history. """

    if g.command_line:
        return

    if has_readline:
        g.READLINE_FILE = os.path.join(get_config_dir(), "input_history")

        if os.path.exists(g.READLINE_FILE):
            readline.read_history_file(g.READLINE_FILE)
            dbg(c.g + "Read history file" + c.w)


def init_opener():
    """ Set up url opener. """

    opener = build_opener()
    ua = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; "
    ua += "Trident/5.0)"
    opener.addheaders = [("User-Agent", ua)]
    g.urlopen = opener.open


def known_player_set():
    """ Return true if the set player is known. """

    for allowed_player in g.playerargs_defaults:
        regex = r'(?:^%s$)|(?:\b%s$)' % ((allowed_player,) * 2)
        match = re.search(regex, Config.PLAYER.get)

        if mswin:
            match = re.search(regex, Config.PLAYER.get, re.IGNORECASE)

        if match:
            return True

    return False


def showconfig(_):
    """ Dump config data. """

    width = Config.CONSOLE_WIDTH.get - 30
    s = "  %s%-17s%s : %s\n"
    out = "  %s%-17s   %s%s%s\n" % (c.ul, "Key", "Value", " " * width, c.w)

    for setting in g.config:
        val = getattr(Config, setting)

        # don't show player specific settings if unknown player
        if not known_player_set() and val.require_known_player:
            continue

        out += s % (c.g, setting.lower(), c.w, val.display)

    g.content = out
    g.message = "Enter %sset <key> <value>%s to change\n" % (c.g, c.w)
    g.message += "Enter %sset all default%s to reset all" % (c.g, c.w)


def saveconfig():
    """ Save current config to file. """

    config = {setting: getattr(Config, setting).value for setting in g.config}

    with open(g.CFFILE, "wb") as cf:
        pickle.dump(config, cf, protocol=2)

    dbg(c.p + "Saved config: " + g.CFFILE + c.w)


def savecache():
    """ Save stream cache. """

    with open(g.CACHEFILE, "wb") as cf:
        pickle.dump(g.streams, cf, protocol=2)

    dbg(c.p + "saved cache file: " + g.CACHEFILE + c.w)


def import_config():
    """ Override config if config file exists. """

    if os.path.exists(g.CFFILE):

        with open(g.CFFILE, "rb") as cf:
            saved_config = pickle.load(cf)

        for k, v in saved_config.items():
            getattr(Config, k).value = v

        # Update config files from versions <= 0.01.41
        if type(Config.PLAYERARGS.get) == list:
            Config.WINDOW_POS.value = "top-right"
            redundant = ("-really-quiet --really-quiet -prefer-ipv4 -nolirc "
                         "-fs --fs".split())

            for r in redundant:
                dbg("removing redundant arg %s", r)
                list_update(r, Config.PLAYERARGS.value, remove=True)

            Config.PLAYERARGS.value = " ".join(Config.PLAYERARGS.get)
            saveconfig()


class c(object):

    """ Class for holding colour code values. """

    if mswin and has_colorama:
        white = Style.RESET_ALL
        ul = Style.DIM + Fore.YELLOW
        red, green, yellow = Fore.RED, Fore.GREEN, Fore.YELLOW
        blue, pink = Fore.CYAN, Fore.MAGENTA

    elif mswin:
        Config.COLOURS.value = False

    else:
        white = "\x1b[%sm" % 0
        ul = "\x1b[%sm" * 3 % (2, 4, 33)
        cols = ["\x1b[%sm" % n for n in range(91, 96)]
        red, green, yellow, blue, pink = cols

    if not Config.COLOURS.get:
        ul = red = green = yellow = blue = pink = white = ""
    r, g, y, b, p, w = red, green, yellow, blue, pink, white


def setconfig(key, val):
    """ Set configuration variable. """

    key = key.replace("-", "_")
    if key.upper() == "ALL" and val.upper() == "DEFAULT":

        for ci in g.config:
            getattr(Config, ci).value = getattr(Config, ci).default

        saveconfig()
        message = "Default configuration reinstated"

    elif not key.upper() in g.config:
        message = "Unknown config item: %s%s%s" % (c.r, key, c.w)

    elif val.upper() == "DEFAULT":
        att = getattr(Config, key.upper())
        att.value = att.default
        message = "%s%s%s set to %s%s%s (default)"
        dispval = att.display or "None"
        message = message % (c.y, key, c.w, c.y, dispval, c.w)
        saveconfig()

    else:
        # saveconfig() will be called by Config.set() method
        message = getattr(Config, key.upper()).set(val)

    showconfig(1)
    g.message = message


def F(key, nb=0, na=0, percent=r"\*", nums=r"\*\*", textlib=None):
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
    number_fmt = textlib.get("_" + key)

    if number_fmt:
        text = re.sub(r"(%s(\d))" % nums, "{\\2}", text)
        text = text.format(*number_fmt)

    if percent_fmt:
        text = re.sub(r"%s" % percent, r"%s", text)
        text = text % percent_fmt

    text = re.sub(r"&&", r"%s", text)

    return "\n" * nb + text + c.w + "\n" * na


def init_text():
    """ Set up text. """

    g.text = {

        "exitmsg": ("**0mps-youtube - **1http://github.com/np1/mps-youtube**0"
                    "\nReleased under the GPLv3 license\n"
                    "(c) 2014 nagev**2\n"""),
        "_exitmsg": (c.r, c.b, c.w),

        # Error / Warning messages

        'no playlists': "*No saved playlists found!*",
        'no playlists_': (c.r, c.w),
        'pl bad name': '*&&* is not valid a valid name. Ensure it starts with'
        ' a letter or _',
        'pl bad name_': (c.r, c.w),
        'pl not found': 'Playlist *&&* unknown. Saved playlists are shown '
        'above',
        'pl not found_': (c.r, c.w),
        'pl not found advise ls': 'Playlist "*&&*" not found. Use *ls* to '
        'list',
        'pl not found advise ls_': (c.y, c.w, c.g, c.w),
        'pl empty': 'Playlist is empty!',
        'advise add': 'Use *add N* to add a track',
        'advise add_': (c.g, c.w),
        'advise search': 'Search for items and then use *add* to add them',
        'advise search_': (c.g, c.w),
        'no data': 'Error fetching data. Possible network issue.'
        '\n*&&*',
        'no data_': (c.r, c.w),
        'use dot': 'Start your query with a *.* to perform a search',
        'use dot_': (c.g, c.w),
        'cant get track': 'Problem playing last item: *&&*',
        'cant get track_': (c.r, c.w),
        'track unresolved': 'Sorry, this track is not available',
        'no player': '*&&* was not found on this system',
        'no player_': (c.y, c.w),
        'no pl match for rename': '*Couldn\'t find matching playlist to '
        'rename*',
        'no pl match for rename_': (c.r, c.w),
        'invalid range': "*Invalid item / range entered!*",
        'invalid range_': (c.r, c.w),
        '-audio': "*Warning* - the filetype you selected (m4v) has no audio!",
        '-audio_': (c.y, c.w),

        # Info messages

        'select mux': ("Select [*&&*] to mux audio or [*Enter*] to download "
                       "without audio\nThis feature is experimental!"),
        'select mux_': (c.y, c.w, c.y, c.w),
        'pl renamed': 'Playlist *&&* renamed to *&&*',
        'pl renamed_': (c.y, c.w, c.y, c.w),
        'pl saved': 'Playlist saved as *&&*.  Use *ls* to list playlists',
        'pl saved_': (c.y, c.w, c.g, c.w),
        'pl loaded': 'Loaded playlist *&&* as current playlist',
        'pl loaded_': (c.y, c.w),
        'pl viewed': 'Showing playlist *&&*',
        'pl viewed_': (c.y, c.w),
        'pl help': 'Enter *open <name or ID>* to load a playlist',
        'pl help_': (c.g, c.w),
        'added to pl': '*&&* tracks added (*&&* total [*&&*]). Use *vp* to '
        'view',
        'added to pl_': (c.y, c.w, c.y, c.w, c.y, c.w, c.g, c.w),
        'added to saved pl': '*&&* tracks added to *&&* (*&&* total [*&&*])',
        'added to saved pl_': (c.y, c.w, c.y, c.w, c.y, c.w, c.y, c.w),
        'song move': 'Moved *&&* to position *&&*',
        'song move_': (c.y, c.w, c.y, c.w),
        'song sw': ("Switched item *&&* with *&&*"),
        'song sw_': (c.y, c.w, c.y, c.w),
        'current pl': "This is the current playlist. Use *save <name>* to save"
        " it",
        'current pl_': (c.g, c.w),
        'help topic': ("  Enter *help <topic>* for specific help:"),
        'help topic_': (c.y, c.w),
        'songs rm': '*&&* tracks removed &&',
        'songs rm_': (c.y, c.w)}


def save_to_file():
    """ Save playlists.  Called each time a playlist is saved or deleted. """

    with open(g.PLFILE, "wb") as plf:
        pickle.dump(g.userpl, plf, protocol=2)

    dbg(c.r + "Playlist saved\n---" + c.w)


def open_from_file():
    """ Open playlists. Called once on script invocation. """

    try:

        with open(g.PLFILE, "rb") as plf:
            g.userpl = pickle.load(plf)

    except IOError:
        # no playlist found, create a blank one
        if not os.path.isfile(g.PLFILE):
            g.userpl = {}
            save_to_file()

    except EOFError:
        print("Error opening playlists from %s" % g.PLFILE)
        sys.exit()

    # remove any cached urls from playlist file, these are now
    # stored in a separate cache file

    save = False

    for k, v in g.userpl.items():

        for song in v.songs:

            if hasattr(song, "urls"):
                dbg("remove %s: %s", k, song.urls)
                del song.urls
                save = True

    if save:
        save_to_file()


def convert_playlist_to_v2():
    """ Convert previous playlist file to v2 playlist. """

    # skip if previously done
    if os.path.isfile(g.PLFILE):
        return

    # skip if no playlist files exist
    elif not os.path.isfile(g.OLD_PLFILE):
        return

    try:
        with open(g.OLD_PLFILE, "rb") as plf:
            old_playlists = pickle.load(plf)

    except IOError:
        sys.exit("Couldn't open old playlist file")

    #rename old playlist file
    backup = g.OLD_PLFILE + "_v1_backup"

    if os.path.isfile(backup):
        sys.exit("Error, backup exists but new playlist exists not!")

    os.rename(g.OLD_PLFILE, backup)

    # do the conversion
    for plname, plitem in old_playlists.items():

        songs = []

        for video in plitem.songs:
            v = Video(video['link'], video['title'], video['duration'])
            songs.append(v)

        g.userpl[plname] = Playlist(plname, songs)

    # save as v2
    save_to_file()


def logo(col=None, version=""):
    """ Return text logo. """

    col = col if col else random.choice((c.g, c.r, c.y, c.b, c.p, c.w))
    LOGO = col + ("""\

                88888b.d88b.  88888b.  .d8888b
                888 "888 "88b 888 "88b 88K
                888  888  888 888  888 "Y8888b.
                888  888  888 888 d88P      X88
                888  888  888 88888P"   88888P'
                              888
                              888   %s%s
                              888%s%s"""
                  % (c.w + "v" + version + " (YouTube)" if version else "",
                     col, c.w, "\n\n"))

    return LOGO + c.w if not g.debug_mode else ""


def playlists_display():
    """ Produce a list of all playlists. """

    if not g.userpl:
        g.message = F("no playlists")
        return logo(c.y) + "\n\n" if g.model.is_empty else \
            generate_songlist_display()

    maxname = max(len(a) for a in g.userpl)
    out = "      {0}Saved Playlists{1}\n".format(c.ul, c.w)
    start = "      "
    fmt = "%s%s%-3s %-" + uni(maxname + 3) + "s%s %s%-7s%s %-5s%s"
    head = (start, c.b, "ID", "Name", c.b, c.b, "Count", c.b, "Duration", c.w)
    out += "\n" + fmt % head + "\n\n"

    for v, z in enumerate(sorted(g.userpl)):
        n, p = z, g.userpl[z]
        l = fmt % (start, c.g, v + 1, n, c.w, c.y, uni(p.size), c.y,
                   p.duration, c.w) + "\n"
        out += l

    return out


def mplayer_help(short=True):
    """ Mplayer help.  """
    # pylint: disable=W1402

    volume = "[{0}9{1}] volume [{0}0{1}]"
    volume = volume if short else volume + "      [{0}ctrl-c{1}] return"
    seek = u"[{0}\u2190{1}] seek [{0}\u2192{1}]"
    pause = u"[{0}\u2193{1}] SEEK [{0}\u2191{1}]       [{0}space{1}] pause"

    if not_utf8_environment:
        seek = "[{0}<-{1}] seek [{0}->{1}]"
        pause = "[{0}DN{1}] SEEK [{0}UP{1}]       [{0}space{1}] pause"

    ret = "[{0}q{1}] %s" % ("return" if short else "next track")
    fmt = "    %-20s       %-20s"
    lines = fmt % (seek, volume) + "\n" + fmt % (pause, ret)
    return lines.format(c.g, c.w)


def fmt_time(seconds):
    """ Format number of seconds to %H:%M:%S. """

    hms = time.strftime('%H:%M:%S', time.gmtime(int(seconds)))
    H, M, S = hms.split(":")

    if H == "00":
        hms = M + ":" + S

    elif H == "01" and int(M) < 40:
        hms = uni(int(M) + 60) + ":" + S

    elif H.startswith("0"):
        hms = ":".join([H[1], M, S])

    return hms


def get_tracks_from_json(jsons):
    """ Get search results from web page. """

    try:
        items = jsons['data']['items']

    except KeyError:
        items = []

    songs = []

    for item in items:
        ytid = item['id']
        cursong = Video(ytid=ytid, title=item['title'].strip(),
                        length=int(item['duration']))

        likes = item.get('likeCount', "0")
        likes = int(re.sub(r"\D", "", likes))
        total = item.get('ratingCount', 0)
        dislikes = total - likes
        g.meta[ytid] = dict(rating=uni(item.get('rating',"0."))
                            [:4].ljust(4, "0"),
                            uploader=item['uploader'],
                            category=item['category'],
                            aspect=item.get('aspectRatio', "custom"),
                            uploaded=yt_datetime(item['uploaded'])[1],
                            likes=uni(num_repr(likes)),
                            dislikes=uni(num_repr(dislikes)),
                            commentCount=uni(num_repr(item.get('commentCount',
                                                               0))),
                            viewCount=uni(num_repr(item.get("viewCount", 0))),
                            title=item['title'],
                            length=uni(fmt_time(cursong.length))
                            )

        songs.append(cursong)

    if not items:
        dbg("got unexpected data or no search results")
        return False

    return songs


def screen_update():
    """ Display content, show message, blank screen."""

    print(g.blank_text)

    if g.content:
        xprint(g.content)

    if g.message:
        xprint(g.message)

    g.message = g.content = False


def playback_progress(idx, allsongs, repeat=False):
    """ Generate string to show selected tracks, indicate current track. """

    # pylint: disable=R0914
    # too many local variables
    cw = Config.CONSOLE_WIDTH.get
    out = "  %s%-XXs%s%s\n".replace("XX", uni(cw - 9))
    out = out % (c.ul, "Title", "Time", c.w)
    show_key_help = (Config.PLAYER.get in ["mplayer", "mpv"]
                     and Config.SHOW_MPLAYER_KEYS.get)
    multi = len(allsongs) > 1

    for n, song in enumerate(allsongs):
        length_orig = fmt_time(song.length)
        length = " " * (8 - len(length_orig)) + length_orig
        i = uea_pad(cw - 14, song.title), length, length_orig
        fmt = (c.w, "  ", c.b, i[0], c.w, c.y, i[1], c.w)

        if n == idx:
            fmt = (c.y, "> ", c.p, i[0], c.w, c.p, i[1], c.w)
            cur = i

        out += "%s%s%s%s%s %s%s%s\n" % fmt

    out += "\n" * (3 - len(allsongs))
    pos = 8 * " ", c.y, idx + 1, c.w, c.y, len(allsongs), c.w
    playing = "{}{}{}{} of {}{}{}\n\n".format(*pos) if multi else "\n\n"
    keys = mplayer_help(short=(not multi and not repeat))
    out = out if multi else generate_songlist_display(song=allsongs[0])

    if show_key_help:
        out += "\n" + keys

    else:
        playing = "{}{}{}{} of {}{}{}\n".format(*pos) if multi else "\n"
        out += "\n" + " " * (cw - 19) if multi else ""

    fmt = playing, c.r, cur[0].strip()[:cw - 19], c.w, c.w, cur[2], c.w
    out += "%s    %s%s%s %s[%s]%s" % fmt
    out += "    REPEAT MODE" if repeat else ""
    return out


def num_repr(num):
    """ Return up to four digit string representation of a number, eg 2.6m. """

    if num <= 9999:
        return uni(num)

    digit_count = lambda x: int(math.floor(math.log10(x)) + 1)
    digits = digit_count(num)
    sig = 3 if digits % 3 == 0 else 2
    rounded = int(round(num, int(sig - digits)))
    digits = digit_count(rounded)
    suffix = "_kmBTqXYX"[(digits - 1) // 3]
    front = 3 if digits % 3 == 0 else digits % 3

    if not front == 1:
        return uni(rounded)[0:front] + suffix

    return uni(rounded)[0] + "." + uni(rounded)[1] + suffix


def real_len(u, alt=False):
    """ Try to determine width of strings displayed with monospace font. """

    if type(u) != uni:
        u = u.decode("utf8")

    ueaw = unicodedata.east_asian_width

    if alt:
        #widths = dict(W=2, F=2, A=1, N=0.75, H=0.5)  # original
        widths = dict(N=.75, Na=1, W=2, F=2, A=1)

    else:
        widths = dict(W=2, F=2, A=1, N=1, H=0.5)

    return int(round(sum(widths.get(ueaw(char), 1) for char in u)))


def uea_trunc(num, t):
    """ Truncate to num chars taking into account East Asian width chars. """

    while real_len(t) > num:
        t = t[:-1]

    return t


def uea_pad(num, t, direction="<", notrunc=False):
    """ Right pad with spaces taking into account East Asian width chars. """

    direction = direction.strip() or "<"

    if not notrunc:
        t = uea_trunc(num, t)

    if real_len(t) < num:
        spaces = num - real_len(t)

        if direction == "<":
            t = t + (" " * spaces)

        elif direction == ">":
            t = (" " * spaces) + t

        elif direction == "^":
            right = False

            while real_len(t) < num:
                t = t + " " if right else " " + t
                right = not right

    return t


def yt_datetime(yt_date_time):
    """ Return a time object and locale formated date string. """

    time_obj = time.strptime(yt_date_time, "%Y-%m-%dT%H:%M:%S.000Z")
    locale_date = time.strftime("%x", time_obj)
    # strip first two digits of four digit year
    short_date = re.sub(r"(\d\d\D\d\d\D)20(\d\d)$", r"\1\2", locale_date)
    return time_obj, short_date


def generate_playlist_display():
    """ Generate list of playlists. """

    if not g.ytpls:
        g.message = c.r + "No playlists found!"
        return logo(c.g) + "\n\n"

    cw = Config.CONSOLE_WIDTH.get
    fmtrow = "%s%-5s %s %-8s  %-2s%s\n"
    fmthd = "%s%-5s %-{}s %-9s %-5s%s\n".format(cw - 23)
    head = (c.ul, "Item", "Playlist", "Updated", "Count", c.w)
    out = "\n" + fmthd % head

    for n, x in enumerate(g.ytpls):
        col = (c.g if n % 2 == 0 else c.w)
        length = x.get('size') or "?"
        length = "%4s" % length
        title = x.get('title') or "unknown"
        updated = yt_datetime(x.get('updated'))[1]
        title = uea_pad(cw - 23, title)
        out += (fmtrow % (col, uni(n + 1), title, updated, uni(length), c.w))

    return out + "\n" * (5 - len(g.ytpls))


def get_user_columns():
    """ Get columns from user config, return dict. """
    total_size = 0
    user_columns = Config.COLUMNS.get
    user_columns = user_columns.replace(",", " ").split()

    defaults = {"views": dict(name="viewCount", size=4, heading="View"),
                "rating": dict(name="rating", size=4, heading="Rtng"),
                "comments": dict(name="commentCount", size=4, heading="Comm"),
                "date": dict(name="uploaded", size=8, heading="Date"),
                "user": dict(name="uploader", size=10, heading="User"),
                "likes": dict(name="likes", size=4, heading="Like"),
                "dislikes": dict(name="dislikes", size=4, heading="Dslk"),
                "category": dict(name="category", size=8, heading="Category"),
                }

    ret = []
    for column in user_columns:
        namesize = column.split(":")
        name = namesize[0]

        if name in defaults:
            z = defaults[name]
            nm, sz, hd = z['name'], z['size'], z['heading']

            if len(namesize) == 2 and namesize[1].isdigit():
                sz = int(namesize[1])

            total_size += sz
            if total_size < Config.CONSOLE_WIDTH.get - 18:
                ret.append(dict(name=nm, size=sz, heading=hd))

    return ret


def generate_songlist_display(song=False, zeromsg=None, frmat="search"):
    """ Generate list of choices from a song list."""

    # pylint: disable=R0914
    if g.browse_mode == "ytpl":
        return generate_playlist_display()

    songs = g.model.songs or []

    if not songs:
        g.message = zeromsg or "Enter /search-term to search or [h]elp"
        return logo(c.g) + "\n\n"

    have_meta = all(x.ytid in g.meta for x in songs)
    user_columns = get_user_columns() if have_meta else []
    maxlength = max(x.length for x in songs)
    lengthsize = 8 if maxlength > 35999 else 7
    lengthsize = 5 if maxlength < 6000 else lengthsize
    reserved = 9 + lengthsize + len(user_columns)
    cw = Config.CONSOLE_WIDTH.get - 1
    title_size = cw - sum(1 + x['size'] for x in user_columns) - reserved
    before = [{"name": "idx", "size": 3, "heading": "Num"},
              {"name": "title", "size": title_size, "heading": "Title"}]
    after = [{"name": "length", "size": lengthsize, "heading": "Time"}]
    columns = before + user_columns + after

    for n, column in enumerate(columns):
        column['idx'] = n
        column['sign'] = "-" if not column['name'] == "length" else ""

    fmt = ["%{}{}s  ".format(x['sign'], x['size']) for x in columns]
    fmtrow = fmt[0:1] + ["%s  "] + fmt[2:]
    fmt, fmtrow = "".join(fmt).strip(), "".join(fmtrow).strip()
    titles = tuple([x['heading'][:x['size']] for x in columns])
    hrow = c.ul + fmt % titles + c.w
    out = "\n" + hrow + "\n"

    for n, x in enumerate(songs):
        col = (c.r if n % 2 == 0 else c.p) if not song else c.b
        details = {'title': x.title, "length": fmt_time(x.length)}
        details = g.meta[x.ytid].copy() if have_meta else details
        otitle = details['title']
        details['idx'] = uni(n + 1)
        details['title'] = uea_pad(columns[1]['size'], otitle)
        data = []

        for z in columns:
            fieldsize, field = z['size'], z['name']

            if len(details[field]) > fieldsize:
                details[field] = details[field][:fieldsize]

            data.append(details[field])

        line = fmtrow % tuple(data)
        col = col if not song or song != songs[n] else c.p
        line = col + line + c.w
        out += line + "\n"

    return out + "\n" * (5 - len(songs)) if not song else out


def writestatus(text, mute=False):
    """ Update status linei. """

    if not mute and Config.SHOW_STATUS.get:
        writeline(text)


def writeline(text):
    """ Print text on same line. """

    spaces = 75 - len(text)
    sys.stdout.write(" " + text + (" " * spaces) + "\r")
    sys.stdout.flush()


def list_update(item, lst, remove=False):
    """ Add or remove item from list, checking first to avoid exceptions. """

    if not remove and not item in lst:
        lst.append(item)

    elif remove and item in lst:
        lst.remove(item)


def generate_real_playerargs(song, override, failcount):
    """ Generate args for player command.

    Return args and songdata status.

    """

    #pylint: disable=R0914
    #pylint: disable=R0912
    video = Config.SHOW_VIDEO.get
    video = True if override in ("fullscreen", "window") else video
    video = False if override == "audio" else video
    m4a = not Config.PLAYER.get == "mplayer"
    q, audio, cached = failcount, not video, g.streams[song.ytid]
    stream = select_stream(cached, q=q, audio=audio, m4a_ok=m4a)

    # handle no audio stream available, or m4a with mplayer
    # by switching to video stream and suppressing video output.
    if not stream and not video or failcount and not video:
        dbg(c.r + "no audio or mplayer m4a, using video stream" + c.w)
        override = "a-v"
        video = True
        stream = select_stream(cached, q=q, audio=False, maxres=1600)

    if not stream and video:
        raise IOError("No streams available")

    if "uiressl=yes" in stream['url'] and "mplayer" in Config.PLAYER.get:
        raise IOError("%s : Sorry mplayer doesn't support this stream. "
                      "Use mpv or download it" % song.title)

    size = get_size(song.ytid, stream['url'])
    songdata = song.ytid, stream['ext'], int(size / (1024 ** 2))

    # pylint: disable=E1103
    # pylint thinks PLAYERARGS.get might be bool
    argsstr = Config.PLAYERARGS.get.strip()
    args = argsstr.split() if argsstr else []

    if known_player_set():
        pd = g.playerargs_defaults[Config.PLAYER.get]
        args.append(pd["title"])
        args.append(song.title)
        novid_arg = pd["novid"]
        fs_arg = pd["fs"]
        list_update(fs_arg, args, remove=not Config.FULLSCREEN.get)

        geometry = ""

        if Config.WINDOW_SIZE.get and not "-geometry" in argsstr:
            geometry = Config.WINDOW_SIZE.get

        if Config.WINDOW_POS.get and not "-geometry" in argsstr:
            wp = Config.WINDOW_POS.get
            xx = "+1" if "top" in wp else "-1"
            yy = "+1" if "left" in wp else "-1"
            geometry += "%s%s" % (yy, xx)

        if geometry:
            list_update(pd['geo'], args)
            list_update(geometry, args)

        # handle no audio stream available
        if override == "a-v":
            list_update(novid_arg, args)

        elif override == "fullscreen":
            list_update(fs_arg, args)

        elif override == "window":
            list_update(fs_arg, args, remove=True)

        # prevent ffmpeg issue (https://github.com/mpv-player/mpv/issues/579)
        if not video and stream['ext'] == "m4a":
            dbg("%susing ignidx flag%s", c.y, c.w)
            list_update(pd["ignidx"], args)

        if "mplayer" in Config.PLAYER.get:
            list_update("-really-quiet", args, remove=True)
            list_update("-prefer-ipv4", args)

        elif "mpv" in Config.PLAYER.get:
            list_update("--really-quiet", args)

    return [Config.PLAYER.get] + args + [stream['url']], songdata


def playsong(song, failcount=0, override=False):
    """ Play song using config.PLAYER called with args config.PLAYERARGS."""

    # pylint: disable=R0912
    # don't interrupt preloading:
    while song.ytid in g.preloading:
        writestatus("fetching item..")
        time.sleep(0.1)

    try:
        get_streams(song, force=failcount, callback=writestatus)

    except (IOError, URLError, HTTPError, socket.timeout) as e:
        dbg("--ioerror in playsong call to get_streams %s", uni(e))

        if "Youtube says" in uni(e):
            g.message = F('cant get track') % (song.title + " " + uni(e))
            return

        elif failcount < g.max_retries:
            dbg("--ioerror - trying next stream")
            failcount += 1
            return playsong(song, failcount=failcount, override=override)

        elif "pafy" in uni(e):
            g.message = uni(e) + " - " + song.ytid
            return

    except ValueError:
        g.message = F('track unresolved')
        dbg("----valueerror in playsong call to get_streams")
        return

    try:
        cmd, songdata = generate_real_playerargs(song, override, failcount)

    except (HTTPError) as e:

        # Fix for invalid streams (gh-65)
        dbg("----htterror in playsong call to gen_real_args %s", uni(e))
        if failcount < g.max_retries:
            failcount += 1
            return playsong(song, failcount=failcount, override=override)

    except IOError as e:
        # this may be cause by attempting to play a https stream with
        # mplayer
        g.message = c.r + uni(e) + c.w
        return

    songdata = "%s; %s; %s Mb" % songdata
    writestatus(songdata)
    dbg("%splaying %s (%s)%s", c.b, song.title, failcount, c.w)
    dbg("calling %s", " ".join(cmd))
    now = time.time()
    launch_player(song, songdata, cmd)
    fin = time.time()
    failed = fin - now < 1.25 and song.length > 2

    if failed and failcount < g.max_retries:
        dbg(c.r + "stream failed to open" + c.w)
        dbg("%strying again (attempt %s)%s", c.r, (2 + failcount), c.w)
        writestatus("error: retrying")
        time.sleep(1.2)
        failcount += 1
        playsong(song, failcount=failcount, override=override)


def launch_player(song, songdata, cmd):
    """ Launch player application. """

    try:

        if "mplayer" in Config.PLAYER.get:

            # fix for github issue 59
            if mswin and sys.version_info[:2] < (3, 0):
                cmd = [x.encode("utf8", errors="replace") for x in cmd]

            p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, bufsize=1)
            mplayer_status(p, songdata + ";", song.length)

        else:

            with open(os.devnull, "w") as devnull:
                subprocess.call(cmd, stderr=devnull)

    except OSError:
        g.message = F('no player') % Config.PLAYER.get
        return

    finally:
        try:
            p.terminate()  # make sure to kill mplayer if mpsyt crashes

        except (OSError, AttributeError, UnboundLocalError):
            pass


def mplayer_status(popen_object, prefix="", songlength=0):
    """ Capture time progress from player output. Write status line. """

    # A: 175.6
    re_mplayer = re.compile(r"A:\s*(?P<elapsed_s>\d+)\.\d\s*")
    last_displayed_line = None
    buff = ''

    while popen_object.poll() is None:
        char = popen_object.stdout.read(1).decode("utf-8", errors="ignore")

        if char in '\r\n':
            m = re_mplayer.match(buff)

            if m:
                line = make_status_line(m, songlength)

                if line != last_displayed_line:
                    writestatus(prefix + (" " if prefix else "") + line)
                    last_displayed_line = line

            buff = ''

        else:
            buff += char


def make_status_line(match_object, songlength=0):
    """ Format progress line output.  """

    progress_bar_size = Config.CONSOLE_WIDTH.get - 50

    try:
        elapsed_s = int(match_object.group('elapsed_s') or '0')

    except ValueError:
        return ""

    display_s = elapsed_s
    display_h = display_m = 0

    if elapsed_s >= 60:
        display_m = display_s // 60
        display_s %= 60

        if display_m >= 100:
            display_h = display_m // 60
            display_m %= 60

    pct = (float(elapsed_s) / songlength * 100) if songlength else 0

    status_line = "%02i:%02i:%02i %s" % (
        display_h, display_m, display_s,
        ("[%.0f%%]" % pct).ljust(6)
    )

    progress = int(math.ceil(pct / 100 * progress_bar_size))
    status_line += " [%s]" % ("=" * (progress - 1) +
                              ">").ljust(progress_bar_size, ' ')

    return status_line


def _search(url, progtext, qs=None, splash=True, pre_load=True):
    """ Perform memoized url fetch, display progtext. """

    g.message = "Searching for '%s%s%s'" % (c.y, progtext, c.w)

    # attach query string if supplied
    url = url + "?" + urlencode(qs) if qs else url
    # use cached value if exists
    if url in g.url_memo:
        songs = g.url_memo[url]

    # show splash screen during fetch
    else:
        if splash:
            g.content = logo(c.b) + "\n\n"
            screen_update()

        # perform fetch
        try:
            wdata = utf8_decode(g.urlopen(url).read())
            wdata = json.loads(wdata)
            songs = get_tracks_from_json(wdata)

        except (URLError, HTTPError) as e:
            g.message = F('no data') % e
            g.content = logo(c.r)
            return

    if songs and pre_load:
        # preload first result url
        kwa = {"song": songs[0], "delay": 0}
        t = threading.Thread(target=preload, kwargs=kwa)
        t.start()

    if songs:
        # cache resuls
        add_to_url_memo(url, songs[::])
        g.model.songs = songs
        return True

    return False


def generate_search_qs(term, page):
    """ Return query string. """

    aliases = dict(relevance="relevance", date="published", rating="rating",
                   views="viewCount")
    term = utf8_encode(term)
    qs = {
        'q': term,
        'v': 2,
        'alt': 'jsonc',
        'start-index': ((page - 1) * Config.MAX_RESULTS.get + 1) or 1,
        'safeSearch': "none",
        'max-results': Config.MAX_RESULTS.get,
        'paid-content': "false",
        'orderby': aliases[Config.ORDER.get]
    }

    if Config.SEARCH_MUSIC.get:
        qs['category'] = "Music"

    return qs


def usersearch(q_user, page=1, splash=True):
    """ Fetch uploads by a YouTube user. """

    query = generate_search_qs(q_user, page)
    #query['orderby'] = 'published'

    if query.get('category'):
        del query['category']

    # check whether this is a search within user uploads
    if "/" in q_user:
        user, _, term = (x.strip() for x in q_user.partition("/"))
        url = "https://gdata.youtube.com/feeds/api/videos"
        query['author'], query['q'] = user, term
        msg = "Results for {1}{3}{0} (by {2}{4}{0})"
        msg = msg.format(c.w, c.y, c.y, term, user)
        termuser = tuple([c.y + x + c.w for x in (term, user)])
        progtext = "%s by %s" % termuser
        failmsg = "No matching results for %s (by %s)" % termuser

    else:
        user = q_user
        del query['q']
        url = "https://gdata.youtube.com/feeds/api/users/%s/uploads" % user
        msg = "Video uploads by %s%s%s" % (c.y, user, c.w)
        failmsg = "User %s%s%s not found" % (c.y, user, c.w)
        progtext = user

    have_results = _search(url, progtext, query)

    if have_results:
        g.browse_mode = "normal"
        g.message = msg
        g.last_opened = ""
        g.last_search_query = {"user": q_user}
        g.current_page = page
        g.content = generate_songlist_display(frmat="search")

    else:
        g.message = failmsg
        g.current_page = 1
        g.last_search_query = {}
        g.content = logo(c.r)


def related_search(vitem, page=1, splash=True):
    """ Fetch uploads by a YouTube user. """

    query = generate_search_qs(vitem.ytid, page)
    del query['q']

    if query.get('category'):
        del query['category']

    url = "https://gdata.youtube.com/feeds/api/videos/%s/related"
    url, t = url % vitem.ytid, vitem.title
    ttitle = t[:48].strip() + ".." if len(t) > 49 else t

    have_results = _search(url, ttitle, query)

    if have_results:
        g.message = "Videos related to %s%s%s" % (c.y, ttitle, c.w)
        g.last_opened = ""
        g.last_search_query = {"related": vitem}
        g.current_page = page
        g.content = generate_songlist_display(frmat="search")

    else:
        g.message = "Related to %s%s%s not found" % (c.y, vitem.ytid, c.w)
        g.content = logo(c.r)
        g.current_page = 1
        g.last_search_query = {}


def search(term, page=1, splash=True):
    """ Perform search. """

    if not term or len(term) < 2:
        g.message = c.r + "Not enough input" + c.w
        g.content = generate_songlist_display()
        return

    original_term = term
    logging.info("search for %s", original_term)
    url = "https://gdata.youtube.com/feeds/api/videos"
    query = generate_search_qs(term, page)
    have_results = _search(url, original_term, query)

    if have_results:
        g.message = "Search results for %s%s%s" % (c.y, original_term, c.w)
        g.last_opened = ""
        g.last_search_query = {"term": original_term}
        g.browse_mode = "normal"
        g.current_page = page
        g.content = generate_songlist_display(frmat="search")

    else:
        g.message = "Found nothing for %s%s%s" % (c.y, term, c.w)
        g.content = logo(c.r)
        g.current_page = 1
        g.last_search_query = {}


def user_pls(user, page=1, splash=True):
    """ Retrieve use playlists. """

    user = {"is_user": True, "term": user}
    return pl_search(user, page=page, splash=splash)


def pl_search(term, page=1, splash=True, is_user=False):
    """ Search for YouTube playlists.

    term can be query str or dict indicating user playlist search.

    """

    if not term or len(term) < 2:
        g.message = c.r + "Not enough input" + c.w
        g.content = generate_songlist_display()
        return

    if isinstance(term, dict):
        is_user = term["is_user"]
        term = term["term"]

    # generate url base on whether this is a user playlist search
    x = "/users/%s/playlists?" % term if is_user else "/playlists/snippets?"
    url = "https://gdata.youtube.com/feeds/api%s" % x
    prog = "user: " + term if is_user else term
    logging.info("playlist search for %s", prog)
    start = (page - 1) * Config.MAX_RESULTS.get or 1
    qs = {"start-index": start,
          "max-results": Config.MAX_RESULTS.get, "v": 2, 'alt': 'jsonc'}

    # modify query string based on whether this is a user playlst search.
    if not is_user:
        qs["q"] = term

    url += urlencode(qs)

    if url in g.url_memo:
        playlists = g.url_memo[url]

    else:
        g.content = logo(c.g)
        g.message = "Searching playlists for %s" % c.y + prog + c.w
        screen_update()
        try:
            wpage = utf8_decode(g.urlopen(url).read())
            pldata = json.loads(wpage)
            playlists = get_pl_from_json(pldata)
        except HTTPError:
            playlists = None

    if playlists:
        add_to_url_memo(url, playlists[::])
        g.last_search_query = {"playlists": {"term": term, "is_user": is_user}}
        g.browse_mode = "ytpl"
        g.current_page = page
        g.ytpls = playlists
        g.message = "Playlist results for %s" % c.y + prog + c.w
        g.content = generate_playlist_display()

    else:
        g.message = "No playlists found for: %s" % c.y + prog + c.w
        g.content = generate_songlist_display(zeromsg=g.message)


def get_pl_from_json(pldata):
    """ Process json playlist data. """

    try:
        items = pldata['data']['items']

    except KeyError:
        items = []

    results = []
    for item in items:
        results.append(dict(link=item.get("id"),
                            size=item.get("size"),
                            title=item.get("title"),
                            author=item.get("author"),
                            created=item.get("created"),
                            updated=item.get("updated"),
                            description=item.get("description")
                            )
                       )
    return results


def paginate(items, pagesize, spacing=2, delim_fn=None):
    """ Paginate items to fit in pagesize.

    item size is defined by delim_fn.

    """

    dfn = lambda x: sum(1 for char in x if char == "\n")
    delim_fn = dfn or delim_fn
    pages = []
    currentpage = []
    roomleft = pagesize

    for item in items:
        itemsize = delim_fn(item) + spacing

        # check for oversized item, fit it on a page of its own
        if itemsize > pagesize:

            # but first end current page if has content
            if len(currentpage):
                pages.append(currentpage)

            # add large item on its own page
            pages.append([item])
            roomleft = pagesize
            currentpage = []

        else:

            # item is smaller than one page
            if itemsize < roomleft:
                # is there room on this page?, yes, fit it in
                currentpage.append(item)
                roomleft = roomleft - itemsize

            else:
                # no room on this page, start a new page
                pages.append(currentpage)
                currentpage = [item]
                roomleft = pagesize - itemsize

    # add final page if it has content
    if len(currentpage):
        pages.append(currentpage)

    return pages


def add_to_url_memo(key, value):
    """ Add to url memo, ensure url memo doesn't get too big. """

    g.url_memo[key] = value

    while len(g.url_memo) > 300:
        g.url_memo.popitem(last=False)

def fetch_comments(item):
    """ Fetch comments for item using gdata. """

    # pylint: disable=R0914
    pagesize = max(Config.MAX_RESULTS.get + 4, 10)
    ytid, title = item.ytid, item.title
    G = lambda x: c.g + x + c.w
    y = lambda x: c.y + x + c.w
    dbg("%sFetching coments for %s%s", c.y, y(ytid), c.w)
    writestatus("Fetching comments for %s" % y(title[:55]))
    url = ("https://gdata.youtube.com/feeds/api/videos/%s/comments?alt="
           "json&v=2&orderby=published&max-results=50" % ytid)

    if not url in g.url_memo:

        try:
            raw = utf8_decode(g.urlopen(url).read())
            add_to_url_memo(url, raw)

        except HTTPError:
            g.message = "No comments for %s" % item.title[:50]
            g.content = generate_songlist_display()
            return

    else:
        raw = g.url_memo[url]

    jsdata = json.loads(raw)
    coms = jsdata['feed'].get('entry', [])
    coms = [x for x in coms if x['content']['$t'].strip()]  # skip blanks

    if not len(coms):
        g.message = "No comments for %s" % item.title[:50]
        g.content = generate_songlist_display()
        return

    items = []

    for n, com in enumerate(coms, 1):
        poster = com['author'][0]['name']['$t']
        date = time.strftime("%c", yt_datetime(com['published']['$t'])[0])
        text = com['content']['$t']
        cid = ("%s/%s" % (n, len(coms)))
        out = ("%s %-35s %s\n" % (cid, G(poster), date))
        out += y(text.strip())
        items.append(out)

    plain = lambda x: x.replace(c.y, "").replace(c.w, "").replace(c.g, "")
    cw = Config.CONSOLE_WIDTH.get
    linecount = lambda x: sum(1 for char in x if char == "\n")
    longlines = lambda x: sum(len(plain(line)) // cw for line in x.split("\n"))
    linecounter = lambda x: linecount(x) + longlines(x)
    pages = paginate(items, pagesize=pagesize, delim_fn=linecounter)
    pagenum = 0

    while True and 0 <= pagenum < len(pages):
        pagecounter = "Page %s/%s" % (pagenum + 1, len(pages))
        page = pages[pagenum]
        pagetext = ("\n\n".join(page)).strip()
        content_length = linecount(pagetext) + longlines(pagetext)
        blanks = "\n" * (-2 + pagesize - content_length)
        g.content = pagetext + blanks
        screen_update()
        print("%s : Use [Enter] for next, [p] for previous, [q] to return:"
              % pagecounter, end="")
        v = xinput()

        if v == "p":
            pagenum -= 1

        elif not v:
            pagenum += 1

        else:
            break

    g.content = generate_songlist_display()


def comments(number):
    """ Receive use request to view comments. """

    if g.browse_mode == "normal":
        item = g.model.songs[int(number) - 1]
        fetch_comments(item)

    else:
        g.content = generate_songlist_display()
        g.message = "Comments only available for video items"


def _make_fname(song, ext=None, av=None):
    """" Create download directory, generate filename. """

    # pylint: disable=E1103
    # Instance of 'bool' has no 'extension' member (some types not inferable)
    if not os.path.exists(Config.DDIR.get):
        os.makedirs(Config.DDIR.get)

    streams = get_streams(song)

    if ext:
        extension = ext

    else:
        stream = select_stream(streams, 0, audio=av == "audio", m4a_ok=True)
        extension = stream['ext']

    filename = song.title[:59] + "." + extension
    filename = os.path.join(Config.DDIR.get,
                            mswinfn(filename.replace("/", "-")))
    return filename


def _download(song, filename, url=None, audio=False):
    """ Download file, show status, return filename. """
    # pylint: disable=R0914
    # too many local variables
    # Instance of 'bool' has no 'url' member (some types not inferable)

    print("Downloading to %s%s%s ..\n" % (c.r, filename, c.w))
    status_string = ('  {0}{1:,}{2} Bytes [{0}{3:.2%}{2}] received. Rate: '
                     '[{0}{4:4.0f} kbps{2}].  ETA: [{0}{5:.0f} secs{2}]')

    if not url:
        streams = get_streams(song)
        stream = select_stream(streams, 0, audio=audio, m4a_ok=True)
        url = stream['url']

    resp = g.urlopen(url)
    total = int(resp.info()['Content-Length'].strip())
    chunksize, bytesdone, t0 = 16384, 0, time.time()
    outfh = open(filename, 'wb')

    while True:
        chunk = resp.read(chunksize)
        outfh.write(chunk)
        elapsed = time.time() - t0
        bytesdone += len(chunk)
        rate = (bytesdone / 1024) / elapsed
        eta = (total - bytesdone) / (rate * 1024)
        stats = (c.y, bytesdone, c.w, bytesdone * 1.0 / total, rate, eta)

        if not chunk:
            outfh.close()
            break

        status = status_string.format(*stats)
        sys.stdout.write("\r" + status + ' ' * 4 + "\r")
        sys.stdout.flush()

    return filename


def _bi_range(start, end):
    """
    Inclusive range function, works for reverse ranges.

    eg. 5,2 returns [5,4,3,2] and 2, 4 returns [2,3,4]

    """
    if start == end:
        return (start,)

    elif end < start:
        return reversed(range(end, start + 1))

    else:
        return range(start, end + 1)


def _parse_multi(choice, end=None):
    """ Handle ranges like 5-9, 9-5, 5- and -5. Return list of ints. """

    end = end or uni(g.model.size)
    pattern = r'(?<![-\d])(\d+-\d+|-\d+|\d+-|\d+)(?![-\d])'
    items = re.findall(pattern, choice)
    alltracks = []

    for x in items:

        if x.startswith("-"):
            x = "1" + x

        elif x.endswith("-"):
            x = x + uni(end)

        if "-" in x:
            nrange = x.split("-")
            startend = map(int, nrange)
            alltracks += _bi_range(*startend)

        else:
            alltracks.append(int(x))

    return alltracks


def _get_near_name(begin, items):
    """ Return the closest matching playlist name that starts with begin. """

    for name in sorted(items):
        if name.lower().startswith(begin.lower()):
            break

    else:
        return begin

    return name


def play_pl(name):
    """ Play a playlist by name. """

    if name.isdigit():
        name = int(name)
        name = sorted(g.userpl)[name - 1]

    saved = g.userpl.get(name)

    if not saved:
        name = _get_near_name(name, g.userpl)
        saved = g.userpl.get(name)

    if saved:
        g.model.songs = list(saved.songs)
        play_all("", "", "")

    else:
        g.message = F("pl not found") % name
        g.content = playlists_display()
        #return


def save_last():
    """ Save command with no playlist name. """

    if g.last_opened:
        open_save_view("save", g.last_opened)

    else:
        saveas = ""

        #save using artist name in postion 1
        if not g.model.is_empty:
            saveas = g.model.songs[0].title[:18].strip()
            saveas = re.sub(r"[^-\w]", "-", saveas, re.UNICODE)

        # loop to find next available name
        post = 0

        while g.userpl.get(saveas):
            post += 1
            saveas = g.model.songs[0].title[:18].strip() + "-" + uni(post)

        open_save_view("save", saveas)


def open_save_view(action, name):
    """ Open, save or view a playlist by name.  Get closest name match. """

    if action == "open" or action == "view":

        saved = g.userpl.get(name)

        if not saved:
            name = _get_near_name(name, g.userpl)
            saved = g.userpl.get(name)

        if saved and action == "open":
            g.browse_mode = "normal"
            g.model.songs = g.active.songs = list(saved.songs)
            g.message = F("pl loaded") % name
            g.last_opened = name
            g.last_search_query = {}
            #g.content = generate_songlist_display()
            g.content = generate_songlist_display(frmat=None)
            kwa = {"song": g.model.songs[0], "delay": 0}
            t = threading.Thread(target=preload, kwargs=kwa)
            t.start()

        elif saved and action == "view":
            g.browse_mode = "normal"
            g.last_search_query = {}
            g.model.songs = list(saved.songs)
            g.message = F("pl viewed") % name
            g.last_opened = ""
            g.content = generate_songlist_display(frmat=None)
            #g.content = generate_songlist_display()
            kwa = {"song": g.model.songs[0], "delay": 0}
            t = threading.Thread(target=preload, kwargs=kwa)
            t.start()

        elif not saved and action in "view open".split():
            g.message = F("pl not found") % name
            g.content = playlists_display()

    elif action == "save":

        if not g.model.songs:
            g.message = "Nothing to save. " + F('advise search')
            g.content = generate_songlist_display()

        else:
            name = name.replace(" ", "-")
            g.userpl[name] = Playlist(name, list(g.model.songs))
            g.message = F('pl saved') % name
            save_to_file()
            g.content = generate_songlist_display(frmat=None)


# TODO = add many to playlist repeatedly saves playlist!  Change to one save


def open_view_bynum(action, num):
    """ Open or view a saved playlist by number. """

    srt = sorted(g.userpl)
    name = srt[int(num) - 1]
    open_save_view(action, name)


def songlist_rm_add(action, songrange):
    """ Remove or add tracks. works directly on user input. """

    selection = _parse_multi(songrange)

    if action == "add":

        for songnum in selection:
            g.active.songs.append(g.model.songs[songnum - 1])

        d = g.active.duration
        g.message = F('added to pl') % (len(selection), g.active.size, d)

    elif action == "rm":
        selection = list(reversed(sorted(list(set(selection)))))
        removed = uni(tuple(reversed(selection))).replace(",", "")

        for x in selection:
            g.model.songs.pop(x - 1)

        g.message = F('songs rm') % (len(selection), removed)

    g.content = generate_songlist_display()


def down_many(dltype, choice):
    """ Download multiple items. """

    choice = _parse_multi(choice)
    choice = list(set(choice))
    getsong = lambda item: g.model.songs[int(item) - 1]
    downsongs = [getsong(x) for x in choice]
    temp = g.model.songs[::]
    g.model.songs = downsongs[::]
    count = len(downsongs)
    av = "audio" if dltype.startswith("da") else "video"
    msg = ""

    def handle_error(message):
        """ Handle error in download. """

        g.message = message
        g.content = disp
        screen_update()
        time.sleep(2)
        g.model.songs.pop(0)

    try:
        for song in downsongs:
            disp = generate_songlist_display()
            title = "Download Queue (%s):%s\n\n" % (av, c.w)
            disp = re.sub(r"(Item\s*?Title.*?\n)", title, disp)
            g.content = disp
            screen_update()

            try:
                filename = _make_fname(song, None, av=av)

            except IOError as e:
                handle_error("Error for %s: %s" % (song.title, uni(e)))
                count -= 1
                continue

            except KeyError:
                handle_error("No audio track for %s" % song.title)
                count -= 1
                continue

            try:
                _download(song, filename, url=None, audio=av == "audio")

            except HTTPError:
                handle_error("HTTP Error for %s" % song.title)
                count -= 1
                continue

            g.model.songs.pop(0)
            msg = "Downloaded %s items" % count
            g.message = "Downloaded " + c.g + song.title + c.w

    except KeyboardInterrupt:
        msg = "Downloads interrupted!"

    finally:
        g.model.songs = temp[::]
        g.message = msg
        g.content = generate_songlist_display()


def play(pre, choice, post=""):
    """ Play choice.  Use repeat/random if appears in pre/post. """
    # pylint: disable=R0914
    # too many local variables

    if g.browse_mode == "ytpl":

        if choice.isdigit():
            return plist(g.ytpls[int(choice) - 1]['link'])

        else:
            g.message = "Invalid playlist selection: %s" % c.y + choice + c.w
            g.content = generate_songlist_display()
            return

    if not g.model.songs:
        g.message = c.r + "There are no tracks to select" + c.w
        g.content = g.content or generate_songlist_display()

    else:
        shuffle = "shuffle" in pre + post
        repeat = "repeat" in pre + post
        novid = "-a" in pre + post
        fs = "-f" in pre + post
        nofs = "-w" in pre + post

        if (novid and fs) or (novid and nofs) or (nofs and fs):
            raise IOError("Conflicting override options specified")

        override = False
        override = "audio" if novid else override
        override = "fullscreen" if fs else override
        override = "window" if nofs else override

        selection = _parse_multi(choice)
        songlist = [g.model.songs[x - 1] for x in selection]

        # cache next result of displayed items
        # when selecting a single item
        if len(songlist) == 1:
            chosen = selection[0] - 1

            if len(g.model.songs) > chosen + 1:
                nx = g.model.songs[chosen + 1]
                kwa = {"song": nx, "override": override}
                t = threading.Thread(target=preload, kwargs=kwa)
                t.start()

        play_range(songlist, shuffle, repeat, override)


def play_all(pre, choice, post=""):
    """ Play all tracks in model (last displayed). shuffle/repeat if req'd."""

    options = pre + choice + post
    play(options, "1-" + uni(len(g.model.songs)))


def ls():
    """ List user saved playlists. """

    if not g.userpl:
        g.message = F('no playlists')
        g.content = g.content or generate_songlist_display(zeromsg=g.message)

    else:
        g.content = playlists_display()
        g.message = F('pl help')


def vp():
    """ View current working playlist. """

    if g.active.is_empty:
        txt = F('advise search') if g.model.is_empty else F('advise add')
        g.message = F('pl empty') + " " + txt

    else:
        g.browse_mode = "normal"
        g.model.songs = g.active.songs
        g.message = F('current pl')

    g.content = generate_songlist_display(zeromsg=g.message)


def preload(song, delay=2, override=False):
    """  Get streams (runs in separate thread). """

    ytid = song.ytid
    g.preloading.append(ytid)
    time.sleep(delay)
    video = Config.SHOW_VIDEO.get
    video = True if override in ("fullscreen", "window") else video
    video = False if override == "audio" else video

    try:
        stream = get_streams(song)
        m4a = not Config.PLAYER.get == "mplayer"
        stream = select_stream(stream, audio=not video, m4a_ok=m4a)

        if not stream and not video:
            # preload video stream, no audio available
            stream = select_stream(g.streams[ytid], audio=False)

        get_size(ytid, stream['url'], preloading=True)

    except (ValueError, AttributeError, IOError) as e:
        dbg(e)  # Fail silently on preload

    finally:
        g.preloading.remove(song.ytid)


def reset_terminal():
    """ Reset terminal control character and modes for non Win OS's. """

    if not mswin:
        subprocess.call(["tset", "-c"])


def play_range(songlist, shuffle=False, repeat=False, override=False):
    """ Play a range of songs, exit cleanly on keyboard interrupt. """

    if shuffle:
        random.shuffle(songlist)

    if not repeat:

        for n, song in enumerate(songlist):
            g.content = playback_progress(n, songlist, repeat=False)

            if not g.command_line:
                screen_update()

            hasnext = len(songlist) > n + 1

            if hasnext:
                nex = songlist[n + 1]
                kwa = {"song": nex, "override": override}
                t = threading.Thread(target=preload, kwargs=kwa)
                t.start()

            try:
                playsong(song, override=override)

            except KeyboardInterrupt:
                logging.info("Keyboard Interrupt")
                print(c.w + "Stopping...                          ")
                reset_terminal()
                g.message = c.y + "Playback halted" + c.w
                break

    elif repeat:

        while True:
            try:
                for n, song in enumerate(songlist):
                    g.content = playback_progress(n, songlist, repeat=True)
                    screen_update()
                    hasnext = len(songlist) > n + 1

                    if hasnext:
                        nex = songlist[n + 1]
                        kwa = {"song": nex, "override": override}
                        t = threading.Thread(target=preload, kwargs=kwa)
                        t.start()

                    playsong(song, override=override)
                    g.content = generate_songlist_display()

            except KeyboardInterrupt:
                print(c.w + "Stopping...                          ")
                reset_terminal()
                g.message = c.y + "Playback halted" + c.w
                break

    g.content = generate_songlist_display()


def show_help(choice):
    """ Print help message. """

    helps = {"download": ("playback dl listen watch show repeat playing"
                          "show_video playurl dlurl d da dv all *"
                          " play".split()
                          ),

             "invoke": "command commands mpsyt invocation".split(),

             "search": ("user userpl pl pls r n p url album "
                        "editing result results related remove swop".split()),

             "edit": ("editing manupulate manipulating rm mv sw edit move "
                      "swap shuffle".split()),

             "tips": ("undump dump -f -w -a adv advanced".split(" ")),

             "basic": ("basic comment basics c comments u i".split()),

             "config": ("set checkupdate colours colors ddir directory player "
                        "arguments args playerargs music search_music keys "
                        "status show_status show_video video configuration "
                        "fullscreen full screen folder player mpv mplayer"
                        " settings default reset configure audio results "
                        "max_results size lines rows height window "
                        "position window_pos quality resolution max_res "
                        "columns width console".split()),

             "playlists": ("save rename delete move rm ls mv sw add vp open"
                           " view".split())
             }

    for topic, aliases in helps.items():

        if choice in aliases:
            choice = topic
            break

    choice = "menu" if not choice else choice
    out, all_help = "", g.helptext
    help_names = [x[0] for x in all_help]
    choice = _get_near_name(choice, help_names)

    if choice == "menu" or not choice in help_names:
        out += "  %sHelp Topics%s" % (c.ul, c.w)
        out += F('help topic', 2, 1)

        for x in all_help:
            out += ("\n%s     %-10s%s : %s" % (c.y, x[0], c.w, x[1]))

        out += "\n"
        g.content = out

    else:
        indent = lambda x: "\n  ".join(x.split("\n"))
        choice = help_names.index(choice)
        g.content = indent(all_help[choice][2])


def quits(showlogo=True):
    """ Exit the program. """

    if has_readline:
        readline.write_history_file(g.READLINE_FILE)
        dbg("Saved history file")

    savecache()

    msg = g.blank_text + logo(c.r, version=__version__) if showlogo else ""
    vermsg = ""
    print(msg + F("exitmsg", 2))

    if Config.CHECKUPDATE.get and showlogo:
        try:
            url = "https://github.com/np1/mps-youtube/raw/master/VERSION"
            v = utf8_decode(g.urlopen(url).read())
            v = re.search(r"^version\s*([\d\.]+)\s*$", v, re.MULTILINE)
            if v:
                v = v.group(1)
                if v > __version__:
                    vermsg += "\nA newer version is available (%s)\n" % v
        except (URLError, HTTPError, socket.timeout):
            pass

    sys.exit(vermsg)


def get_dl_data(song, mediatype="any"):
    """ Get filesize and metadata for all streams, return dict. """

    mbsize = lambda x: uni(int(x / (1024 ** 2)))

    p = get_pafy(song)
    dldata = []
    text = " [Fetching stream info] >"
    streams = [x for x in p.allstreams]

    if mediatype == "audio":
        streams = [x for x in p.audiostreams]

    l = len(streams)
    for n, stream in enumerate(streams):
        sys.stdout.write(text + "-" * n + ">" + " " * (l - n - 1) + "<\r")
        sys.stdout.flush()
        #---- line below can cause TypeError from pafy line 67 makeurl
        #---- raw += "&signature=" + sig
        #---- sig is NoneType
        try:
            size = mbsize(stream.get_filesize())

        except TypeError:
            dbg(c.r + "---Error getting stream size" + c.w)
            size = 0

        item = {'mediatype': stream.mediatype,
                'size': size,
                'ext': stream.extension,
                'quality': stream.quality,
                'notes': getattr(stream, "notes", ""),  # getattr for backward
                                                        # pafy compatibility
                'url': stream.url}

        dldata.append(item)

    writestatus("")
    return dldata, p


def menu_prompt(model, prompt=" > ", rows=None, header=None, theading=None,
                footer=None, force=0):
    """ Generate a list of choice, returns item from model. """

    content = ""

    for x in header, theading, rows, footer:
        if type(x) == list:

            for line in x:
                content += line + "\n"

        elif type(x) == str:
            content += x + "\n"

    g.content = content
    screen_update()

    choice = xinput(prompt)

    if choice in model:
        return model[choice]

    elif force:
        return menu_prompt(model, prompt, rows, header, theading, footer,
                           force)

    elif not choice.strip():
        return False, False

    else:  # unrecognised input
        return False, "abort"


def prompt_dl(song):
    """ Prompt user do choose a stream to dl.  Return (url, extension). """

    # pylint: disable=R0914
    dl_data, p = get_dl_data(song)
    dl_text = gen_dl_text(dl_data, song, p)

    model = [x['url'] for x in dl_data]
    ed = enumerate(dl_data)
    model = {uni(n + 1): (x['url'], x['ext']) for n, x in ed}
    url, ext = menu_prompt(model, "Download number: ", *dl_text)
    url2 = ext2 = None

    muxapp = has_exefile("avconv") or has_exefile("ffmpeg")
    if ext == "m4v" and muxapp:
        dl_data, p = get_dl_data(song, mediatype="audio")
        dl_text = gen_dl_text(dl_data, song, p)
        au_choices = "1" if len(dl_data) == 1 else "1-%s" % len(dl_data)
        footer = [F('-audio'), F('select mux') % au_choices]
        dl_text = tuple(dl_text[0:3]) + (footer,)
        aext = ("ogg", "m4a")
        model = [x['url'] for x in dl_data if x['ext'] in aext]
        ed = enumerate(dl_data)
        model = {uni(n + 1): (x['url'], x['ext']) for n, x in ed}
        prompt = "Audio stream: "
        url2, ext2 = menu_prompt(model, prompt, *dl_text)

    return url, ext, url2, ext2


def gen_dl_text(ddata, song, p):
    """ Generate text for dl screen. """

    hdr = []
    hdr.append("  %s%s%s" % (c.r, song.title, c.w))
    author = utf8_decode(p.author)
    hdr.append(c.r + "  Uploaded by " + author + c.w)
    hdr.append("  [" + fmt_time(song.length) + "]")
    hdr.append("")

    heading = tuple("Item Format Quality Media Size Notes".split())
    fmt = "  {0}%-6s %-8s %-13s %-7s   %-5s   %-16s{1}"
    heading = [fmt.format(c.w, c.w) % heading]
    heading.append("")

    content = []

    for n, d in enumerate(ddata):
        row = (n + 1, d['ext'], d['quality'], d['mediatype'], d['size'],
               d['notes'])
        fmt = "  {0}%-6s %-8s %-13s %-7s %5s Mb   %-16s{1}"
        row = fmt.format(c.g, c.w) % row
        content.append(row)

    content.append("")

    footer = "Select [%s1-%s%s] to download or [%sEnter%s] to return"
    footer = [footer % (c.y, len(content) - 1, c.w, c.y, c.w)]
    return(content, hdr, heading, footer)


def download(dltype, num):
    """ Download a track. """

    # This function needs refactoring!
    # pylint: disable=R0912
    # pylint: disable=R0914

    if g.browse_mode != "normal":
        g.message = "Download must refer to a specific video item"
        g.message = c.y + g.message + c.w
        g.content = generate_songlist_display()
        return

    writestatus("Fetching video info...")
    song = (g.model.songs[int(num) - 1])
    best = dltype.startswith("dv") or dltype.startswith("da")

    if not best:

        try:
            # user prompt for download stream
            url, ext, url_au, ext_au = prompt_dl(song)

        except KeyboardInterrupt:
            g.message = c.r + "Download aborted!" + c.w
            g.content = generate_songlist_display()
            return

        if not url or ext_au == "abort":
            # abort on invalid stream selection
            g.content = generate_songlist_display()
            g.message = "%sNo download selected / invalid input%s" % (c.y, c.w)
            return

        else:
            # download user selected stream(s)
            filename = _make_fname(song, ext)
            args = (song, filename, url)
            kwargs = {}

            if url_au and ext_au:
                filename_au = _make_fname(song, ext_au)
                args_au = (song, filename_au, url_au)

    elif best:
        # set updownload without prompt
        url_au = None
        av = "audio" if dltype.startswith("da") else "video"
        audio = av == "audio"
        filename = _make_fname(song, None, av=av)
        args = (song, filename)
        kwargs = dict(url=None, audio=audio)

    try:
        # perform download(s)
        dl_filenames = [args[1]]
        f = _download(*args, **kwargs)
        g.message = "Downloaded " + c.g + f + c.w

        if url_au:
            dl_filenames += [args_au[1]]
            _download(*args_au, **kwargs)

    except KeyboardInterrupt:
        g.message = c.r + "Download halted!" + c.w

        try:
            for downloaded in dl_filenames:
                os.remove(downloaded)

        except IOError:
            pass

    if url_au:
        # multiplex
        muxapp = has_exefile("avconv") or has_exefile("ffmpeg")
        mux_cmd = "APP -i BISH -vcodec h264 -i BASH -acodec copy -map 0:v:0"
        mux_cmd += " -map 1:a:0 -threads 2 BOSH"
        mux_cmd = mux_cmd.split()
        mux_cmd[2], mux_cmd[6] = args[1], args_au[1]
        mux_cmd[0], mux_cmd[15] = muxapp, args[1][:-3] + "mp4"

        try:
            subprocess.call(mux_cmd)
            g.message = "Saved to :" + c.g + mux_cmd[15] + c.w
            os.remove(args[1])
            os.remove(args_au[1])

        except KeyboardInterrupt:
            g.message = "Audio/Video multiplex aborted!"

    g.content = generate_songlist_display()


def prompt_for_exit():
    """ Ask for exit confirmation. """

    g.message = c.r + "Press ctrl-c again to exit" + c.w
    g.content = generate_songlist_display()
    screen_update()

    try:
        userinput = xinput(c.r + " > " + c.w)

    except (KeyboardInterrupt, EOFError):
        quits(showlogo=False)

    return userinput


def playlist_remove(name):
    """ Delete a saved playlist by name - or purge working playlist if *all."""

    if name.isdigit() or g.userpl.get(name):

        if name.isdigit():
            name = int(name) - 1
            name = sorted(g.userpl)[name]

        del g.userpl[name]
        g.message = "Deleted playlist %s%s%s" % (c.y, name, c.w)
        g.content = playlists_display()
        save_to_file()

    else:
        g.message = F('pl not found advise ls') % name
        g.content = playlists_display()


def songlist_mv_sw(action, a, b):
    """ Move a song or swap two songs. """

    i, j = int(a) - 1, int(b) - 1

    if action == "mv":
        g.model.songs.insert(j, g.model.songs.pop(i))
        g.message = F('song move') % (g.model.songs[j].title, b)

    elif action == "sw":
        g.model.songs[i], g.model.songs[j] = g.model.songs[j], g.model.songs[i]
        g.message = F('song sw') % (min(a, b), max(a, b))

    g.content = generate_songlist_display()


def playlist_add(nums, playlist):
    """ Add selected song nums to saved playlist. """

    nums = _parse_multi(nums)

    if not g.userpl.get(playlist):
        playlist = playlist.replace(" ", "-")
        g.userpl[playlist] = Playlist(playlist)

    for songnum in nums:
        g.userpl[playlist].songs.append(g.model.songs[songnum - 1])
        dur = g.userpl[playlist].duration
        f = (len(nums), playlist, g.userpl[playlist].size, dur)
        g.message = F('added to saved pl') % f
        save_to_file()

    g.content = generate_songlist_display()


def playlist_rename_idx(_id, name):
    """ Rename a playlist by ID. """

    _id = int(_id) - 1
    playlist_rename(sorted(g.userpl)[_id] + " " + name)


def playlist_rename(playlists):
    """ Rename a playlist using mv command. """

    # Deal with old playlist names that permitted spaces
    a, b = "", playlists.split(" ")
    while a not in g.userpl:
        a = (a + " " + (b.pop(0))).strip()
        if not b and not a in g.userpl:
            g.message = F('no pl match for rename')
            g.content = g.content or playlists_display()
            return

    b = "-".join(b)
    g.userpl[b] = Playlist(b)
    g.userpl[b].songs = list(g.userpl[a].songs)
    playlist_remove(a)
    g.message = F('pl renamed') % (a, b)
    save_to_file()


def add_rm_all(action):
    """ Add all displayed songs to current playlist.

    remove all displayed songs from view.

    """

    if action == "rm":
        for n in reversed(range(0, len(g.model.songs))):
            g.model.songs.pop(n)
        g.message = c.b + "Cleared all songs" + c.w
        g.content = generate_songlist_display()

    elif action == "add":
        size = g.model.size
        songlist_rm_add("add", "-" + uni(size))


def nextprev(np):
    """ Get next / previous search results. """

    glsq = g.last_search_query
    content = g.model.songs

    if "user" in g.last_search_query:
        function, query = usersearch, glsq['user']

    elif "related" in g.last_search_query:
        function, query = related_search, glsq['related']

    elif "term" in g.last_search_query:
        function, query = search, glsq['term']

    elif "playlists" in g.last_search_query:
        function, query = pl_search, glsq['playlists']
        content = g.ytpls

    elif "playlist" in g.last_search_query:
        function, query = plist, glsq['playlist']

    good = False

    if np == "n":
        if len(content) == Config.MAX_RESULTS.get and glsq:
            g.current_page += 1
            good = True

    elif np == "p":
        if g.current_page > 1 and g.last_search_query:
            g.current_page -= 1
            good = True

    if good:
        function(query, g.current_page, splash=True)
        g.message += " : page %s" % g.current_page

    else:
        norp = "next" if np == "n" else "previous"
        g.message = "No %s items to display" % norp

    g.content = generate_songlist_display(frmat="search")


def user_more(num):
    """ Show more videos from user of vid num. """

    if g.browse_mode != "normal":
        g.message = "User uploads must refer to a specific video item"
        g.message = c.y + g.message + c.w
        g.content = generate_songlist_display()
        return

    item = g.model.songs[int(num) - 1]
    p = get_pafy(item)
    user = p.username
    usersearch(user)


def related(num):
    """ Show videos related to to vid num. """

    if g.browse_mode != "normal":
        g.message = "Related items must refer to a specific video item"
        g.message = c.y + g.message + c.w
        g.content = generate_songlist_display()
        return

    item = g.model.songs[int(num) - 1]
    related_search(item)


def info(num):
    """ Get video description. """

    if g.browse_mode == "ytpl":
        p = g.ytpls[int(num) - 1]

        # fetch the playlist item as it has more metadata
        yt_playlist = g.pafy_pls.get(p['link'])

        if not yt_playlist:
            g.content = logo(col=c.g)
            g.message = "Fetching playlist info.."
            screen_update()
            dbg("%sFetching playlist using pafy%s", c.y, c.w)
            yt_playlist = pafy.get_playlist(p['link'])
            g.pafy_pls[p['link']] = yt_playlist

        ytpl_likes = yt_playlist.get('likes', 0)
        ytpl_dislikes = yt_playlist.get('dislikes', 0)
        ytpl_desc = yt_playlist.get('description', "")
        g.content = generate_songlist_display()

        #created = time.strptime(p['created'], "%Y-%m-%dT%H:%M:%S.000Z")
        #updated = time.strptime(p['updated'], "%Y-%m-%dT%H:%M:%S.000Z")
        created = yt_datetime(p['created'])[0]
        updated = yt_datetime(p['updated'])[0]
        out = c.ul + "Playlist Info" + c.w + "\n\n"
        out += p['title']
        out += "\n" + ytpl_desc
        out += ("\n\nAuthor     : " + p['author'])
        out += "\nSize       : " + uni(p['size']) + " videos"
        out += "\nLikes      : " + uni(ytpl_likes)
        out += "\nDislikes   : " + uni(ytpl_dislikes)
        out += "\nCreated    : " + time.strftime("%x %X", created)
        out += "\nUpdated    : " + time.strftime("%x %X", updated)
        out += "\nID         : " + uni(p['link'])
        out += ("\n\n%s[%sPress enter to go back%s]%s" % (c.y, c.w, c.y, c.w))
        g.content = out

    elif g.browse_mode == "normal":
        g.content = logo(c.b)
        screen_update()
        writestatus("Fetching video metadata..")
        item = (g.model.songs[int(num) - 1])
        get_streams(item)
        p = get_pafy(item)
        i = utf8_decode
        pub = time.strptime(uni(p.published), "%Y-%m-%d %H:%M:%S")
        writestatus("Fetched")
        up = "Update Pafy to 0.3.42 to view likes/dislikes"
        out = c.ul + "Video Info" + c.w + "\n\n"
        out += i(p.title or "")
        out += "\n" + (p.description or "")
        out += i("\n\nAuthor     : " + uni(p.author))
        out += i("\nPublished  : " + time.strftime("%c", pub))
        out += i("\nView count : " + uni(p.viewcount))
        out += i("\nRating     : " + uni(p.rating)[:4])
        out += i("\nLikes      : " + uni(getattr(p, "likes", up)))
        out += i("\nDislikes   : " + uni(getattr(p, "dislikes", up)))
        out += i("\nCategory   : " + p.category)
        out += i("\nLink       : " + "https://youtube.com/watch?v=%s" %
                 p.videoid)
        out += i("\n\n%s[%sPress enter to go back%s]%s" % (c.y, c.w, c.y, c.w))
        g.content = out


def play_url(url, override):
    """ Open and play a youtube video url. """

    override = override if override else "_"
    g.browse_mode = "normal"
    yt_url(url, print_title=1)

    if len(g.model.songs) == 1:
        play(override, "1", "_")

    if g.command_line:
        sys.exit("")


def dl_url(url):
    """ Open and prompt for download of youtube video url. """

    g.browse_mode = "normal"
    yt_url(url)

    if len(g.model.songs) == 1:
        download("download", "1")

    if g.command_line:
        sys.exit("")


def yt_url(url, print_title=0):
    """ Acess a video by url. """

    try:
        p = pafy.new(url, basic=1, signature=0)

    except (IOError, ValueError) as e:
        g.message = c.r + uni(e) + c.w
        g.content = g.content or generate_songlist_display(zeromsg=g.message)
        return

    g.browse_mode = "normal"
    v = Video(p.videoid, utf8_decode(p.title), p.length)
    g.model.songs = [v]

    if not g.command_line:
        g.content = generate_songlist_display()

    if print_title:
        print(v.title)


def dump(un):
    """ Show entire playlist. """

    if g.last_search_query.get("playlist") and not un:
        plist(g.last_search_query['playlist'], dumps=True)

    elif g.last_search_query.get("playlist") and un:
        plist(g.last_search_query['playlist'], pagenum=1, dumps=False)

    else:
        un = "" if not un else un
        g.message = "%s%sdump%s may only be used on an open YouTube playlist"
        g.message = g.message % (c.y, un, c.w)
        g.content = generate_songlist_display()


def plist(parturl, pagenum=1, splash=True, dumps=False):
    """ Import playlist created on website. """

    if "playlist" in g.last_search_query and\
            parturl == g.last_search_query['playlist']:

        # go to pagenum
        s = (pagenum - 1) * Config.MAX_RESULTS.get
        e = pagenum * Config.MAX_RESULTS.get

        if dumps:
            s, e = 0, 99999

        g.model.songs = g.ytpl['items'][s:e]
        g.content = generate_songlist_display()
        g.message = "Showing YouTube playlist: %s" % c.y + g.ytpl['name'] + c.w
        g.current_page = pagenum
        return

    if splash:
        g.content = logo(col=c.b)
        g.message = "Retreiving YouTube playlist"
        screen_update()

    dbg("%sFetching playlist using pafy%s", c.y, c.w)
    yt_playlist = pafy.get_playlist(parturl)
    g.pafy_pls[parturl] = yt_playlist
    ytpl_items = yt_playlist['items']
    ytpl_title = yt_playlist['title']
    g.content = generate_songlist_display()
    songs = []

    for item in ytpl_items:
        # Create Video object, appends to songs
        cur = Video(ytid=item['pafy'].videoid,
                    title=item['pafy'].title,
                    length=item['pafy'].length)
        songs.append(cur)

    if not ytpl_items:
        dbg("got unexpected data or no search results")
        return False

    g.last_search_query = {"playlist": parturl}
    g.browse_mode = "normal"
    g.ytpl = dict(name=ytpl_title, items=songs)
    g.current_page = 1
    g.model.songs = songs[:Config.MAX_RESULTS.get]
    # preload first result url
    kwa = {"song": songs[0], "delay": 0}
    t = threading.Thread(target=preload, kwargs=kwa)
    t.start()

    g.content = generate_songlist_display()
    g.message = "Showing YouTube playlist %s" % (c.y + ytpl_title + c.w)


def shuffle_fn(_):
    """ Shuffle displayed items. """

    random.shuffle(g.model.songs)
    g.message = c.y + "Items shuffled" + c.w
    g.content = generate_songlist_display()


def clearcache():
    """ Clear cached items - for debugging use. """

    g.pafs = {}
    g.streams = {}
    dbg("%scache cleared%s", c.p, c.w)
    g.message = "cache cleared"


def show_message(message, col=c.r, update=False):
    """ Show message using col, update screen if required. """

    g.content = generate_songlist_display()
    g.message = col + message + c.w

    if update:
        screen_update()



def _do_query(url, query, err='query failed', cache=True, report=False):
    """ Perform http request.

    if cache is True, memo is utilised
    if report is True, return whether response is from memo

    """

    # convert query to sorted list of tuples (needed for consistent url_memo)
    query = [(k, query[k]) for k in sorted(query.keys())]
    url = "%s?%s" % (url, urlencode(query))

    #if cache and g.memo.get(url):
        #return g.memo.get(url) if not report else (g.memo.get(url), True)

    try:
        wdata = utf8_decode(g.urlopen(url).read())

    except (URLError, HTTPError) as e:
        g.message = "%s: %s (%s)" % (err, e, url)
        g.content = logo(c.r)
        return None if not report else (None, False)

    #if cache and wdata:
        #g.memo.add(url, wdata)

    return wdata if not report else (wdata, False)


def _best_song_match(songs, title, duration):
    """ Select best matching song based on title, length.

    Score from 0 to 1 where 1 is best.

    """

    # pylint: disable=R0914
    seqmatch = difflib.SequenceMatcher
    variance = lambda a, b: float(abs(a - b)) / max(a, b)
    candidates = []

    ignore = "music video lyrics new lyrics video audio".split()
    extra = "official original vevo".split()


    for song in songs:
        dur, tit = int(song.length), song.title
        dbg("Title: %s, Duration: %s", tit, dur)

        for word in extra:
            if word in tit.lower() and not word in title.lower():
                pattern = re.compile(word, re.I)
                tit = pattern.sub("", tit)

        for word in ignore:
            if word in tit.lower() and not word in title.lower():
                pattern = re.compile(word, re.I)
                tit = pattern.sub("", tit)

        replacechars = re.compile(r"[\]\[\)\(\-]")
        tit = replacechars.sub(" ", tit)
        multiple_spaces = re.compile(r"(\s)(\s*)")
        tit = multiple_spaces.sub(r"\1", tit)

        title_score = seqmatch(None, title.lower(), tit.lower()).ratio()
        duration_score = 1 - variance(duration, dur)
        dbg("Title score: %s, Duration score: %s", title_score,
            duration_score)

        # apply weightings
        score = duration_score * .5 + title_score * .5
        candidates.append((score, song))

    best_score, best_song = max(candidates, key=lambda x: x[0])
    percent_score = int(100 * best_score)
    return best_song, percent_score


def _match_tracks(artist, title, mb_tracks):
    """ Match list of tracks in mb_tracks by performing multiple searches. """

    #pylint: disable=R0914
    dbg("artists is %s", artist)
    dbg("title is %s", title)
    title_artist_str = c.g + title + c.w, c.g + artist + c.w
    xprint("\nSearching for %s by %s\n\n" % title_artist_str)
    dtime = lambda x: time.strftime('%M:%S', time.gmtime(int(x)))

    # do matching
    for track in mb_tracks:
        ttitle = track['title']
        length = track['length']
        xprint("Search :  %s%s - %s%s - %s" % (c.y, artist, ttitle, c.w,
                                               dtime(length)))
        #q = utf8_encode("%s %s" % (ttitle, artist))
        #q = utf8_encode(ttitle) if artist == "Various Artists" else q
        #w = q + utf8_encode(" -cover -guitar -piano")
        q = "%s %s" % (artist, ttitle)
        w = q = ttitle if artist == "Various Artists" else q
        #ignore = "guitar piano cover karaoke".split()

        #for word in ignore:
            #if not word in w.lower():
                #w += " -%s" % word

        url = "https://gdata.youtube.com/feeds/api/videos"
        query = generate_search_qs(w, 1)
        dbg(query)
        have_results = _search(url, q, query, splash=False, pre_load=False)
        time.sleep(0.5)

        if not have_results:
            print(c.r + "Nothing matched :(\n" + c.w)
            continue

        results = g.model.songs
        s, score = _best_song_match(results, artist + " " + ttitle, length)
        cc = c.g if score > 85 else c.y
        cc = c.r if score < 75 else cc
        xprint("Matched:  %s%s%s - %s \n[%sMatch confidence: "
               "%s%s]\n" % (c.y, s.title, c.w, fmt_time(s.length), cc, score, c.w))
        yield s


def _get_mb_tracks(albumid):
    """ Get track listing from MusicBraiz by album id. """

    ns = {'mb': 'http://musicbrainz.org/ns/mmd-2.0#'}
    url = "http://musicbrainz.org/ws/2/release/" + albumid
    query = {"inc": "recordings"}
    wdata = _do_query(url, query, err='album search error')

    if not wdata:
        return None

    root = ET.fromstring(utf8_encode(wdata))
    tlist = root.find("./mb:release/mb:medium-list/mb:medium/mb:track-list",
                      namespaces=ns)
    mb_songs = tlist.findall("mb:track", namespaces=ns)
    tracks = []
    path = "./mb:recording/mb:"

    for track in mb_songs:

        try:
            title, length, rawlength = "unknown", 0, 0
            title = track.find(path + "title", namespaces=ns).text
            rawlength = track.find(path + "length", namespaces=ns).text
            length = int(round(float(rawlength) / 1000))

        except (ValueError, AttributeError):
            xprint("not found")

        tracks.append(dict(title=title, length=length, rawlength=rawlength))

    return tracks


def _get_mb_album(albumname, **kwa):
    """ Return artist, album title and track count from MusicBrainz. """

    url = "http://musicbrainz.org/ws/2/release/"
    qargs = dict(
        release='"%s"' % albumname,
        primarytype=kwa.get("primarytype", "album"),
        status=kwa.get("status", "official"))
    qargs.update({k: '"%s"' % v for k, v in kwa.items()})
    qargs = ["%s:%s" % item for item in qargs.items()]
    qargs = {"query": " AND ".join(qargs)}
    g.message = "Album search for '%s%s%s'" % (c.y, albumname, c.w)
    wdata = _do_query(url, qargs)

    if not wdata:
        return None

    ns = {'mb': 'http://musicbrainz.org/ns/mmd-2.0#'}
    root = ET.fromstring(utf8_encode(wdata))
    rlist = root.find("mb:release-list", namespaces=ns)

    if int(rlist.get('count')) == 0:
        return None

    album = rlist.find("mb:release", namespaces=ns)
    artist = album.find("./mb:artist-credit/mb:name-credit/mb:artist",
                        namespaces=ns).find("mb:name", namespaces=ns).text
    title = album.find("mb:title", namespaces=ns).text
    aid = album.get('id')
    return dict(artist=artist, title=title, aid=aid)


def search_album(term, page=1, splash=True):
    """Search for albums. """

    #pylint: disable=R0914,R0912
    if not term:
        show_message("Enter album name:", c.g, update=True)
        term = xinput("> ")

        if not term or len(term) < 2:
            g.message = c.r + "Not enough input!" + c.w
            g.content = generate_songlist_display()
            return

    album = _get_mb_album(term)

    if not album:
        show_message("Album '%s' not found!" % term)
        return

    out = "'%s' by %s%s%s\n\n" % (album['title'],
                                  c.g, album['artist'], c.w)
    out += ("[Enter] to continue, [q] to abort, or enter artist name for:\n"
            "    %s" % (c.y + term + c.w + "\n"))

    g.message, g.content = out, logo(c.b)
    screen_update()
    prompt = "Artist? [%s] > " % album['artist']
    xprint(prompt, end="")
    artistentry = xinput().strip()

    if artistentry:

        if artistentry == "q":
            show_message("Album search abandoned!")
            return

        album = _get_mb_album(term, artist=artistentry)

        if not album:
            show_message("Album '%s' by '%s' not found!" % (term, artistentry))
            return

    title, artist = album['title'], album['artist']
    mb_tracks = _get_mb_tracks(album['aid'])

    if not mb_tracks:
        show_message("Album '%s' by '%s' has 0 tracks!" % (title, artist))
        return


    msg = "%s%s%s by %s%s%s\n\n" % (c.g, title, c.w, c.g, artist, c.w)
    msg += "Enter to begin matching or [q] to abort"
    g.message = msg
    g.content = "Tracks:\n"
    for n, track in enumerate(mb_tracks, 1):
        g.content += "%02s  %s" % (n, track['title'])
        g.content += "\n"

    #g.content = logo(c.b) + "\n\n"
    screen_update()
    entry = xinput("Continue? [Enter] > ")

    if entry == "":
        pass

    else:
        show_message("Album search abandoned!")
        return

    songs = []
    print(g.blank_text)
    itt = _match_tracks(artist, title, mb_tracks)

    stash = Config.SEARCH_MUSIC.get, Config.ORDER.get, Config.MAX_RESULTS.get
    Config.SEARCH_MUSIC.value = True
    Config.MAX_RESULTS.value = 50
    Config.ORDER.value = "relevance"


    try:
        while True:
            songs.append(next(itt))

    except KeyboardInterrupt:
        print("%sHalted!%s" % (c.r, c.w))

    except StopIteration:
        pass

    finally:
        (Config.SEARCH_MUSIC.value, Config.ORDER.value,
         Config.MAX_RESULTS.value) = stash


    if songs:
        g.model.songs = songs
        kwa = {"song": songs[0], "delay": 0}
        t = threading.Thread(target=preload, kwargs=kwa)
        t.start()
        print("\n%s / %s songs matched" % (len(songs), len(mb_tracks)))
        xinput("Press Enter to continue")
        g.message = "Contents of album %s%s - %s%s %s(%d/%d)%s:" % (
            c.y, artist, title, c.w, c.b, len(songs), len(mb_tracks), c.w)
        g.last_opened = ""
        g.last_search_query = ""
        g.current_page = page
        g.content = generate_songlist_display()

    else:
        g.message = "Found no album tracks for %s%s%s" % (c.y, title, c.w)
        g.content = generate_songlist_display()
        g.current_page = 1
        g.last_search_query = ""


g.helptext = [("basic", "Basics", """

{0}Basic Usage{1}

Use {2}/{1} or {2}.{1} to prefix your search query.  e.g., {2}/pink floyd{1}

Then, when results are shown:

    {2}<number(s)>{1} - play specified items, separated by commas.
                  e.g., {2}1-3,5{1} plays items 1, 2, 3 and 5.

    {2}i <number>{1} - view information on video <number>
    {2}c <number>{1} - view comments for video <number>
    {2}d <number>{1} - download video <number>
    {2}r <number>{1} - show videos related to video <number>
    {2}u <number>{1} - show videos uploaded by uploader of video <number>

    {2}q{1}, {2}quit{1} - exit mpsyt
""".format(c.ul, c.w, c.y, c.r)),

    ("search", "Searching and Retrieving", """
{0}Searching and Retrieving{1}

{2}set search_music false{1} - search all YouTube categories.
{2}set search_music true{1}  - search only YouTube music category.

{2}/<query>{1} or {2}.<query>{1} to search for videos. e.g., {2}/daft punk{1}
{2}//<query>{1} or {2}..<query>{1} - search for YouTube playlists. e.g., \
{2}//80's music{1}
{2}n{1} and {2}p{1} - continue search to next/previous pages.

{2}album <album title>{1} - Search for matching tracks using album title
{2}user <username>{1} - list YouTube uploads by <username>.
{2}user <username>/<query>{1} - as above, but matches <query>.
{2}userpl <username>{1} - list YouTube playlists created by <username>.
{2}pl <playlist url or id>{1} - Open YouTube playlist by url or id.
{2}url <url or id>{1} - Retrieve specific YouTube video by url or id.

{2}r <number>{1} - show videos related to video <number>.
{2}u <number>{1} - show videos uploaded by uploader of video <number>.
{2}c <number>{1} - view comments for video <number>
""".format(c.ul, c.w, c.y, c.r)),

    ("edit", "Editing / Manipulating Results", """
{0}Editing and Manipulating Results{1}

{2}rm <number(s)>{1} - remove items from displayed results.
{2}sw <number>,<number>{1} - swap two items.
{2}mv <number>,<number>{1} - move item <number> to position <number>.
{2}save <name>{1} - save displayed items as a local playlist.

{2}shuffle{1} - Shuffle the displayed results.
""".format(c.ul, c.w, c.y, c.r)),

    ("download", "Downloading and Playback", """
{0}Downloading and Playback{1}

{2}set show_video true{1} - play video instead of audio.

{2}<number(s)>{1} - play specified items, separated by commas.
              e.g., {2}1-3,5{1} plays items 1, 2, 3 and 5

{2}d <number>{1} - view downloads available for an item.
{2}da <number(s)>{1} - download best available audio file(s).
{2}dv <number(s)>{1} - download best available video file(s).
{2}dlurl <url or id>{1} download a YouTube video by url or video id.
{2}playurl <url or id>{1} play a YouTube video by url or id.

{2}all{1} or {2}*{1} - play all displayed items.
{2}repeat <number(s)>{1} - play and repeat the specified items.
{2}shuffle <number(s)>{1} - play specified items in random order.
""".format(c.ul, c.w, c.y, c.r)),

    ("playlists", "Using Local Playlists", """
{0}Using Local Playlists{1}

{2}add <number(s)>{1} - add items to the current playlist.
{2}add <number(s)> <playlist>{1} - add items to the specified playlist.
     (<playlist> will be created if it doesn't already exist)

{2}vp{1} - view current playlist.
{2}ls{1} - list saved playlists.
{2}mv <old name or ID> <new name>{1} - rename a playlist.
{2}rmp <playlist_name or ID>{1} - delete a playlist from disk.

{2}open <name or ID>{1} - open a saved playlist as the current playlist.
{2}play <name or ID>{1} - play a saved playlist directly.
{2}view <name or ID>{1} - view a playlist (current playlist left intact).
{2}save{1} or {2}save <name>{1} - save the displayed items as a playlist.

{2}rm <number(s)>{1} - remove items from displayed results.
{2}sw <number>,<number>{1} - swap two items.
{2}mv <number>,<number>{1} - move item <number> to position <number>.
""".format(c.ul, c.w, c.y, c.r)),

    ("invoke", "Invocation Parameters", """
{0}Invocation{1}

All mpsyt commands can be entered from the command line.  For example;

  {2}mpsyt dlurl <url or id>{1} to download a YouTube video by url or id
  {2}mpsyt playurl <url or id>{1} to play a YouTube video by url or id
  {2}mpsyt /mozart{1} to search
  {2}mpsyt //best songs of 2010{1} for a playlist search
  {2}mpsyt play <playlist name or ID>{1} to play a saved playlist
  {2}mpsyt ls{1} to list saved playlists

For further automation, a series of commands can be entered separated by
commas (,).  E.g.,

  {2}mpsyt open 1, 2-4{1} - play items 2-4 of first saved playlist
  {2}mpsyt //the doors, 1, all -a{1} - open YouTube playlist and play audio

If you need to enter an actual comma on the command line, use {2},,{1} instead.
""".format(c.ul, c.w, c.y, c.r)),

    ("config", "Configuration Options", """
{0}Configuration{1}

{2}set{1} - view current configuration
{2}set <item> default{1} - set an item to its default value
{2}set all default{1} - restore default settings
{2}set checkupdate true|false{1} - check for updates on exit
{2}set colours true|false{1} - use colours in display output
{2}set columns <columns>{1} - select extra displayed fields in search results:
     (valid: views comments rating date user likes dislikes category)
{2}set ddir <download direcory>{1} - set where downloads are saved
{2}set fullscreen true|false{1} - output video content in full-screen mode
{2}set max_res <number>{1} - play / download maximum video resolution height
{2}set max_results <number>{1} - show <number> results when searching (max 50)
{2}set order <relevance|date|views|rating>{1} search result ordering
{2}set player <player app>{1} - use <player app> for playback
{2}set playerargs <args>{1} - use specified arguments with player
{2}set search_music true|false{1} - search only music (all categories if false)
{2}set show_mplayer_keys true|false{1} - show keyboard help for mplayer and mpv
{2}set show_status true|false{1} - show status messages and progress
{2}set show_video true|false{1} - show video output (audio only if false)
{2}set window_pos <top|bottom>-<left|right>{1} - set player window position
{2}set window_size <number>x<number>{1} - set player window width & height
""".format(c.ul, c.w, c.y, c.r)),

    ("tips", "Advanced Tips", """
{0}Advanced Tips{1}

Use {2}-w{1}, {2}-f{1} or {2}-a{1} with your choice to override the configured\
 setting and
play items in windowed, fullscreen or audio modes.  E.g., 1-4 -a

When specifying columns with {2}set columns{1} command, append :N to set\
 width.
    E.g.: {2}set columns date views user:17 likes{1}

When using {2}open{1}, {2}view{1} or {2}play{1} to access a local playlist, \
you can enter
the first few characters instead of the whole name.

Use {2}5-{1} to select items 5 upward and {2}-5{1} to select up to item 5. \
This can be
included with other choices. e.g., 5,3,7-,-2
You can use spaces instead of commas: 5 3 7- -2
Reversed ranges also work. eg., 5-2

{2}dump{1} - to show entire contents of an opened YouTube playlist.
       (useful for playing or saving entire playlists, use {2}undump{1} to \
undo)

{2}set player mpv{1} or {2}set player mplayer{1} - change player application

Use {2}1{1} and {2}0{1} in place of true and false when using the {2}set{1} \
command
""".format(c.ul, c.w, c.y, c.r)),

    ("new", "New Features", """
{0}New Features in v0.01.46{1}

 - Added {2}c <number>{1} to view comments for a video
    (first 50 comments, no reply-comments)

 - Added feature to match album tracks using MusicBrainz
    To search albums, enter {2}album{1} optionally followed by album title

 - Custom formatted search result list using {2}set columns{1} command
   Optionally shows: rating, likes, dislikes, views, user, date, category
   and comments (number of) in search results

 - Added {2}set order <relevance|views|rating|date>{1} command for
     specifying search result ordering

 - Added {2}set console-width{1} for setting output width (default 80)

 - Added uploaded date in video info display (request #64)

 - Added likes / dislikes in video info display
""".format(c.ul, c.w, c.y, c.r))
]


def matchfunction(funcname, regex, userinput):
    """ Match userinput against regex.

    Call funcname, return True if matches.

    """

    if regex.match(userinput):
        matches = regex.match(userinput).groups()
        dbg("input: %s", userinput)
        dbg("function call: %s", funcname)
        dbg("regx matches: %s", matches)

        if g.debug_mode:
            globals()[funcname](*matches)

        else:

            try:
                globals()[funcname](*matches)

            except IndexError:
                g.message = F('invalid range')
                g.content = g.content or generate_songlist_display()

            except (ValueError, IOError) as e:
                g.message = F('cant get track') % uni(e)
                g.content = g.content or\
                    generate_songlist_display(zeromsg=g.message)

        return True


def main():
    """ Main control loop. """

    if not g.command_line:
        g.content = generate_songlist_display()
        g.content = logo(col=c.g, version=__version__) + "\n"
        g.message = "Enter /search-term to search or [h]elp"
        screen_update()

    # open playlists from file
    convert_playlist_to_v2()
    open_from_file()

    # get cmd line input
    arg_inp = " ".join(sys.argv[1:])

    # input types
    #yt = r'[^-_a-zA-Z0-9]?([-_a-zA-Z0-9]{11})[^-_a-zA-Z0-9]?
    word = r'[^\W\d][-\w\s]{,100}'
    rs = r'(?:repeat\s*|shuffle\s*|-a\s*|-f\s*|-w\s*)'
    regx = {
        'ls': r'ls$',
        'vp': r'vp$',
        'top': r'top(|3m|6m|year|all)\s*$',
        'dump': r'(un)?dump',
        'play': r'(%s{0,3})([-,\d\s]{1,250})\s*(%s{0,3})$' % (rs, rs),
        'info': r'i\s*(\d{1,4})$',
        'quits': r'(?:q|quit|exit)$',
        'plist': r'pl\s+(?:.*=|)([-_a-zA-Z0-9]{18,50})(?:(?:\&\#).*|$)',
        'yt_url': r'url\s(.*[-_a-zA-Z0-9]{11}.*$)',
        'search': r'(?:search|\.|/)\s*([^./].{1,500})',
        'dl_url': r'dlurl\s(.*[-_a-zA-Z0-9]{11}.*$)',
        'play_pl': r'play\s+(%s|\d+)$' % word,
        'related': r'r\s?(\d{1,4})$',
        'download': r'(dv|da|d|dl|download)\s*(\d{1,4})$',
        'play_url': r'playurl\s(.*[-_a-zA-Z0-9]{11}[^\s]*)(\s-(?:f|a|w))?$',
        'comments': r'c\s?(\d{1,4})$',
        'nextprev': r'(n|p)$',
        'play_all': r'(%s{0,3})(?:\*|all)\s*(%s{0,3})$' % (rs, rs),
        'user_pls': r'u(?:ser)?pl\s(.*)$',
        'save_last': r'save\s*$',
        'pl_search': r'(?:\.\.|\/\/|pls(?:earch)?\s)\s*(.*)$',
        'setconfig': r'set\s+([-\w]+)\s*"?([^"]*)"?\s*$',
        'down_many': r'(da|dv)\s+((?:\d+\s\d+|-\d|\d+-|\d,)(?:[\d\s,-]*))\s*$',
        'show_help': r'(?:help|h)(?:\s+(-?\w+)\s*)?$',
        'user_more': r'u\s?([\d]{1,4})$',
        'clearcache': r'clearcache$',
        'usersearch': r'user\s+([^\s].{2,})$',
        'shuffle_fn': r'\s*(shuffle)\s*$',
        'add_rm_all': r'(rm|add)\s(?:\*|all)$',
        'showconfig': r'(set|showconfig)\s*$',
        'search_album': r'album\s*(.{0,500})',
        'playlist_add': r'add\s*(-?\d[-,\d\s]{1,250})(%s)$' % word,
        'open_save_view': r'(open|save|view)\s*(%s)$' % word,
        'songlist_mv_sw': r'(mv|sw)\s*(\d{1,4})\s*[\s,]\s*(\d{1,4})$',
        'songlist_rm_add': r'(rm|add)\s*(-?\d[-,\d\s]{,250})$',
        'playlist_rename': r'mv\s*(%s\s+%s)$' % (word, word),
        'playlist_remove': r'rmp\s*(\d+|%s)$' % word,
        'open_view_bynum': r'(open|view)\s*(\d{1,4})$',
        'playlist_rename_idx': r'mv\s*(\d{1,3})\s*(%s)\s*$' % word
        #'play_url': r'(.*[-_a-zA-Z0-9]{11}[^\s]*)(\s-(?:f|a|w))?$'
    }

    # compile regexp's
    regx = {name: re.compile(val, re.UNICODE) for name, val in regx.items()}
    prompt = "> "
    arg_inp = arg_inp.replace(r",,", "[mpsyt-comma]")
    arg_inp = arg_inp.split(",")

    while True:
        next_inp = ""

        if len(arg_inp):
            arg_inp, next_inp = arg_inp[1:], arg_inp[0].strip()
            next_inp = next_inp.replace("[mpsyt-comma]", ",")

        try:
            userinput = next_inp or xinput(prompt).strip()

        except (KeyboardInterrupt, EOFError):
            userinput = prompt_for_exit()

        for k, v in regx.items():
            if matchfunction(k, v, userinput):
                break

        else:
            g.content = g.content or generate_songlist_display()

            if g.command_line:
                g.content = ""

            if userinput and not g.command_line:
                g.message = c.b + "Bad syntax. Enter h for help" + c.w

            elif userinput and g.command_line:
                sys.exit("Bad syntax")

        screen_update()

if "--debug" in sys.argv or os.environ.get("mpsytdebug") == "1":
    print(get_version_info())
    list_update("--debug", sys.argv, remove=True)
    g.debug_mode = True
    g.blank_text = "--\n"
    logfile = os.path.join(tempfile.gettempdir(), "mpsyt.log")
    logging.basicConfig(level=logging.DEBUG, filename=logfile)
    logging.getLogger("pafy").setLevel(logging.DEBUG)

elif "--logging" in sys.argv or os.environ.get("mpsytlog") == "1":
    list_update("--logging", sys.argv, remove=True)
    logfile = os.path.join(tempfile.gettempdir(), "mpsyt.log")
    logging.basicConfig(level=logging.DEBUG, filename=logfile)
    logging.getLogger("pafy").setLevel(logging.DEBUG)

dbg = logging.debug

if __name__ == "__main__":
    init()
    main()
