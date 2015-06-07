"""
mps-youtube.

https://github.com/np1/mps-youtube

Copyright (C) 2014, 2015 np1 and contributors

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

# python2 compatibility (for landscape)
from __future__ import print_function

__version__ = "0.2.5"
__notes__ = "released 1 June 2015"
__author__ = "np1"
__license__ = "GPLv3"
__url__ = "http://github.com/np1/mps-youtube"

from xml.etree import ElementTree as ET
import multiprocessing
import unicodedata
import collections
import subprocess
import threading
import platform
import tempfile
import difflib
import logging
import base64
import random
import locale
import socket
import shlex
import time
import math
import json
import sys
import re
import os
import pickle
from urllib.request import urlopen, build_opener
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

import pafy

from . import terminalsize

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

try:
    # pylint: disable=F0401
    import xerox
    has_xerox = True

except ImportError:
    has_xerox = False


mswin = os.name == "nt"
not_utf8_environment = mswin or "UTF-8" not in os.environ.get("LANG", "")


def member_var(x):
    """ Return True if x is a member variable. """
    return not(x.startswith("__") or callable(x))


locale.setlocale(locale.LC_ALL, "")  # for date formatting
XYTuple = collections.namedtuple('XYTuple', 'width height max_results')

ISO8601_TIMEDUR_EX = re.compile(r'PT((\d{1,3})H)?((\d{1,3})M)?((\d{1,2})S)?')


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

    ddir = ddir
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

    if not os.path.exists(mps_confdir):
        os.makedirs(mps_confdir)

    return mps_confdir


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


def get_content_length(url, preloading=False):
    """ Return content length of a url. """
    prefix = "preload: " if preloading else ""
    dbg(c.y + prefix + "getting content-length header" + c.w)
    response = urlopen(url)
    headers = response.headers
    cl = headers['content-length']
    return int(cl)


class Video(object):

    """ Class to represent a YouTube video. """

    def __init__(self, ytid, title, length):
        """ class members. """
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
    def nullfunc(x):
        """ Function that returns None. """
        return None

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


def get_streams(vid, force=False, callback=None, threeD=False):
    """ Get all streams as a dict.  callback function passed to get_pafy. """
    now = time.time()
    ytid = vid.ytid
    have_stream = g.streams.get(ytid) and g.streams[ytid]['expiry'] > now
    prfx = "preload: " if not callback else ""

    if not force and have_stream:
        ss = str(int(g.streams[ytid]['expiry'] - now) // 60)
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
    slist = slist['meta'] if isinstance(slist, dict) else slist
    au_streams = [x for x in slist if x['mtype'] == "audio"]

    def okres(x):
        """ Return True if resolution is within user specified maxres. """
        return int(x['quality'].split("x")[1]) <= maxres

    def getq(x):
        """ Return height aspect of resolution, eg 640x480 => 480. """
        return int(x['quality'].split("x")[1])

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
            retval = str(retval) + "p"

        if self.name == "encoder":
            retval = str(retval) + " [%s]" % (str(g.encoders[retval]['name']))

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

        # handle known player not set

        if self.allowed_values and value not in self.allowed_values:
            fail_msg = "%s must be one of * - not %s"
            allowed_values = self.allowed_values.copy()
            if '' in allowed_values:
                allowed_values[allowed_values.index('')] = "<nothing>"
            fail_msg = fail_msg.replace("*", ", ".join(allowed_values))

        if self.require_known_player and not known_player_set():
            fail_msg = "%s requires mpv or mplayer, can't set to %s"

        # handle true / false values

        elif self.type == bool:

            if value.upper() in "0 OFF NO DISABLED FALSE".split():
                value = False
                success_msg = "%s set to False" % c.c("g", self.name)

            elif value.upper() in "1 ON YES ENABLED TRUE".split():
                value = True
                success_msg = "%s set to True" % c.c("g", self.name)

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
                    success_msg = "%s set to %s" % (c.c("g", self.name),
                                                    dispval)

        # handle space separated list

        elif self.type == list:
            success_msg = "%s set to %s" % (c.c("g", self.name), value)
            value = value.split()

        # handle string values

        elif self.type == str:
            dispval = value or "None"
            success_msg = "%s set to %s" % (c.c("g", self.name),
                                            c.c("g", dispval))

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


def check_api_key(key):
    """ Validate an API key by calling an API endpoint with no quota cost """
    url = "https://www.googleapis.com/youtube/v3/i18nLanguages"
    query = {"part": "snippet", "fields": "items/id", "key": key}
    try:
        urlopen(url + "?" + urlencode(query)).read()
        message = "The key, '" + key + "' will now be used for API requests."

        # Make pafy use the same api key
        pafy.set_api_key(Config.API_KEY.get)

        return dict(valid=True, message=message)
    except HTTPError:
        message = "Invalid key or quota exceeded, '" + key + "'"
        return dict(valid=False, message=message)


def check_ddir(d):
    """ Check whether dir is a valid directory. """
    expanded = os.path.expanduser(d)
    if os.path.isdir(expanded):
        message = "Downloads will be saved to " + c.y + d + c.w
        return dict(valid=True, message=message, value=expanded)

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


def check_encoder(option):
    """ Check encoder value is acceptable. """
    encs = g.encoders

    if option >= len(encs):
        message = "%s%s%s is too high, type %sencoders%s to see valid values"
        message = message % (c.y, option, c.w, c.g, c.w)
        return dict(valid=False, message=message)

    else:
        message = "Encoder set to %s%s%s"
        message = message % (c.y, encs[option]['name'], c.w)
        return dict(valid=True, message=message)


def check_player(player):
    """ Check player exefile exists and get mpv version. """
    if has_exefile(player):

        if "mpv" in player:
            g.mpv_version = get_mpv_version(player)
            version = "%s.%s.%s" % g.mpv_version
            fmt = c.g, c.w, c.g, c.w, version
            msg = "%splayer%s set to %smpv%s (version %s)" % fmt
            return dict(valid=True, message=msg, value=player)

        else:
            msg = "%splayer%s set to %s%s%s" % (c.g, c.w, c.g, player, c.w)
            return dict(valid=True, message=msg, value=player)

    else:
        if mswin and not player.endswith(".exe"):
            return check_player(player + ".exe")

        else:
            msg = "Player application %s%s%s not found" % (c.r, player, c.w)
            return dict(valid=False, message=msg)


class Config(object):

    """ Holds various configuration values. """

    ORDER = ConfigItem("order", "relevance")
    ORDER.allowed_values = "relevance date views rating".split()
    USER_ORDER = ConfigItem("user_order", "")
    USER_ORDER.allowed_values = [""] + ORDER.allowed_values
    MAX_RESULTS = ConfigItem("max_results", 19, maxval=50, minval=1)
    CONSOLE_WIDTH = ConfigItem("console_width", 80, minval=70, maxval=880,
                               check_fn=check_console_width)
    MAX_RES = ConfigItem("max_res", 2160, minval=192, maxval=2160)
    PLAYER = ConfigItem("player", "mplayer" + (".exe" if mswin else ""),
                        check_fn=check_player)
    PLAYERARGS = ConfigItem("playerargs", "")
    ENCODER = ConfigItem("encoder", 0, minval=0, check_fn=check_encoder)
    NOTIFIER = ConfigItem("notifier", "")
    CHECKUPDATE = ConfigItem("checkupdate", True)
    SHOW_MPLAYER_KEYS = ConfigItem("show_mplayer_keys", True)
    SHOW_MPLAYER_KEYS.require_known_player = True
    FULLSCREEN = ConfigItem("fullscreen", False)
    FULLSCREEN.require_known_player = True
    SHOW_STATUS = ConfigItem("show_status", True)
    COLUMNS = ConfigItem("columns", "")
    DDIR = ConfigItem("ddir", get_default_ddir(), check_fn=check_ddir)
    OVERWRITE = ConfigItem("overwrite", True)
    SHOW_VIDEO = ConfigItem("show_video", False)
    SEARCH_MUSIC = ConfigItem("search_music", True)
    WINDOW_POS = ConfigItem("window_pos", "", check_fn=check_win_pos)
    WINDOW_POS.require_known_player = True
    WINDOW_SIZE = ConfigItem("window_size", "", check_fn=check_win_size)
    WINDOW_SIZE.require_known_player = True
    COLOURS = ConfigItem("colours",
                         False if mswin and not has_colorama else True,
                         check_fn=check_colours)
    DOWNLOAD_COMMAND = ConfigItem("download_command", '')
    API_KEY = ConfigItem("api_key", "AIzaSyCIM4EzNqi1in22f4Z3Ru3iYvLaY8tc3bo", check_fn=check_api_key)


class Playlist(object):

    """ Representation of a playist, has list of songs. """

    def __init__(self, name=None, songs=None):
        """ class members. """
        self.name = name
        self.creation = time.time()
        self.songs = songs or []

    @property
    def is_empty(self):
        """ Return True / False if songs are populated or not. """
        return not self.songs

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

    transcoder_path = "auto"
    delete_orig = True
    encoders = []
    muxapp = False
    meta = {}
    detectable_size = True
    command_line = False
    debug_mode = False
    preload_disabled = False
    ytpls = []
    mpv_version = 0, 0, 0
    mpv_usesock = False
    mprisctl = None
    browse_mode = "normal"
    preloading = []
    # expiry = 5 * 60 * 60  # 5 hours
    blank_text = "\n" * 200
    helptext = []
    max_retries = 3
    max_cached_streams = 1500
    url_memo = collections.OrderedDict()
    username_query_cache = collections.OrderedDict()
    model = Playlist(name="model")
    last_search_query = {}
    current_page = 0
    result_count = 0
    more_pages = None
    rprompt = None
    active = Playlist(name="active")
    text = {}
    userpl = {}
    ytpl = {}
    pafs = collections.OrderedDict()
    streams = collections.OrderedDict()
    pafy_pls = {}  #
    last_opened = message = content = ""
    config = [x for x in sorted(dir(Config)) if member_var(x)]
    defaults = {setting: getattr(Config, setting) for setting in config}
    suffix = "3" # Python 3
    CFFILE = os.path.join(get_config_dir(), "config")
    TCFILE = os.path.join(get_config_dir(), "transcode")
    OLD_PLFILE = os.path.join(get_config_dir(), "playlist" + suffix)
    PLFILE = os.path.join(get_config_dir(), "playlist_v2")
    CACHEFILE = os.path.join(get_config_dir(), "cache_py_" + sys.version[0:5])
    READLINE_FILE = None
    playerargs_defaults = {
        "mpv": {
            "msglevel": {"<0.4": "--msglevel=all=no:statusline=status",
                         ">=0.4": "--msg-level=all=no:statusline=status"},
            "title": "--title",
            "fs": "--fs",
            "novid": "--no-video",
            "ignidx": "--demuxer-lavf-o=fflags=+ignidx",
            "geo": "--geometry"},
        "mplayer": {
            "title": "-title",
            "fs": "-fs",
            "novid": "-novideo",
            # "ignidx": "-lavfdopts o=fflags=+ignidx".split()
            "ignidx": "",
            "geo": "-geometry"}
        }

def get_version_info():
    """ Return version and platform info. """
    out = "\nmpsyt version  : %s " % __version__
    out += "\n   notes       : %s" % __notes__
    out += "\npafy version   : %s" % pafy.__version__
    out += "\nPython version : %s" % sys.version
    out += "\nProcessor      : %s" % platform.processor()
    out += "\nMachine type   : %s" % platform.machine()
    out += "\nArchitecture   : %s, %s" % platform.architecture()
    out += "\nPlatform       : %s" % platform.platform()
    out += "\nsys.stdout.enc : %s" % sys.stdout.encoding
    out += "\ndefault enc    : %s" % sys.getdefaultencoding()
    out += "\nConfig dir     : %s" % get_config_dir()
    envs = "TERM SHELL LANG LANGUAGE".split()

    for env in envs:
        value = os.environ.get(env)
        out += "\nenv:%-11s: %s" % (env, value) if value else ""

    return out


def process_cl_args(args):
    """ Process command line arguments. """
    if "--version" in args:
        xprint(get_version_info())
        xprint("")
        sys.exit()

    if "--help" in args:

        for x in g.helptext:
            xprint(x[2])

        sys.exit()

    g.command_line = "playurl" in args or "dlurl" in args
    g.blank_text = "" if g.command_line else g.blank_text

    if "--no-preload" in sys.argv:
        g.preload_disabled = True
        list_update("--no-preload", sys.argv, remove=True)


def init():
    """ Initial setup. """
    # I believe these two lines once resolved a pickle error.
    # perhaps no longer needed, commenting out.
    # __main__.Playlist = Playlist
    # __main__.Video = Video

    init_text()
    init_readline()
    init_cache()
    init_transcode()

    # set player to mpv or mplayer if found, otherwise unset
    suffix = ".exe" if mswin else ""
    mplayer, mpv = "mplayer" + suffix, "mpv" + suffix

    if not os.path.exists(g.CFFILE):

        if has_exefile(mpv):
            Config.PLAYER.set(mpv)

        elif has_exefile(mplayer):
            Config.PLAYER.set(mplayer)

        saveconfig()

    else:
        import_config()

    # ensure encoder is not set beyond range of available presets
    if Config.ENCODER.get >= len(g.encoders):
        Config.ENCODER.set("0")

    # check mpv version

    if "mpv" in Config.PLAYER.get and not mswin:
        if has_exefile(Config.PLAYER.get):
            g.mpv_version = get_mpv_version(Config.PLAYER.get)
            options = subprocess.check_output(
                [Config.PLAYER.get, "--list-options"]).decode()
            # g.mpv_usesock = "--input-unix-socket" in options and not mswin

            if "--input-unix-socket" in options:
                g.mpv_usesock = True
                dbg(c.g + "mpv supports --input-unix-socket" + c.w)

    # setup colorama
    if has_colorama and mswin:
        init_colorama()

    # find muxer app
    if mswin:
        g.muxapp = has_exefile("ffmpeg.exe") or has_exefile("avconv.exe")

    else:
        g.muxapp = has_exefile("ffmpeg") or has_exefile("avconv")

    # initialize remote interface
    try:
        from . import mpris
        g.mprisctl, conn = multiprocessing.Pipe()
        t = multiprocessing.Process(target=mpris.main, args=(conn,))
        t.daemon = True
        t.start()
    except ImportError:
        pass

    # Make pafy use the same api key
    pafy.set_api_key(Config.API_KEY.get)

    process_cl_args(sys.argv)


def init_transcode():
    """ Create transcoding presets if not present.

    Read transcoding presets.
    """
    if not os.path.exists(g.TCFILE):
        config_file_contents = """\
# transcoding presets for mps-youtube
# VERSION 0

# change ENCODER_PATH to the path of ffmpeg / avconv or leave it as auto
# to let mps-youtube attempt to find ffmpeg or avconv
ENCODER_PATH: auto

# Delete original file after encoding it
# Set to False to keep the original downloaded file
DELETE_ORIGINAL: True

# ENCODING PRESETS

# Encode ogg or m4a to mp3 256k
name: MP3 256k
extension: mp3
valid for: ogg,m4a
command: ENCODER_PATH -i IN -codec:a libmp3lame -b:a 256k OUT.EXT

# Encode ogg or m4a to mp3 192k
name: MP3 192k
extension: mp3
valid for: ogg,m4a
command: ENCODER_PATH -i IN -codec:a libmp3lame -b:a 192k OUT.EXT

# Encode ogg or m4a to mp3 highest quality vbr
name: MP3 VBR best
extension: mp3
valid for: ogg,m4a
command: ENCODER_PATH -i IN -codec:a libmp3lame -q:a 0 OUT.EXT

# Encode ogg or m4a to mp3 high quality vbr
name: MP3 VBR good
extension: mp3
valid for: ogg,m4a
command: ENCODER_PATH -i IN -codec:a libmp3lame -q:a 2 OUT.EXT

# Encode m4a to ogg
name: OGG 256k
extension: ogg
valid for: m4a
command: ENCODER_PATH -i IN -codec:a libvorbis -b:a 256k OUT.EXT

# Encode ogg to m4a
name: M4A 256k
extension: m4a
valid for: ogg
command: ENCODER_PATH -i IN -strict experimental -codec:a aac -b:a 256k OUT.EXT

# Encode ogg or m4a to wma v2
name: Windows Media Audio v2
extension: wma
valid for: ogg,m4a
command: ENCODER_PATH -i IN -codec:a wmav2 -q:a 0 OUT.EXT"""

        with open(g.TCFILE, "w") as tcf:
            tcf.write(config_file_contents)
            dbg("generated transcoding config file")

    else:
        dbg("transcoding config file exists")

    with open(g.TCFILE, "r") as tcf:
        g.encoders = [dict(name="None", ext="COPY", valid="*")]
        e = {}

        for line in tcf.readlines():

            if line.startswith("TRANSCODER_PATH:"):
                m = re.match("TRANSCODER_PATH:(.*)", line).group(1)
                g.transcoder_path = m.strip()

            elif line.startswith("DELETE_ORIGINAL:"):
                m = re.match("DELETE_ORIGINAL:(.*)", line).group(1)
                do = m.strip().lower() in ("true", "yes", "enabled", "on")
                g.delete_orig = do

            elif line.startswith("name:"):
                e['name'] = re.match("name:(.*)", line).group(1).strip()

            elif line.startswith("extension:"):
                e['ext'] = re.match("extension:(.*)", line).group(1).strip()

            elif line.startswith("valid for:"):
                e['valid'] = re.match("valid for:(.*)", line).group(1).strip()

            elif line.startswith("command:"):
                e['command'] = re.match("command:(.*)", line).group(1).strip()

                if "name" in e and "ext" in e and "valid" in e:
                    g.encoders.append(e)
                    e = {}


def init_cache():
    """ Import cache file. """
    if os.path.isfile(g.CACHEFILE):

        try:

            with open(g.CACHEFILE, "rb") as cf:
                cached = pickle.load(cf)

            if 'streams' in cached:
                g.streams = cached['streams']
                g.username_query_cache = cached['userdata']
            else:
                g.streams = cached

            if 'pafy' in cached:
                pafy.load_cache(cached['pafy'])

            dbg(c.g + "%s cached streams imported%s", str(len(g.streams)), c.w)

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


def known_player_set():
    """ Return true if the set player is known. """
    for allowed_player in g.playerargs_defaults:
        regex = r'(?:\b%s($|\.[a-zA-Z0-9]+$))' % re.escape(allowed_player)
        match = re.search(regex, Config.PLAYER.get)

        if mswin:
            match = re.search(regex, Config.PLAYER.get, re.IGNORECASE)

        if match:
            return allowed_player

    return None


def showconfig(_):
    """ Dump config data. """
    width = getxy().width
    width -= 30
    s = "  %s%-17s%s : %s\n"
    out = "  %s%-17s   %s%s%s\n" % (c.ul, "Key", "Value", " " * width, c.w)

    for setting in g.config:
        val = getattr(Config, setting)

        # don't show player specific settings if unknown player
        if not known_player_set() and val.require_known_player:
            continue

        # don't show max_results if auto determined
        if g.detectable_size and setting == "MAX_RESULTS":
            continue

        if g.detectable_size and setting == "CONSOLE_WIDTH":
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
    caches = dict(
        streams=g.streams,
        userdata=g.username_query_cache,
        pafy=pafy.dump_cache())

    with open(g.CACHEFILE, "wb") as cf:
        pickle.dump(caches, cf, protocol=2)

    dbg(c.p + "saved cache file: " + g.CACHEFILE + c.w)


def import_config():
    """ Override config if config file exists. """
    if os.path.exists(g.CFFILE):

        with open(g.CFFILE, "rb") as cf:
            saved_config = pickle.load(cf)

        for k, v in saved_config.items():

            try:
                getattr(Config, k).value = v

            except AttributeError:  # Ignore unrecognised data in config
                dbg("Unrecognised config item: %s", k)

        # Update config files from versions <= 0.01.41
        if isinstance(Config.PLAYERARGS.get, list):
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

    @classmethod
    def c(cls, colour, text):
        """ Return coloured text. """
        return getattr(cls, colour) + text + cls.w


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
                    "(c) 2014, 2015 np1 and contributors**2\n"""),
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
        'no mix': 'No mix is available for the selected video',
        'mix only videos': 'Mixes are only available for videos',
        'invalid item': '*Invalid item entered!*',

        # Info messages..

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

    except AttributeError:
        # playlist is from a time when this module was __main__
        # https://github.com/np1/mps-youtube/issues/214
        import __main__
        __main__.Playlist = Playlist
        __main__.Video = Video

        with open(g.PLFILE, "rb") as plf:
            g.userpl = pickle.load(plf)

        save_to_file()
        xprint("Updated playlist file. Please restart mpsyt")
        sys.exit()

    except EOFError:
        xprint("Error opening playlists from %s" % g.PLFILE)
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

    # rename old playlist file
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
    logo_txt = r"""                                             _         _
 _ __ ___  _ __  ___       _   _  ___  _   _| |_ _   _| |__   ___
| '_ ` _ \| '_ \/ __|_____| | | |/ _ \| | | | __| | | | '_ \ / _ \
| | | | | | |_) \__ \_____| |_| | (_) | |_| | |_| |_| | |_) |  __/
|_| |_| |_| .__/|___/      \__, |\___/ \__,_|\__|\__,_|_.__/ \___|
          |_|              |___/"""
    version = " v" + version if version else ""
    logo_txt = col + logo_txt + c.w + version
    lines = logo_txt.split("\n")
    length = max(len(x) for x in lines)
    x, y, _ = getxy()
    indent = (x - length - 1) // 2
    newlines = (y - 12) // 2
    indent, newlines = (0 if x < 0 else x for x in (indent, newlines))
    lines = [" " * indent + l for l in lines]
    logo_txt = "\n".join(lines) + "\n" * newlines
    return logo_txt if not g.debug_mode else ""


def playlists_display():
    """ Produce a list of all playlists. """
    if not g.userpl:
        g.message = F("no playlists")
        return logo(c.y) + "\n\n" if g.model.is_empty else \
            generate_songlist_display()

    maxname = max(len(a) for a in g.userpl)
    out = "      {0}Local Playlists{1}\n".format(c.ul, c.w)
    start = "      "
    fmt = "%s%s%-3s %-" + str(maxname + 3) + "s%s %s%-7s%s %-5s%s"
    head = (start, c.b, "ID", "Name", c.b, c.b, "Count", c.b, "Duration", c.w)
    out += "\n" + fmt % head + "\n\n"

    for v, z in enumerate(sorted(g.userpl)):
        n, p = z, g.userpl[z]
        l = fmt % (start, c.g, v + 1, n, c.w, c.y, str(p.size), c.y,
                   p.duration, c.w) + "\n"
        out += l

    return out


def mplayer_help(short=True):
    """ Mplayer help.  """
    # pylint: disable=W1402

    volume = "[{0}9{1}] volume [{0}0{1}]"
    volume = volume if short else volume + "      [{0}q{1}] return"
    seek = "[{0}\u2190{1}] seek [{0}\u2192{1}]"
    pause = "[{0}\u2193{1}] SEEK [{0}\u2191{1}]       [{0}space{1}] pause"

    if not_utf8_environment:
        seek = "[{0}<-{1}] seek [{0}->{1}]"
        pause = "[{0}DN{1}] SEEK [{0}UP{1}]       [{0}space{1}] pause"

    single = "[{0}q{1}] return"
    next_prev = "[{0}>{1}] next/prev [{0}<{1}]"
    # ret = "[{0}q{1}] %s" % ("return" if short else "next track")
    ret = single if short else next_prev
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
        hms = str(int(M) + 60) + ":" + S

    elif H.startswith("0"):
        hms = ":".join([H[1], M, S])

    return hms


def get_track_id_from_json(item):
    """ Try to extract video Id from various response types """
    fields = ['contentDetails/videoId',
              'snippet/resourceId/videoId',
              'id/videoId',
              'id']
    for field in fields:
        node = item
        for p in field.split('/'):
            if node and type(node) is dict:
                node = node.get(p)
        if node:
            return node
    return ''


class GdataError(Exception):
    """Gdata query failed."""
    pass


def call_gdata(api, qs):
    """Make a request to the youtube gdata api."""
    qs = qs.copy()
    qs['key'] = Config.API_KEY.get
    url = "https://www.googleapis.com/youtube/v3/" + api + '?' + urlencode(qs)

    if url in g.url_memo:
        return json.loads(g.url_memo[url])

    try:
        data = urlopen(url).read().decode()

    except HTTPError as e:
        try:
            errdata = e.file.read().decode()
            error = json.loads(errdata)['error']['message']
            errmsg = 'Youtube Error %d: %s' % (e.getcode(), error)
        except:
            errmsg = str(e)
        raise GdataError(errmsg)

    # Add to url memo, ensure url memo doesn't get too big.
    dbg('Cache data for query url {}:'.format(url))
    g.url_memo[url] = data

    while len(g.url_memo) > 300:
        g.url_memo.popitem(last=False)

    return json.loads(data)


def get_page_info_from_json(jsons, result_count=None):
    """ Extract & save some information about result count and paging. """
    g.more_pages = jsons.get('nextPageToken')
    if result_count:
        if result_count < getxy().max_results:
            g.more_pages = False
    pageinfo = jsons.get('pageInfo')
    per_page = pageinfo.get('resultsPerPage')
    g.result_count = pageinfo.get('totalResults')
    if result_count: # limit number of results, e.g. if api makes it up
        if result_count < per_page:
            g.result_count = min(g.result_count, result_count)


def get_tracks_from_json(jsons):
    """ Get search results from API response """

    items = jsons.get("items")
    if not items:
        dbg("got unexpected data or no search results")
        return False

    # fetch detailed information about items from videos API
    qs = {'part':'contentDetails,statistics,snippet',
          'id': ','.join([get_track_id_from_json(i) for i in items])}
    try:
        wdata = call_gdata('videos', qs)

    except GdataError as e:
        g.message = F('no data') % e
        g.content = logo(c.r)
        return

    items_vidinfo = wdata.get('items', [])
    # enhance search results by adding information from videos API response
    for searchresult, vidinfoitem in zip(items, items_vidinfo):
        searchresult.update(vidinfoitem)

    # populate list of video objects
    songs = []
    catids = []
    for item in items:

        try:

            ytid = get_track_id_from_json(item)
            duration = item.get('contentDetails', {}).get('duration')

            if duration:
                duration = ISO8601_TIMEDUR_EX.findall(duration)
                if len(duration) > 0:
                    _, hours, _, minutes, _, seconds = duration[0]
                    duration = [seconds, minutes, hours]
                    duration = [int(v) if len(v) > 0 else 0 for v in duration]
                    duration = sum([60**p*v for p, v in enumerate(duration)])
                else:
                    duration = 30
            else:
                duration = 30

            stats = item.get('statistics', {})
            snippet = item.get('snippet', {})
            title = snippet.get('title', '').strip()
            # instantiate video representation in local model
            cursong = Video(ytid=ytid, title=title, length=duration)
            likes = int(stats.get('likeCount', 0))
            dislikes = int(stats.get('dislikeCount', 0))
            #XXX this is a very poor attempt to calculate a rating value
            rating = 5.*likes/(likes+dislikes) if (likes+dislikes) > 0 else 0
            category = snippet.get('categoryId')

            # cache video information in custom global variable store
            g.meta[ytid] = dict(
                # tries to get localized title first, fallback to normal title
                title=snippet.get('localized',
                                  {'title':snippet.get('title',
                                                       '[!!!]')}).get('title',
                                                                      '[!]'),
                length=str(fmt_time(cursong.length)),
                rating=str('{}'.format(rating))[:4].ljust(4, "0"),
                uploader=snippet.get('channelId'),
                uploaderName=snippet.get('channelTitle'),
                category=category,
                aspect="custom", #XXX
                uploaded=yt_datetime(snippet.get('publishedAt', ''))[1],
                likes=str(num_repr(likes)),
                dislikes=str(num_repr(dislikes)),
                commentCount=str(num_repr(int(stats.get('commentCount', 0)))),
                viewCount=str(num_repr(int(stats.get('viewCount', 0)))))

        except Exception as e:

            dbg(json.dumps(item, indent=2))
            dbg('Error during metadata extraction/instantiation of search ' +
                'result {}\n{}'.format(ytid, e))

        songs.append(cursong)

    get_page_info_from_json(jsons, len(songs))

    # return video objects
    return songs



def screen_update(fill_blank=True):
    """ Display content, show message, blank screen."""
    xprint(g.blank_text)

    if g.content:
        xprint(g.content)

    if g.message or g.rprompt:
        out = g.message or ''
        blanks = getxy().width - len(out) - len(g.rprompt or '')
        out += ' ' * blanks + (g.rprompt or '')
        xprint(out)

    elif fill_blank:
        xprint("")

    g.message = g.content = g.rprompt = False


def playback_progress(idx, allsongs, repeat=False):
    """ Generate string to show selected tracks, indicate current track. """
    # pylint: disable=R0914
    # too many local variables
    cw = getxy().width
    out = "  %s%-XXs%s%s\n".replace("XX", str(cw - 9))
    out = out % (c.ul, "Title", "Time", c.w)
    show_key_help = (known_player_set and Config.SHOW_MPLAYER_KEYS.get)
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
        return str(num)

    def digit_count(x):
        """ Return number of digits. """
        return int(math.floor(math.log10(x)) + 1)

    digits = digit_count(num)
    sig = 3 if digits % 3 == 0 else 2
    rounded = int(round(num, int(sig - digits)))
    digits = digit_count(rounded)
    suffix = "_kmBTqXYX"[(digits - 1) // 3]
    front = 3 if digits % 3 == 0 else digits % 3

    if not front == 1:
        return str(rounded)[0:front] + suffix

    return str(rounded)[0] + "." + str(rounded)[1] + suffix


def real_len(u, alt=False):
    """ Try to determine width of strings displayed with monospace font. """
    if not isinstance(u, str):
        u = u.decode("utf8")

    u = xenc(u) # Handle replacements of unsuported characters

    ueaw = unicodedata.east_asian_width

    if alt:
        # widths = dict(W=2, F=2, A=1, N=0.75, H=0.5)  # original
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

    t = ' '.join(t.split('\n'))

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
    time_obj = time.strptime(yt_date_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    locale_date = time.strftime("%x", time_obj)
    # strip first two digits of four digit year
    short_date = re.sub(r"(\d\d\D\d\d\D)20(\d\d)$", r"\1\2", locale_date)
    return time_obj, short_date


def generate_playlist_display():
    """ Generate list of playlists. """
    if not g.ytpls:
        g.message = c.r + "No playlists found!"
        return logo(c.g) + "\n\n"
    g.rprompt = page_msg(g.current_page)

    cw = getxy().width
    fmtrow = "%s%-5s %s %-12s %-8s  %-2s%s\n"
    fmthd = "%s%-5s %-{}s %-12s %-9s %-5s%s\n".format(cw - 36)
    head = (c.ul, "Item", "Playlist", "Author", "Updated", "Count", c.w)
    out = "\n" + fmthd % head

    for n, x in enumerate(g.ytpls):
        col = (c.g if n % 2 == 0 else c.w)
        length = x.get('size') or "?"
        length = "%4s" % length
        title = x.get('title') or "unknown"
        author = x.get('author') or "unknown"
        updated = yt_datetime(x.get('updated'))[1]
        title = uea_pad(cw - 36, title)
        out += (fmtrow % (col, str(n + 1), title, author[:12], updated, str(length), c.w))

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
                "user": dict(name="uploaderName", size=10, heading="User"),
                "likes": dict(name="likes", size=4, heading="Like"),
                "dislikes": dict(name="dislikes", size=4, heading="Dslk"),
                "category": dict(name="category", size=8, heading="Category")}

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
            cw = getxy().width
            if total_size < cw - 18:
                ret.append(dict(name=nm, size=sz, heading=hd))

    return ret


def page_msg(page=0):
    """ Format information about currently displayed page to a string. """
    max_results = getxy().max_results
    page_count = max(int(math.ceil(min(g.result_count, 500)/max_results)), 1)
    if page_count > 1:
        pagemsg = "{}{}/{}{}"
        #start_index = max_results * g.current_page
        return pagemsg.format('<' if page > 0 else '[',
                              "%s%s%s" % (c.y, page+1, c.w),
                              page_count,
                              ']>'[int(g.more_pages != None or
                                       (page < page_count))])
    return None


def generate_songlist_display(song=False, zeromsg=None, frmat="search"):
    """ Generate list of choices from a song list."""
    # pylint: disable=R0914
    if g.browse_mode == "ytpl":
        return generate_playlist_display()

    songs = g.model.songs or []

    if not songs:
        g.message = zeromsg or "Enter /search-term to search or [h]elp"
        return logo(c.g) + "\n\n"
    g.rprompt = page_msg(g.current_page)

    have_meta = all(x.ytid in g.meta for x in songs)
    user_columns = get_user_columns() if have_meta else []
    maxlength = max(x.length for x in songs)
    lengthsize = 8 if maxlength > 35999 else 7
    lengthsize = 5 if maxlength < 6000 else lengthsize
    reserved = 9 + lengthsize + len(user_columns)
    cw = getxy().width
    cw -= 1
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
        details['idx'] = "%2d" % (n + 1)
        details['title'] = uea_pad(columns[1]['size'], otitle)
        cat = details.get('category') or '-'
        details['category'] = pafy.get_categoryname(cat)
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
    """ Update status line. """
    if not mute and Config.SHOW_STATUS.get:
        writeline(text)


def writeline(text):
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


def list_update(item, lst, remove=False):
    """ Add or remove item from list, checking first to avoid exceptions. """
    if not remove and item not in lst:
        lst.append(item)

    elif remove and item in lst:
        lst.remove(item)


def generate_real_playerargs(song, override, failcount):
    """ Generate args for player command.

    Return args and songdata status.

    """
    # pylint: disable=R0914
    # pylint: disable=R0912
    video = Config.SHOW_VIDEO.get
    video = True if override in ("fullscreen", "window") else video
    video = False if override == "audio" else video
    m4a = "mplayer" not in Config.PLAYER.get
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
    songdata = (song.ytid, stream['ext'] + " " + stream['quality'],
                int(size / (1024 ** 2)))

    # pylint: disable=E1103
    # pylint thinks PLAYERARGS.get might be bool
    argsstr = Config.PLAYERARGS.get.strip()
    args = argsstr.split() if argsstr else []

    known_player = known_player_set()
    if known_player:
        pd = g.playerargs_defaults[known_player]
        args.append(pd["title"])
        args.append(song.title)
        novid_arg = pd["novid"]
        fs_arg = pd["fs"]
        list_update(fs_arg, args, remove=not Config.FULLSCREEN.get)

        geometry = ""

        if Config.WINDOW_SIZE.get and "-geometry" not in argsstr:
            geometry = Config.WINDOW_SIZE.get

        if Config.WINDOW_POS.get and "-geometry" not in argsstr:
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
            list_update("-noquiet", args)
            list_update("-prefer-ipv4", args)

        elif "mpv" in Config.PLAYER.get:
            msglevel = pd["msglevel"]["<0.4"]

            #  undetected (negative) version number assumed up-to-date
            if g.mpv_version[0:2] < (0, 0) or g.mpv_version[0:2] >= (0, 4):
                msglevel = pd["msglevel"][">=0.4"]

            if g.mpv_usesock:
                list_update("--really-quiet", args)
            else:
                list_update("--really-quiet", args, remove=True)
                list_update(msglevel, args)

    return [Config.PLAYER.get] + args + [stream['url']], songdata


def playsong(song, failcount=0, override=False):
    """ Play song using config.PLAYER called with args config.PLAYERARGS."""
    # pylint: disable=R0911,R0912
    if not Config.PLAYER.get or not has_exefile(Config.PLAYER.get):
        g.message = "Player not configured! Enter %sset player <player_app> "\
            "%s to set a player" % (c.g, c.w)
        return

    if Config.NOTIFIER.get:
        subprocess.call(shlex.split(Config.NOTIFIER.get) + [song.title])

    # don't interrupt preloading:
    while song.ytid in g.preloading:
        writestatus("fetching item..")
        time.sleep(0.1)

    try:
        get_streams(song, force=failcount, callback=writestatus)

    except (IOError, URLError, HTTPError, socket.timeout) as e:
        dbg("--ioerror in playsong call to get_streams %s", str(e))

        if "Youtube says" in str(e):
            g.message = F('cant get track') % (song.title + " " + str(e))
            return

        elif failcount < g.max_retries:
            dbg("--ioerror - trying next stream")
            failcount += 1
            return playsong(song, failcount=failcount, override=override)

        elif "pafy" in str(e):
            g.message = str(e) + " - " + song.ytid
            return

    except ValueError:
        g.message = F('track unresolved')
        dbg("----valueerror in playsong call to get_streams")
        return

    try:
        cmd, songdata = generate_real_playerargs(song, override, failcount)

    except (HTTPError) as e:

        # Fix for invalid streams (gh-65)
        dbg("----htterror in playsong call to gen_real_args %s", str(e))
        if failcount < g.max_retries:
            failcount += 1
            return playsong(song, failcount=failcount, override=override)

    except IOError as e:
        # this may be cause by attempting to play a https stream with
        # mplayer
        # ====
        errmsg = e.message if hasattr(e, "message") else str(e)
        g.message = c.r + str(errmsg) + c.w
        return

    songdata = "%s; %s; %s Mb" % songdata
    writestatus(songdata)
    dbg("%splaying %s (%s)%s", c.b, song.title, failcount, c.w)
    dbg("calling %s", " ".join(cmd))
    returncode = launch_player(song, songdata, cmd)
    failed = returncode not in (0, 42, 43)

    if failed and failcount < g.max_retries:
        dbg(c.r + "stream failed to open" + c.w)
        dbg("%strying again (attempt %s)%s", c.r, (2 + failcount), c.w)
        writestatus("error: retrying")
        time.sleep(1.2)
        failcount += 1
        return playsong(song, failcount=failcount, override=override)

    return returncode


def get_input_file():
    """ Check for existence of custom input file.

    Return file name of temp input file with mpsyt mappings included
    """
    confpath = conf = ''

    if "mpv" in Config.PLAYER.get:
        confpath = os.path.join(get_config_dir(), "mpv-input.conf")

    elif "mplayer" in Config.PLAYER.get:
        confpath = os.path.join(get_config_dir(), "mplayer-input.conf")

    if os.path.isfile(confpath):
        dbg("using %s for input key file", confpath)

        with open(confpath) as conffile:
            conf = conffile.read() + '\n'

    conf = conf.replace("quit", "quit 43")
    conf = conf.replace("playlist_prev", "quit 42")
    conf = conf.replace("pt_step -1", "quit 42")
    conf = conf.replace("playlist_next", "quit")
    conf = conf.replace("pt_step 1", "quit")
    standard_cmds = ['q quit 43\n', '> quit\n', '< quit 42\n', 'NEXT quit\n',
                     'PREV quit 42\n', 'ENTER quit\n']
    bound_keys = [i.split()[0] for i in conf.splitlines() if i.split()]

    for i in standard_cmds:
        key = i.split()[0]

        if key not in bound_keys:
            conf += i

    with tempfile.NamedTemporaryFile('w', prefix='mpsyt-input',
                                     delete=False) as tmpfile:
        tmpfile.write(conf)
        return tmpfile.name


def launch_player(song, songdata, cmd):
    """ Launch player application. """

    # Fix UnicodeEncodeError when title has characters
    # not supported by encoding
    cmd = [xenc(i) for i in cmd]

    arturl = "http://i.ytimg.com/vi/%s/default.jpg" % song.ytid
    input_file = get_input_file()
    sockpath = None
    fifopath = None

    try:
        if "mplayer" in Config.PLAYER.get:
            cmd.append('-input')

            if mswin:
                # Mplayer does not recognize path starting with drive letter,
                # or with backslashes as a delimiter.
                input_file = input_file[2:].replace('\\', '/')

            cmd.append('conf=' + input_file)

            if g.mprisctl:
                fifopath = tempfile.mktemp('.fifo', 'mpsyt-mplayer')
                os.mkfifo(fifopath)
                cmd.extend(['-input', 'file=' + fifopath])
                g.mprisctl.send(('mplayer-fifo', fifopath))
                g.mprisctl.send(('metadata', (song.ytid, song.title,
                                              song.length, arturl)))

            p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, bufsize=1)
            player_status(p, songdata + "; ", song.length)
            returncode = p.wait()

        elif "mpv" in Config.PLAYER.get:
            cmd.append('--input-conf=' + input_file)

            if g.mpv_usesock:
                sockpath = tempfile.mktemp('.sock', 'mpsyt-mpv')
                cmd.append('--input-unix-socket=' + sockpath)

                with open(os.devnull, "w") as devnull:
                    p = subprocess.Popen(cmd, shell=False, stderr=devnull)

                if g.mprisctl:
                    g.mprisctl.send(('socket', sockpath))
                    g.mprisctl.send(('metadata', (song.ytid, song.title,
                                                  song.length, arturl)))

            else:
                if g.mprisctl:
                    fifopath = tempfile.mktemp('.fifo', 'mpsyt-mpv')
                    os.mkfifo(fifopath)
                    cmd.append('--input-file=' + fifopath)
                    g.mprisctl.send(('mpv-fifo', fifopath))
                    g.mprisctl.send(('metadata', (song.ytid, song.title,
                                                  song.length, arturl)))

                p = subprocess.Popen(cmd, shell=False, stderr=subprocess.PIPE,
                                     bufsize=1)

            player_status(p, songdata + "; ", song.length, mpv=True,
                          sockpath=sockpath)
            returncode = p.wait()

        else:
            with open(os.devnull, "w") as devnull:
                returncode = subprocess.call(cmd, stderr=devnull)
            p = None

        return returncode

    except OSError:
        g.message = F('no player') % Config.PLAYER.get
        return None

    finally:
        os.unlink(input_file)

        # May not exist if mpv has not yet created the file
        if sockpath and os.path.exists(sockpath):
            os.unlink(sockpath)

        if fifopath:
            os.unlink(fifopath)

        if g.mprisctl:
            g.mprisctl.send(('stop', True))

        if p and p.poll() is None:
            p.terminate()  # make sure to kill mplayer if mpsyt crashes


def player_status(po_obj, prefix, songlength=0, mpv=False, sockpath=None):
    """ Capture time progress from player output. Write status line. """
    # pylint: disable=R0914, R0912
    re_mplayer = re.compile(r"A:\s*(?P<elapsed_s>\d+)\.\d\s*")
    re_mpv = re.compile(r".{,15}AV?:\s*(\d\d):(\d\d):(\d\d)")
    re_volume = re.compile(r"Volume:\s*(?P<volume>\d+)\s*%")
    re_player = re_mpv if mpv else re_mplayer
    last_displayed_line = None
    buff = ''
    volume_level = None
    last_pos = None

    if sockpath:
        s = socket.socket(socket.AF_UNIX)

        tries = 0
        while tries < 10 and po_obj.poll() is None:
            time.sleep(.5)
            try:
                s.connect(sockpath)
                break
            except socket.error:
                pass
            tries += 1
        else:
            return

        try:
            observe_full = False
            cmd = {"command": ["observe_property", 1, "time-pos"]}
            s.send(json.dumps(cmd).encode() + b'\n')
            volume_level = elapsed_s = None

            for line in s.makefile():
                resp = json.loads(line)

                # deals with bug in mpv 0.7 - 0.7.3
                if resp.get('event') == 'property-change' and not observe_full:
                    cmd = {"command": ["observe_property", 2, "volume"]}
                    s.send(json.dumps(cmd).encode() + b'\n')
                    observe_full = True

                if resp.get('event') == 'property-change' and resp['id'] == 1:
                    elapsed_s = int(resp['data'])

                elif resp.get('event') == 'property-change' and resp['id'] == 2:
                    volume_level = int(resp['data'])

                if elapsed_s:
                    line = make_status_line(elapsed_s, prefix, songlength,
                                            volume=volume_level)

                    if line != last_displayed_line:
                        writestatus(line)
                        last_displayed_line = line

        except socket.error:
            pass

    else:
        elapsed_s = 0

        while po_obj.poll() is None:
            stdstream = po_obj.stderr if mpv else po_obj.stdout
            char = stdstream.read(1).decode("utf-8", errors="ignore")

            if char in '\r\n':

                mv = re_volume.search(buff)

                if mv:
                    volume_level = int(mv.group("volume"))

                match_object = re_player.match(buff)

                if match_object:

                    try:
                        h, m, s = map(int, match_object.groups())
                        elapsed_s = h * 3600 + m * 60 + s

                    except ValueError:

                        try:
                            elapsed_s = int(match_object.group('elapsed_s') or
                                            '0')

                        except ValueError:
                            continue

                    line = make_status_line(elapsed_s, prefix, songlength,
                                            volume=volume_level)

                    if line != last_displayed_line:
                        writestatus(line)
                        last_displayed_line = line

                if buff.startswith('ANS_volume='):
                    volume_level = round(float(buff.split('=')[1]))

                paused = ("PAUSE" in buff) or ("Paused" in buff)
                if (elapsed_s != last_pos or paused) and g.mprisctl:
                    last_pos = elapsed_s
                    g.mprisctl.send(('pause', paused))
                    g.mprisctl.send(('volume', volume_level))
                    g.mprisctl.send(('time-pos', elapsed_s))

                buff = ''

            else:
                buff += char


def make_status_line(elapsed_s, prefix, songlength=0, volume=None):
    """ Format progress line output.  """
    # pylint: disable=R0914

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

    if volume:
        vol_suffix = " vol: %d%%" % volume

    else:
        vol_suffix = ""

    cw = getxy().width
    prog_bar_size = cw - len(prefix) - len(status_line) - len(vol_suffix) - 7
    progress = int(math.ceil(pct / 100 * prog_bar_size))
    status_line += " [%s]" % ("=" * (progress - 1) +
                              ">").ljust(prog_bar_size, ' ')
    return prefix + status_line + vol_suffix


def _search(progtext, qs=None, splash=True, pre_load=True):
    """ Perform memoized url fetch, display progtext. """
    g.message = "Searching for '%s%s%s'" % (c.y, progtext, c.w)

    # show splash screen during fetch
    if splash:
        g.content = logo(c.b) + "\n\n"
        screen_update()

    # perform fetch
    try:
        wdata = call_gdata('search', qs)
        songs = get_tracks_from_json(wdata)

    except GdataError as e:
        g.message = F('no data') % e
        g.content = logo(c.r)
        return

    if songs and pre_load:
        # preload first result url
        kwa = {"song": songs[0], "delay": 0}
        t = threading.Thread(target=preload, kwargs=kwa)
        t.start()

    if songs:
        g.model.songs = songs
        return True

    return False



def token(page):
    """ Returns a page token for a given start index. """
    index = (page or 0) * getxy().max_results
    k = index//128 - 1
    index -= 128 * k
    f = [8, index]
    if k > 0 or index > 127:
        f.append(k+1)
    f += [16, 0]
    b64 = base64.b64encode(bytes(f)).decode('utf8')
    return b64.strip('=')


def generate_search_qs(term, page=0, result_count=getxy().max_results, match='term'):
    """ Return query string. """
    if not result_count:
        result_count = getxy().max_results

    aliases = dict(views='viewCount')
    qs = {
        'q': term,
        'maxResults': result_count,
        'safeSearch': "none",
        'order': aliases.get(Config.ORDER.get, Config.ORDER.get),
        'part': 'id,snippet',
        'type': 'video',
        'key': Config.API_KEY.get
    }

    if match == 'related':
        qs['relatedToVideoId'] = term
        del qs['q']

    qs['pageToken'] = token(page)

    if Config.SEARCH_MUSIC.get:
        qs['videoCategoryId'] = 10

    return qs


def userdata_cached(userterm):
    """ Check if user name search term found in cache """
    userterm = ''.join([t.strip().lower() for t in userterm.split(' ')])
    return g.username_query_cache.get(userterm)


def cache_userdata(userterm, username, channel_id):
    """ Cache user name and channel id tuple """
    userterm = ''.join([t.strip().lower() for t in userterm.split(' ')])
    g.username_query_cache[userterm] = (username, channel_id)
    dbg('Cache data for username search query "{}": {} ({})'.format(
        userterm, username, channel_id))

    while len(g.username_query_cache) > 300:
        g.username_query_cache.popitem(last=False)
    return (username, channel_id)


def channelfromname(user):
    """ Query channel id from username. """

    cached = userdata_cached(user)
    if cached:
        user, channel_id = cached
    else:
        # if the user is looked for by their display name,
        # we have to sent an additional request to find their
        # channel id
        qs = {'part': 'id,snippet',
              'maxResults': 1,
              'q': user,
              'type': 'channel'}

        try:
            userinfo = call_gdata('search', qs)['items']
            if len(userinfo) > 0:
                snippet = userinfo[0].get('snippet', {})
                channel_id = snippet.get('channelId', user)
                username = snippet.get('title', user)
                user = cache_userdata(user, username, channel_id)[0]
            else:
                g.message = "User {} not found.".format(c.y + user + c.w)
                return

        except GdataError as e:
            g.message = "Could not retrieve information for user {}\n{}".format(
                c.y + user + c.w, e)
            dbg('Error during channel request for user {}:\n{}'.format(
                user, e))
            return

    # at this point, we know the channel id associated to a user name
    return (user, channel_id)


def usersearch(q_user, page=0, splash=True, identify='forUsername'):
    """ Fetch uploads by a YouTube user. """

    user, _, term = (x.strip() for x in q_user.partition("/"))
    if identify == 'forUsername':
        ret = channelfromname(user)
        if not ret: # Error
            return
        user, channel_id = ret

    else:
        channel_id = user

    # at this point, we know the channel id associated to a user name
    usersearch_id('/'.join([user, channel_id, term]), page, splash)


def usersearch_id(q_user, page=0, splash=True):
    """ Performs a search within a user's (i.e. a channel's) uploads
    for an optional search term with the user (i.e. the channel)
    identified by its ID """

    user, channel_id, term = (x.strip() for x in q_user.split("/"))
    query = generate_search_qs(term, page=page)
    aliases = dict(views='viewCount')  # The value of the config item is 'views' not 'viewCount'
    if Config.USER_ORDER.get:
        query['order'] = aliases.get(Config.USER_ORDER.get,
                Config.USER_ORDER.get)
    query['channelId'] = channel_id

    termuser = tuple([c.y + x + c.w for x in (term, user)])
    if term:
        msg = "Results for {1}{3}{0} (by {2}{4}{0})"
        progtext = "%s by %s" % termuser
        failmsg = "No matching results for %s (by %s)" % termuser
    else:
        msg = "Video uploads by {2}{4}{0}"
        progtext = termuser[1]
        failmsg = "User %s not found" % termuser[1]
    msg = str(msg).format(c.w, c.y, c.y, term, user)

    have_results = _search(progtext, query, splash)

    if have_results:
        g.browse_mode = "normal"
        g.message = msg
        g.last_opened = ""
        g.last_search_query = {"user": q_user}
        g.current_page = page
        g.content = generate_songlist_display(frmat="search")

    else:
        g.message = failmsg
        g.current_page = 0
        g.last_search_query = {}
        g.content = logo(c.r)


def related_search(vitem, page=0, splash=True):
    """ Fetch uploads by a YouTube user. """
    query = generate_search_qs(vitem.ytid, page, match='related')

    if query.get('videoCategoryId'):
        del query['videoCategoryId']

    t = vitem.title
    ttitle = t[:48].strip() + ".." if len(t) > 49 else t

    have_results = _search(ttitle, query, splash)

    if have_results:
        g.message = "Videos related to %s%s%s" % (c.y, ttitle, c.w)
        g.last_opened = ""
        g.last_search_query = {"related": vitem}
        g.current_page = page
        g.content = generate_songlist_display(frmat="search")

    else:
        g.message = "Related to %s%s%s not found" % (c.y, vitem.ytid, c.w)
        g.content = logo(c.r)
        g.current_page = 0
        g.last_search_query = {}


def search(term, page=0, splash=True):
    """ Perform search. """
    if not term or len(term) < 2:
        g.message = c.r + "Not enough input" + c.w
        g.content = generate_songlist_display()
        return

    logging.info("search for %s", term)
    query = generate_search_qs(term, page)
    have_results = _search(term, query, splash)

    if have_results:
        g.message = "Search results for %s%s%s" % (c.y, term, c.w)
        g.last_opened = ""
        g.last_search_query = {"term": term}
        g.browse_mode = "normal"
        g.current_page = page
        g.content = generate_songlist_display(frmat="search")

    else:
        g.message = "Found nothing for %s%s%s" % (c.y, term, c.w)
        g.content = logo(c.r)
        g.current_page = 0
        g.last_search_query = {}


def user_pls(user, page=0, splash=True):
    """ Retrieve user playlists. """
    user = {"is_user": True, "term": user}
    return pl_search(user, page=page, splash=splash)


def pl_search(term, page=0, splash=True, is_user=False):
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

    if splash:
        g.content = logo(c.g)
        prog = "user: " + term if is_user else term
        g.message = "Searching playlists for %s" % c.y + prog + c.w
        screen_update()

    if is_user:
        ret = channelfromname(term)
        if not ret: # Error
            return
        user, channel_id = ret

    else:
        # playlist search is done with the above url and param type=playlist
        logging.info("playlist search for %s", prog)
        max_results = min(getxy().max_results, 50) # Limit for playlists command
        qs = generate_search_qs(term, page, result_count=max_results)
        qs['type'] = 'playlist'
        if 'videoCategoryId' in qs:
            del qs['videoCategoryId'] # Incompatable with type=playlist

        try:
            pldata = call_gdata('search', qs)
            id_list = [i.get('id', {}).get('playlistId')
                        for i in pldata.get('items', ())]
            # page info
            get_page_info_from_json(pldata, len(id_list))
        except GdataError as e:
            g.message = F('no data') % e
            g.content = logo(c.r)
            return

    qs = {'part': 'contentDetails,snippet',
          'maxResults': 50}

    if is_user:
        if page:
            qs['pageToken'] = token(page)
        qs['channelId'] = channel_id
    else:
        qs['id'] = ','.join(id_list)

    try:
        pldata = call_gdata('playlists', qs)
        playlists = get_pl_from_json(pldata)
    except GdataError as e:
        g.message = F('no data') % e
        g.content = logo(c.r)
        return

    if playlists:
        g.last_search_query = {"playlists": {"term": term, "is_user": is_user}}
        g.browse_mode = "ytpl"
        g.current_page = page
        g.ytpls = playlists
        g.message = "Playlist results for %s" % c.y + prog + c.w
        g.content = generate_playlist_display()

    else:
        g.message = "No playlists found for: %s" % c.y + prog + c.w
        g.current_page = 0
        g.content = generate_songlist_display(zeromsg=g.message)


def get_pl_from_json(pldata):
    """ Process json playlist data. """

    try:
        items = pldata['items']

    except KeyError:
        items = []

    results = []

    for item in items:
        snippet = item['snippet']
        results.append(dict(
            link=item["id"],
            size=item["contentDetails"]["itemCount"],
            title=snippet["title"],
            author=snippet["channelTitle"],
            created=snippet["publishedAt"],
            updated=snippet['publishedAt'], #XXX Not available in API?
            description=snippet["description"]))

    return results


def paginate(items, pagesize, spacing=2, delim_fn=None):
    """ Paginate items to fit in pagesize.

    item size is defined by delim_fn.

    """
    def dfn(x):
        """ Count lines. """
        return sum(1 for char in x if char == "\n")

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


def fetch_comments(item):
    """ Fetch comments for item using gdata. """
    # pylint: disable=R0912
    # pylint: disable=R0914
    cw, ch, _ = getxy()
    ch = max(ch, 10)
    ytid, title = item.ytid, item.title
    dbg("Fetching comments for %s", c.c("y", ytid))
    writestatus("Fetching comments for %s" % c.c("y", title[:55]))
    qs = {'textFormat': 'plainText',
          'videoId': ytid,
          'maxResults': 50,
          'part': 'snippet'}

    # XXX should comment threads be expanded? this would require
    # additional requests for comments responding on top level comments

    try:
        jsdata = call_gdata('commentThreads', qs)

    except GdataError as e:
        g.message = "No comments for %s\n%s" % (item.title[:50], e)
        g.content = generate_songlist_display()
        return

    coms = jsdata.get('items', [])
    coms = [x.get('snippet', {}) for x in coms]
    coms = [x.get('topLevelComment', {}) for x in coms]
    # skip blanks
    coms = [x for x in coms if len(x.get('snippet', {}).get('textDisplay', '').strip())]
    if not len(coms):
        g.message = "No comments for %s" % item.title[:50]
        g.content = generate_songlist_display()
        return

    items = []

    for n, com in enumerate(coms, 1):
        snippet = com.get('snippet', {})
        poster = snippet.get('authorDisplayName')
        _, shortdate = yt_datetime(snippet.get('publishedAt', ''))
        text = snippet.get('textDisplay', '')
        cid = ("%s/%s" % (n, len(coms)))
        out = ("%s %-35s %s\n" % (cid, c.c("g", poster), shortdate))
        out += c.c("y", text.strip())
        items.append(out)

    cw = Config.CONSOLE_WIDTH.get

    def plain(x):
        """ Remove formatting. """
        return x.replace(c.y, "").replace(c.w, "").replace(c.g, "")

    def linecount(x):
        """ Return number of newlines. """
        return sum(1 for char in x if char == "\n")

    def longlines(x):
        """ Return number of oversized lines. """
        return sum(len(plain(line)) // cw for line in x.split("\n"))

    def linecounter(x):
        """ Return amount of space required. """
        return linecount(x) + longlines(x)

    pagenum = 0
    pages = paginate(items, pagesize=ch, delim_fn=linecounter)

    while 0 <= pagenum < len(pages):
        pagecounter = "Page %s/%s" % (pagenum + 1, len(pages))
        page = pages[pagenum]
        pagetext = ("\n\n".join(page)).strip()
        content_length = linecount(pagetext) + longlines(pagetext)
        blanks = "\n" * (-2 + ch - content_length)
        g.content = pagetext + blanks
        screen_update(fill_blank=False)
        xprint("%s : Use [Enter] for next, [p] for previous, [q] to return:"
               % pagecounter, end="")
        v = input()

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


def _make_fname(song, ext=None, av=None, subdir=None):
    """" Create download directory, generate filename. """
    # pylint: disable=E1103
    # Instance of 'bool' has no 'extension' member (some types not inferable)
    ddir = os.path.join(Config.DDIR.get, subdir) if subdir else Config.DDIR.get
    if not os.path.exists(ddir):
        os.makedirs(ddir)

    streams = get_streams(song)

    if ext:
        extension = ext

    else:
        stream = select_stream(streams, 0, audio=av == "audio", m4a_ok=True)
        extension = stream['ext']

    # filename = song.title[:59] + "." + extension
    filename = song.title + "." + extension
    filename = os.path.join(ddir, mswinfn(filename.replace("/", "-")))
    filename = filename.replace('"', '')
    return filename


def extract_metadata(name):
    """ Try to determine metadata from video title. """
    seps = name.count(" - ")
    artist = title = None

    if seps == 1:

        pos = name.find(" - ")
        artist = name[:pos].strip()
        title = name[pos + 3:].strip()

    else:
        title = name.strip()

    return dict(artist=artist, title=title)


def remux_audio(filename, title):
    """ Remux audio file. Insert limited metadata tags. """
    dbg("starting remux")
    temp_file = filename + "." + str(random.randint(10000, 99999))
    os.rename(filename, temp_file)
    meta = extract_metadata(title)
    metadata = ["title=%s" % meta["title"]]

    if meta["artist"]:
        metadata = ["title=%s" % meta["title"], "-metadata",
                    "artist=%s" % meta["artist"]]

    cmd = [g.muxapp, "-y", "-i", temp_file, "-acodec", "copy", "-metadata"]
    cmd += metadata + ["-vn", filename]
    dbg(cmd)

    try:
        with open(os.devnull, "w") as devnull:
            subprocess.call(cmd, stdout=devnull, stderr=subprocess.STDOUT)

    except OSError:
        dbg("Failed to remux audio using %s", g.muxapp)
        os.rename(temp_file, filename)

    else:
        os.unlink(temp_file)
        dbg("remuxed audio file using %s" % g.muxapp)


def transcode(filename, enc_data):
    """ Re encode a download. """
    base = os.path.splitext(filename)[0]
    exe = g.muxapp if g.transcoder_path == "auto" else g.transcoder_path

    # ensure valid executable
    if not exe or not os.path.exists(exe) or not os.access(exe, os.X_OK):
        xprint("Encoding failed. Couldn't find a valid encoder :(\n")
        time.sleep(2)
        return filename

    command = shlex.split(enc_data['command'])
    newcom, outfn = command[::], ""

    for n, d in enumerate(command):

        if d == "ENCODER_PATH":
            newcom[n] = exe

        elif d == "IN":
            newcom[n] = filename

        elif d == "OUT":
            newcom[n] = outfn = base

        elif d == "OUT.EXT":
            newcom[n] = outfn = base + "." + enc_data['ext']

    returncode = subprocess.call(newcom)

    if returncode == 0 and g.delete_orig:
        os.unlink(filename)

    return outfn


def external_download(filename, url):
    """ Perform download using external application. """
    cmd = Config.DOWNLOAD_COMMAND.get
    ddir, basename = Config.DDIR.get, os.path.basename(filename)
    cmd_list = shlex.split(cmd)

    def list_string_sub(orig, repl, lst):
        """ Replace substrings for items in a list. """
        return [x if orig not in x else x.replace(orig, repl) for x in lst]

    cmd_list = list_string_sub("%F", filename, cmd_list)
    cmd_list = list_string_sub("%d", ddir, cmd_list)
    cmd_list = list_string_sub("%f", basename, cmd_list)
    cmd_list = list_string_sub("%u", url, cmd_list)
    dbg("Downloading using: %s", " ".join(cmd_list))
    subprocess.call(cmd_list)


def _download(song, filename, url=None, audio=False, allow_transcode=True):
    """ Download file, show status.

    Return filename or None in case of user specified download command.

    """
    # pylint: disable=R0914
    # too many local variables
    # Instance of 'bool' has no 'url' member (some types not inferable)

    if not url:
        streams = get_streams(song)
        stream = select_stream(streams, 0, audio=audio, m4a_ok=True)
        url = stream['url']

    # if an external download command is set, use it
    if Config.DOWNLOAD_COMMAND.get:
        title = c.y + os.path.splitext(os.path.basename(filename))[0] + c.w
        xprint("Downloading %s using custom command" % title)
        external_download(filename, url)
        return None

    if not Config.OVERWRITE.get:
        if os.path.exists(filename):
            xprint("File exists. Skipping %s%s%s ..\n" % (c.r, filename, c.w))
            time.sleep(0.2)
            return filename

    xprint("Downloading to %s%s%s .." % (c.r, filename, c.w))
    status_string = ('  {0}{1:,}{2} Bytes [{0}{3:.2%}{2}] received. Rate: '
                     '[{0}{4:4.0f} kbps{2}].  ETA: [{0}{5:.0f} secs{2}]')

    resp = urlopen(url)
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

    active_encoder = g.encoders[Config.ENCODER.get]
    ext = filename.split(".")[-1]
    valid_ext = ext in active_encoder['valid'].split(",")

    if audio and g.muxapp:
        remux_audio(filename, song.title)

    if Config.ENCODER.get != 0 and valid_ext and allow_transcode:
        filename = transcode(filename, active_encoder)

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
    end = end or str(g.model.size)
    pattern = r'(?<![-\d])(\d+-\d+|-\d+|\d+-|\d+)(?![-\d])'
    items = re.findall(pattern, choice)
    alltracks = []

    for x in items:

        if x.startswith("-"):
            x = "1" + x

        elif x.endswith("-"):
            x = x + str(end)

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


def save_last():
    """ Save command with no playlist name. """
    if g.last_opened:
        open_save_view("save", g.last_opened)

    else:
        saveas = ""

        # save using artist name in postion 1
        if not g.model.is_empty:
            saveas = g.model.songs[0].title[:18].strip()
            saveas = re.sub(r"[^-\w]", "-", saveas, re.UNICODE)

        # loop to find next available name
        post = 0

        while g.userpl.get(saveas):
            post += 1
            saveas = g.model.songs[0].title[:18].strip() + "-" + str(post)

        open_save_view("save", saveas)


def open_save_view(action, name):
    """ Open, save or view a playlist by name.  Get closest name match. """
    name = name.replace(" ", "-")
    if action == "open" or action == "view":

        saved = g.userpl.get(name)

        if not saved:
            name = _get_near_name(name, g.userpl)
            saved = g.userpl.get(name)

        elif action == "open":
            g.browse_mode = "normal"
            g.model.songs = g.active.songs = list(saved.songs)
            g.message = F("pl loaded") % name
            g.last_opened = name
            g.last_search_query = {}
            # g.content = generate_songlist_display()
            g.content = generate_songlist_display(frmat=None)
            kwa = {"song": g.model.songs[0], "delay": 0}
            t = threading.Thread(target=preload, kwargs=kwa)
            t.start()

        elif action == "view":
            g.browse_mode = "normal"
            g.last_search_query = {}
            g.model.songs = list(saved.songs)
            g.message = F("pl viewed") % name
            g.last_opened = ""
            g.content = generate_songlist_display(frmat=None)
            # g.content = generate_songlist_display()
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
            g.userpl[name] = Playlist(name, list(g.model.songs))
            g.message = F('pl saved') % name
            save_to_file()
            g.content = generate_songlist_display(frmat=None)


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
        selection = sorted(set(selection), reverse=True)
        removed = str(tuple(reversed(selection))).replace(",", "")

        for x in selection:
            g.model.songs.pop(x - 1)

        g.message = F('songs rm') % (len(selection), removed)

    g.content = generate_songlist_display()


def down_many(dltype, choice, subdir=None):
    """ Download multiple items. """
    choice = _parse_multi(choice)
    choice = list(set(choice))
    downsongs = [g.model.songs[int(x) - 1] for x in choice]
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
            disp = re.sub(r"(Num\s*?Title.*?\n)", title, disp)
            g.content = disp
            screen_update()

            try:
                filename = _make_fname(song, None, av=av, subdir=subdir)

            except IOError as e:
                handle_error("Error for %s: %s" % (song.title, str(e)))
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
            g.message = "Saved to " + c.g + song.title + c.w

    except KeyboardInterrupt:
        msg = "Downloads interrupted!"

    finally:
        g.model.songs = temp[::]
        g.message = msg
        g.content = generate_songlist_display()


def down_plist(dltype, parturl):
    """ Download YouTube playlist. """

    plist(parturl, page=0, splash=True, dumps=True)
    title = g.pafy_pls[parturl]['title']
    subdir = mswinfn(title.replace("/", "-"))
    down_many(dltype, "1-", subdir=subdir)


def down_user_pls(dltype, user):
    """ Download all user playlists. """
    user_pls(user)
    for pl in g.ytpls:
        down_plist(dltype, pl.get('link'))

    return


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
        nofs = "-w" in pre + post or "-v" in pre + post

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
    play(options, "1-" + str(len(g.model.songs)))


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
    if g.preload_disabled:
        return

    ytid = song.ytid
    g.preloading.append(ytid)
    time.sleep(delay)
    video = Config.SHOW_VIDEO.get
    video = True if override in ("fullscreen", "window") else video
    video = False if override == "audio" else video

    try:
        stream = get_streams(song)
        m4a = "mplayer" not in Config.PLAYER.get
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

    n = 0
    while 0 <= n <= len(songlist)-1:
        song = songlist[n]
        g.content = playback_progress(n, songlist, repeat=repeat)

        if not g.command_line:
            screen_update(fill_blank=False)

        hasnext = len(songlist) > n + 1

        if hasnext:
            nex = songlist[n + 1]
            kwa = {"song": nex, "override": override}
            t = threading.Thread(target=preload, kwargs=kwa)
            t.start()

        set_window_title(song.title + " - mpsyt")
        try:
            returncode = playsong(song, override=override)

        except KeyboardInterrupt:
            logging.info("Keyboard Interrupt")
            xprint(c.w + "Stopping...                          ")
            reset_terminal()
            g.message = c.y + "Playback halted" + c.w
            break
        set_window_title("mpsyt")

        if returncode == 42:
            n -= 1

        elif returncode == 43:
            break

        else:
            n += 1

        if n == -1:
            n = len(songlist) - 1 if repeat else 0

        elif n == len(songlist) and repeat:
            n = 0

    g.content = generate_songlist_display()


def show_help(choice):
    """ Print help message. """
    helps = {"download": ("playback dl listen watch show repeat playing"
                          "show_video playurl dlurl d da dv all *"
                          " play".split()),

             "dl-command": ("dlcmd dl-cmd download-cmd dl_cmd download_cmd "
                            "download-command download_command".split()),

             "encode": ("encoding transcoding transcode wma mp3 format "
                        "encode encoder".split()),

             "invoke": "command commands mpsyt invocation".split(),

             "search": ("user userpl pl pls r n p url album "
                        "editing result results related remove swop".split()),

             "edit": ("editing manupulate manipulating rm mv sw edit move "
                      "swap shuffle".split()),

             "tips": ("undump dump -f -w -a adv advanced".split(" ")),

             "basic": ("basic comment basics c copy clipboard comments u "
                       "i".split()),

             "config": ("set checkupdate colours colors ddir directory player "
                        "arguments args playerargs music search_music keys "
                        "status show_status show_video video configuration "
                        "fullscreen full screen folder player mpv mplayer"
                        " settings default reset configure audio results "
                        "max_results size lines rows height window "
                        "position window_pos quality resolution max_res "
                        "columns width console overwrite".split()),

             "playlists": ("save rename delete move rm ls mv sw add vp open"
                           " view".split())}

    for topic, aliases in helps.items():

        if choice in aliases:
            choice = topic
            break

    choice = "menu" if not choice else choice
    out, all_help = "", g.helptext
    help_names = [x[0] for x in all_help]
    choice = _get_near_name(choice, help_names)

    def indent(x):
        """ Indent. """
        return "\n  ".join(x.split("\n"))

    if choice == "menu" or choice not in help_names:
        out += "  %sHelp Topics%s" % (c.ul, c.w)
        out += F('help topic', 2, 1)

        for x in all_help:
            out += ("\n%s     %-10s%s : %s" % (c.y, x[0], c.w, x[1]))

        out += "\n"
        g.content = out

    else:
        choice = help_names.index(choice)
        g.content = indent(all_help[choice][2])


def quits(showlogo=True):
    """ Exit the program. """
    if has_readline:
        readline.write_history_file(g.READLINE_FILE)
        dbg("Saved history file")

    savecache()

    msg = g.blank_text + logo(c.r, version=__version__) if showlogo else ""
    xprint(msg + F("exitmsg", 2))

    if Config.CHECKUPDATE.get and showlogo:

        try:
            url = "https://github.com/np1/mps-youtube/raw/master/VERSION"
            v = urlopen(url, timeout=1).read().decode()
            v = re.search(r"^version\s*([\d\.]+)\s*$", v, re.MULTILINE)

            if v:
                v = v.group(1)

                if v > __version__:
                    vermsg = "\nA newer version is available (%s)\n" % v
                    xprint(vermsg)

        except (URLError, HTTPError, socket.timeout):
            dbg("check update timed out")

    sys.exit()


def get_dl_data(song, mediatype="any"):
    """ Get filesize and metadata for all streams, return dict. """
    def mbsize(x):
        """ Return size in MB. """
        return str(int(x / (1024 ** 2)))

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

        try:
            size = mbsize(stream.get_filesize())

        except TypeError:
            dbg(c.r + "---Error getting stream size" + c.w)
            size = 0

        item = {'mediatype': stream.mediatype,
                'size': size,
                'ext': stream.extension,
                'quality': stream.quality,
                'notes': stream.notes,
                'url': stream.url}

        dldata.append(item)

    writestatus("")
    return dldata, p


def menu_prompt(model, prompt=" > ", rows=None, header=None, theading=None,
                footer=None, force=0):
    """ Generate a list of choice, returns item from model. """
    content = ""

    for x in header, theading, rows, footer:
        if isinstance(x, list):

            for line in x:
                content += line + "\n"

        elif isinstance(x, str):
            content += x + "\n"

    g.content = content
    screen_update()

    choice = input(prompt)

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
    model = {str(n + 1): (x['url'], x['ext']) for n, x in ed}
    url, ext = menu_prompt(model, "Download number: ", *dl_text)
    url2 = ext2 = None

    if ext == "m4v" and g.muxapp and not Config.DOWNLOAD_COMMAND.get:
        # offer mux if not using external downloader
        dl_data, p = get_dl_data(song, mediatype="audio")
        dl_text = gen_dl_text(dl_data, song, p)
        au_choices = "1" if len(dl_data) == 1 else "1-%s" % len(dl_data)
        footer = [F('-audio'), F('select mux') % au_choices]
        dl_text = tuple(dl_text[0:3]) + (footer,)
        aext = ("ogg", "m4a")
        model = [x['url'] for x in dl_data if x['ext'] in aext]
        ed = enumerate(dl_data)
        model = {str(n + 1): (x['url'], x['ext']) for n, x in ed}
        prompt = "Audio stream: "
        url2, ext2 = menu_prompt(model, prompt, *dl_text)

    return url, ext, url2, ext2


def gen_dl_text(ddata, song, p):
    """ Generate text for dl screen. """
    hdr = []
    hdr.append("  %s%s%s" % (c.r, song.title, c.w))
    author = p.author
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
    """ Download a track or playlist by menu item number. """
    # This function needs refactoring!
    # pylint: disable=R0912
    # pylint: disable=R0914
    if g.browse_mode == "ytpl" and dltype in ("da", "dv"):
        plid = g.ytpls[int(num) - 1]["link"]
        down_plist(dltype, plid)
        return

    elif g.browse_mode == "ytpl":
        g.message = "Use da or dv to specify audio / video playlist download"
        g.message = c.y + g.message + c.w
        g.content = generate_songlist_display()
        return

    elif g.browse_mode != "normal":
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

            if url_au and ext_au:
                # downloading video and audio stream for muxing
                audio = False
                filename_au = _make_fname(song, ext_au)
                args_au = (song, filename_au, url_au)

            else:
                audio = ext in ("m4a", "ogg")

            kwargs = dict(audio=audio)

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
        if f:
            g.message = "Saved to " + c.g + f + c.w

        if url_au:
            dl_filenames += [args_au[1]]
            _download(*args_au, allow_transcode=False, **kwargs)

    except KeyboardInterrupt:
        g.message = c.r + "Download halted!" + c.w

        try:
            for downloaded in dl_filenames:
                os.remove(downloaded)

        except IOError:
            pass

    if url_au:
        # multiplex
        mux_cmd = "APP -i VIDEO -i AUDIO -c copy OUTPUT".split()
        mux_cmd = "%s -i %s -i %s -c copy %s"
        mux_cmd = [g.muxapp, "-i", args[1], "-i", args_au[1], "-c",
                   "copy", args[1][:-3] + "mp4"]

        try:
            subprocess.call(mux_cmd)
            g.message = "Saved to :" + c.g + mux_cmd[7] + c.w
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
        userinput = input(c.r + " > " + c.w)

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

    if nums:
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
        if not b and a not in g.userpl:
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
        songlist_rm_add("add", "-" + str(size))


def nextprev(np, page=None):
    """ Get next / previous search results. """
    glsq = g.last_search_query
    content = g.model.songs
    max_results = getxy().max_results

    if "user" in g.last_search_query:
        function, query = usersearch_id, glsq['user']

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
        if len(content) == max_results and glsq:
            if (g.current_page + 1) * max_results < 500:
                if g.more_pages:
                    g.current_page += 1
                    good = True

    elif np == "p":

        if g.last_search_query:
            if page and int(page) in range(1,20):
                g.current_page = int(page)-1
                good = True

            elif g.current_page > 0:
                g.current_page -= 1
                good = True

    if good:
        function(query, page=g.current_page, splash=True)

    else:
        norp = "next" if np == "n" else "previous"
        g.message = "No %s items to display" % norp

    g.content = generate_songlist_display(frmat="search")
    return good


def user_more(num):
    """ Show more videos from user of vid num. """
    if g.browse_mode != "normal":
        g.message = "User uploads must refer to a specific video item"
        g.message = c.y + g.message + c.w
        g.content = generate_songlist_display()
        return

    g.current_page = 0
    item = g.model.songs[int(num) - 1]
    channel_id = g.meta.get(item.ytid, {}).get('uploader')
    user = g.meta.get(item.ytid, {}).get('uploaderName')
    usersearch_id('/'.join([user, channel_id, '']), 0, True)


def related(num):
    """ Show videos related to to vid num. """
    if g.browse_mode != "normal":
        g.message = "Related items must refer to a specific video item"
        g.message = c.y + g.message + c.w
        g.content = generate_songlist_display()
        return

    g.current_page = 0
    item = g.model.songs[int(num) - 1]
    related_search(item)


def clip_copy(num):
    """ Copy item to clipboard. """
    if g.browse_mode == "ytpl":

        p = g.ytpls[int(num) - 1]
        link = "https://youtube.com/playlist?list=%s" % p['link']

    elif g.browse_mode == "normal":
        item = (g.model.songs[int(num) - 1])
        link = "https://youtube.com/watch?v=%s" % item.ytid

    else:
        g.message = "clipboard copy not valid in this mode"
        g.content = generate_songlist_display()
        return

    if has_xerox:

        try:
            xerox.copy(link)
            g.message = c.y + link + c.w + " copied"
            g.content = generate_songlist_display()

        except xerox.base.ToolNotFound as e:
            xprint(link)
            xprint("Error - couldn't copy to clipboard.")
            xprint(e.__doc__)
            xprint("")
            input("Press Enter to continue.")
            g.content = generate_songlist_display()

    else:
        g.message = "xerox module must be installed for clipboard support\n"
        g.message += "see https://pypi.python.org/pypi/xerox/"
        g.content = generate_songlist_display()

def mix(num):
    """ Retrieves the YouTube mix for the selected video. """
    g.content = g.content or generate_songlist_display()
    if g.browse_mode != "normal":
        g.message = F('mix only videos')
    else:
        item = (g.model.songs[int(num) - 1])
        if item is None:
            g.message = F('invalid item')
            return
        item = get_pafy(item)
        # Mix playlists are made up of 'RD' + video_id
        try:
            plist("RD" + item.videoid)
        except OSError:
            g.message = F('no mix')


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

        created = yt_datetime(p['created'])[0]
        updated = yt_datetime(p['updated'])[0]
        out = c.ul + "Playlist Info" + c.w + "\n\n"
        out += p['title']
        out += "\n" + ytpl_desc
        out += ("\n\nAuthor     : " + p['author'])
        out += "\nSize       : " + str(p['size']) + " videos"
        out += "\nLikes      : " + str(ytpl_likes)
        out += "\nDislikes   : " + str(ytpl_dislikes)
        out += "\nCreated    : " + time.strftime("%x %X", created)
        out += "\nUpdated    : " + time.strftime("%x %X", updated)
        out += "\nID         : " + str(p['link'])
        out += ("\n\n%s[%sPress enter to go back%s]%s" % (c.y, c.w, c.y, c.w))
        g.content = out

    elif g.browse_mode == "normal":
        g.content = logo(c.b)
        screen_update()
        writestatus("Fetching video metadata..")
        item = (g.model.songs[int(num) - 1])
        get_streams(item)
        p = get_pafy(item)
        pub = time.strptime(str(p.published), "%Y-%m-%d %H:%M:%S")
        writestatus("Fetched")
        out = c.ul + "Video Info" + c.w + "\n\n"
        out += p.title or ""
        out += "\n" + (p.description or "")
        out += "\n\nAuthor     : " + str(p.author)
        out += "\nPublished  : " + time.strftime("%c", pub)
        out += "\nView count : " + str(p.viewcount)
        out += "\nRating     : " + str(p.rating)[:4]
        out += "\nLikes      : " + str(p.likes)
        out += "\nDislikes   : " + str(p.dislikes)
        out += "\nCategory   : " + str(p.category)
        out += "\nLink       : " + "https://youtube.com/watch?v=%s" % p.videoid
        out += "\n\n%s[%sPress enter to go back%s]%s" % (c.y, c.w, c.y, c.w)
        g.content = out


def play_url(url, override):
    """ Open and play a youtube video url. """
    override = override if override else "_"
    g.browse_mode = "normal"
    yt_url(url, print_title=1)

    if len(g.model.songs) == 1:
        play(override, "1", "_")

    if g.command_line:
        sys.exit()


def dl_url(url):
    """ Open and prompt for download of youtube video url. """
    g.browse_mode = "normal"
    yt_url(url)

    if len(g.model.songs) == 1:
        download("download", "1")

    if g.command_line:
        sys.exit()


def yt_url(url, print_title=0):
    """ Acess a video by url. """
    try:
        p = pafy.new(url)

    except (IOError, ValueError) as e:
        g.message = c.r + str(e) + c.w
        g.content = g.content or generate_songlist_display(zeromsg=g.message)
        return

    g.browse_mode = "normal"
    v = Video(p.videoid, p.title, p.length)
    g.model.songs = [v]

    if not g.command_line:
        g.content = generate_songlist_display()

    if print_title:
        xprint(v.title)


def dump(un):
    """ Show entire playlist. """
    if g.last_search_query.get("playlist") and not un:
        plist(g.last_search_query['playlist'], dumps=True)

    elif g.last_search_query.get("playlist") and un:
        plist(g.last_search_query['playlist'], page=0, dumps=False)

    else:
        un = "" if not un else un
        g.message = "%s%sdump%s may only be used on an open YouTube playlist"
        g.message = g.message % (c.y, un, c.w)
        g.content = generate_songlist_display()


def plist(parturl, page=0, splash=True, dumps=False):
    """ Retrieve YouTube playlist. """
    max_results = getxy().max_results

    if "playlist" in g.last_search_query and\
            parturl == g.last_search_query['playlist']:

        # go to pagenum
        s = page * max_results
        e = (page + 1) * max_results

        if dumps:
            s, e = 0, 99999

        g.model.songs = g.ytpl['items'][s:e]
        g.more_pages = e < len(g.ytpl['items'])
        g.content = generate_songlist_display()
        g.message = "Showing YouTube playlist: %s" % c.y + g.ytpl['name'] + c.w
        g.current_page = page
        return

    if splash:
        g.content = logo(col=c.b)
        g.message = "Retrieving YouTube playlist"
        screen_update()

    dbg("%sFetching playlist using pafy%s", c.y, c.w)
    yt_playlist = pafy.get_playlist(parturl)
    g.pafy_pls[parturl] = yt_playlist
    ytpl_items = yt_playlist['items']
    ytpl_title = yt_playlist['title']
    g.result_count = len(ytpl_items)
    g.more_pages = max_results < len(ytpl_items)

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
    g.current_page = 0
    g.model.songs = songs[:max_results]
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
    g.url_memo = collections.OrderedDict()
    dbg("%scache cleared%s", c.p, c.w)
    g.message = "cache cleared"


def show_message(message, col=c.r, update=False):
    """ Show message using col, update screen if required. """
    g.content = generate_songlist_display()
    g.message = col + message + c.w

    if update:
        screen_update()


def _do_query(url, query, err='query failed', cache=True, report=False):
    """ Perform http request using mpsyt user agent header.

    if cache is True, memo is utilised
    if report is True, return whether response is from memo

    """
    # create url opener
    ua = "mps-youtube/%s ( %s )" % (__version__, __url__)
    mpsyt_opener = build_opener()
    mpsyt_opener.addheaders = [('User-agent', ua)]

    # convert query to sorted list of tuples (needed for consistent url_memo)
    query = [(k, query[k]) for k in sorted(query.keys())]
    url = "%s?%s" % (url, urlencode(query))

    try:
        wdata = mpsyt_opener.open(url).read().decode()

    except (URLError, HTTPError) as e:
        g.message = "%s: %s (%s)" % (err, e, url)
        g.content = logo(c.r)
        return None if not report else (None, False)

    return wdata if not report else (wdata, False)


def _best_song_match(songs, title, duration):
    """ Select best matching song based on title, length.

    Score from 0 to 1 where 1 is best.

    """
    # pylint: disable=R0914
    seqmatch = difflib.SequenceMatcher

    def variance(a, b):
        """ Return difference ratio. """
        return float(abs(a - b)) / max(a, b)

    candidates = []

    ignore = "music video lyrics new lyrics video audio".split()
    extra = "official original vevo".split()

    for song in songs:
        dur, tit = int(song.length), song.title
        dbg("Title: %s, Duration: %s", tit, dur)

        for word in extra:
            if word in tit.lower() and word not in title.lower():
                pattern = re.compile(word, re.I)
                tit = pattern.sub("", tit)

        for word in ignore:
            if word in tit.lower() and word not in title.lower():
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
    # pylint: disable=R0914
    dbg("artists is %s", artist)
    dbg("title is %s", title)
    title_artist_str = c.g + title + c.w, c.g + artist + c.w
    xprint("\nSearching for %s by %s\n\n" % title_artist_str)

    def dtime(x):
        """ Format time to M:S. """
        return time.strftime('%M:%S', time.gmtime(int(x)))

    # do matching
    for track in mb_tracks:
        ttitle = track['title']
        length = track['length']
        xprint("Search :  %s%s - %s%s - %s" % (c.y, artist, ttitle, c.w,
                                               dtime(length)))
        q = "%s %s" % (artist, ttitle)
        w = q = ttitle if artist == "Various Artists" else q
        query = generate_search_qs(w, 0, result_count=50)
        dbg(query)
        have_results = _search(q, query, splash=False, pre_load=False)

        if not have_results:
            xprint(c.r + "Nothing matched :(\n" + c.w)
            continue

        results = g.model.songs
        s, score = _best_song_match(results, artist + " " + ttitle, length)
        cc = c.g if score > 85 else c.y
        cc = c.r if score < 75 else cc
        xprint("Matched:  %s%s%s - %s \n[%sMatch confidence: "
               "%s%s]\n" % (c.y, s.title, c.w, fmt_time(s.length),
                            cc, score, c.w))
        yield s


def _get_mb_tracks(albumid):
    """ Get track listing from MusicBraiz by album id. """
    ns = {'mb': 'http://musicbrainz.org/ns/mmd-2.0#'}
    url = "http://musicbrainz.org/ws/2/release/" + albumid
    query = {"inc": "recordings"}
    wdata = _do_query(url, query, err='album search error')

    if not wdata:
        return None

    root = ET.fromstring(wdata)
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
    root = ET.fromstring(wdata)
    rlist = root.find("mb:release-list", namespaces=ns)

    if int(rlist.get('count')) == 0:
        return None

    album = rlist.find("mb:release", namespaces=ns)
    artist = album.find("./mb:artist-credit/mb:name-credit/mb:artist",
                        namespaces=ns).find("mb:name", namespaces=ns).text
    title = album.find("mb:title", namespaces=ns).text
    aid = album.get('id')
    return dict(artist=artist, title=title, aid=aid)


def search_album(term, page=0, splash=True):
    """Search for albums. """
    # pylint: disable=R0914,R0912
    if not term:
        show_message("Enter album name:", c.g, update=True)
        term = input("> ")

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

    if splash:
        g.message, g.content = out, logo(c.b)
        screen_update()

    prompt = "Artist? [%s] > " % album['artist']
    xprint(prompt, end="")
    artistentry = input().strip()

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

    screen_update()
    entry = input("Continue? [Enter] > ")

    if entry == "":
        pass

    else:
        show_message("Album search abandoned!")
        return

    songs = []
    xprint(g.blank_text)
    itt = _match_tracks(artist, title, mb_tracks)

    stash = Config.SEARCH_MUSIC.get, Config.ORDER.get
    Config.SEARCH_MUSIC.value = True
    Config.ORDER.value = "relevance"

    try:
        songs.extend(itt)

    except KeyboardInterrupt:
        xprint("%sHalted!%s" % (c.r, c.w))

    finally:
        Config.SEARCH_MUSIC.value, Config.ORDER.value = stash

    if songs:
        g.model.songs = songs
        kwa = {"song": songs[0], "delay": 0}
        t = threading.Thread(target=preload, kwargs=kwa)
        t.start()
        xprint("\n%s / %s songs matched" % (len(songs), len(mb_tracks)))
        input("Press Enter to continue")
        g.message = "Contents of album %s%s - %s%s %s(%d/%d)%s:" % (
            c.y, artist, title, c.w, c.b, len(songs), len(mb_tracks), c.w)
        g.last_opened = ""
        g.last_search_query = ""
        g.current_page = page
        g.content = generate_songlist_display()

    else:
        g.message = "Found no album tracks for %s%s%s" % (c.y, title, c.w)
        g.content = generate_songlist_display()
        g.current_page = 0
        g.last_search_query = ""


def show_encs():
    """ Display available encoding presets. """
    encs = g.encoders
    out = "%sEncoding profiles:%s\n\n" % (c.ul, c.w)

    for x, e in enumerate(encs):
        sel = " (%sselected%s)" % (c.y, c.w) if Config.ENCODER.get == x else ""
        out += "%2d. %s%s\n" % (x, e['name'], sel)

    g.content = out
    message = "Enter %sset encoder <num>%s to select an encoder"
    g.message = message % (c.g, c.w)


def matchfunction(func, regex, userinput):
    """ Match userinput against regex.

    Call func, return True if matches.

    """
    if regex.match(userinput):
        matches = regex.match(userinput).groups()
        dbg("input: %s", userinput)
        dbg("function call: %s", func.__name__)
        dbg("regx matches: %s", matches)

        if g.debug_mode:
            func(*matches)

        else:

            try:
                func(*matches)

            except IndexError:
                g.message = F('invalid range')
                g.content = g.content or generate_songlist_display()

            except (ValueError, IOError) as e:
                g.message = F('cant get track') % str(e)
                g.content = g.content or\
                    generate_songlist_display(zeromsg=g.message)

        return True


def main():
    """ Main control loop. """
    set_window_title("mpsyt")

    if not g.command_line:
        g.content = logo(col=c.g, version=__version__) + "\n\n"
        g.message = "Enter /search-term to search or [h]elp"
        screen_update()

    # open playlists from file
    convert_playlist_to_v2()
    open_from_file()

    # get cmd line input
    arg_inp = " ".join(sys.argv[1:])

    # input types
    word = r'[^\W\d][-\w\s]{,100}'
    rs = r'(?:repeat\s*|shuffle\s*|-a\s*|-v\s*|-f\s*|-w\s*)'
    pl = r'(?:.*=|)([-_a-zA-Z0-9]{18,50})(?:(?:\&\#).*|$)'
    regx = {
        ls: r'ls$',
        vp: r'vp$',
        mix: r'mix\s*(\d{1,4})$',
        dump: r'(un)?dump',
        play: r'(%s{0,3})([-,\d\s]{1,250})\s*(%s{0,3})$' % (rs, rs),
        info: r'i\s*(\d{1,4})$',
        quits: r'(?:q|quit|exit)$',
        plist: r'pl\s+%s' % pl,
        yt_url: r'url\s(.*[-_a-zA-Z0-9]{11}.*$)',
        search: r'(?:search|\.|/)\s*([^./].{1,500})',
        dl_url: r'dlurl\s(.*[-_a-zA-Z0-9]{11}.*$)',
        play_pl: r'play\s+(%s|\d+)$' % word,
        related: r'r\s?(\d{1,4})$',
        download: r'(dv|da|d|dl|download)\s*(\d{1,4})$',
        play_url: r'playurl\s(.*[-_a-zA-Z0-9]{11}[^\s]*)(\s-(?:f|a|w))?$',
        comments: r'c\s?(\d{1,4})$',
        nextprev: r'(n|p)\s*(\d{1,2})?$',
        play_all: r'(%s{0,3})(?:\*|all)\s*(%s{0,3})$' % (rs, rs),
        user_pls: r'u(?:ser)?pl\s(.*)$',
        save_last: r'save\s*$',
        pl_search: r'(?:\.\.|\/\/|pls(?:earch)?\s)\s*(.*)$',
        # setconfig: r'set\s+([-\w]+)\s*"?([^"]*)"?\s*$',
        setconfig: r'set\s+([-\w]+)\s*(.*?)\s*$',
        clip_copy: r'x\s*(\d+)$',
        down_many: r'(da|dv)\s+((?:\d+\s\d+|-\d|\d+-|\d,)(?:[\d\s,-]*))\s*$',
        show_help: r'(?:help|h)(?:\s+([-_a-zA-Z]+)\s*)?$',
        show_encs: r'encoders?\s*$',
        user_more: r'u\s?([\d]{1,4})$',
        down_plist: r'(da|dv)pl\s+%s' % pl,
        clearcache: r'clearcache$',
        usersearch: r'user\s+([^\s].{1,})$',
        shuffle_fn: r'\s*(shuffle)\s*$',
        add_rm_all: r'(rm|add)\s(?:\*|all)$',
        showconfig: r'(set|showconfig)\s*$',
        search_album: r'album\s*(.{0,500})',
        playlist_add: r'add\s*(-?\d[-,\d\s]{1,250})(%s)$' % word,
        down_user_pls: r'(da|dv)upl\s+(.*)$',
        open_save_view: r'(open|save|view)\s*(%s)$' % word,
        songlist_mv_sw: r'(mv|sw)\s*(\d{1,4})\s*[\s,]\s*(\d{1,4})$',
        songlist_rm_add: r'(rm|add)\s*(-?\d[-,\d\s]{,250})$',
        playlist_rename: r'mv\s*(%s\s+%s)$' % (word, word),
        playlist_remove: r'rmp\s*(\d+|%s)$' % word,
        open_view_bynum: r'(open|view)\s*(\d{1,4})$',
        playlist_rename_idx: r'mv\s*(\d{1,3})\s*(%s)\s*$' % word}

    # compile regexp's
    regx = {func: re.compile(val, re.UNICODE) for func, val in regx.items()}
    prompt = "> "
    arg_inp = arg_inp.replace(r",,", "[mpsyt-comma]")
    arg_inp = arg_inp.split(",")

    while True:
        next_inp = ""

        if len(arg_inp):
            arg_inp, next_inp = arg_inp[1:], arg_inp[0].strip()
            next_inp = next_inp.replace("[mpsyt-comma]", ",")

        try:
            userinput = next_inp or input(prompt).strip()

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
    xprint(get_version_info())
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

if "--no-autosize" in sys.argv:
    list_update("--no-autosize", sys.argv, remove=True)
    g.detectable_size = False

def dbg(*args):
    """Emit a debug message."""
    # Uses xenc to deal with UnicodeEncodeError when writing to terminal
    logging.debug(xenc(i) for i in args)

g.helptext = [
    ("basic", "Basics", """

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
    {2}x <number>{1} - copy item <number> url to clipboard (requires xerox)

    {2}q{1}, {2}quit{1} - exit mpsyt
""".format(c.ul, c.w, c.y)),
    ("search", "Searching and Retrieving", """
{0}Searching and Retrieving{1}

{2}set search_music false{1} - search all YouTube categories.
{2}set search_music true{1}  - search only YouTube music category.

{2}/<query>{1} or {2}.<query>{1} to search for videos. e.g., {2}/daft punk{1}
{2}//<query>{1} or {2}..<query>{1} - search for YouTube playlists. e.g., \
{2}//80's music{1}
{2}n{1} and {2}p{1} - continue search to next/previous pages.
{2}p <number>{1} - switch to page <number>.

{2}album <album title>{1} - Search for matching tracks using album title
{2}user <username>{1} - list YouTube uploads by <username>.
{2}user <username>/<query>{1} - as above, but matches <query>.
{2}userpl <username>{1} - list YouTube playlists created by <username>.
{2}pl <url or id>{1} - Open YouTube playlist by url or id.
{2}url <url or id>{1} - Retrieve specific YouTube video by url or id.

{2}r <number>{1} - show videos related to video <number>.
{2}u <number>{1} - show videos uploaded by uploader of video <number>.
{2}c <number>{1} - view comments for video <number>
""".format(c.ul, c.w, c.y)),

    ("edit", "Editing / Manipulating Results", """
{0}Editing and Manipulating Results{1}

{2}rm <number(s)>{1} - remove items from displayed results.
{2}sw <number>,<number>{1} - swap two items.
{2}mv <number>,<number>{1} - move item <number> to position <number>.
{2}save <name>{1} - save displayed items as a local playlist.
{2}mix <number>{1} - show YouTube mix playlist from item in results.

{2}shuffle{1} - Shuffle the displayed results.
""".format(c.ul, c.w, c.y)),

    ("download", "Downloading and Playback", """
{0}Downloading and Playback{1}

{2}set show_video true{1} - play video instead of audio.

{2}<number(s)>{1} - play specified items, separated by commas.
              e.g., {2}1-3,5{1} plays items 1, 2, 3 and 5

{2}d <number>{1} - view downloads available for an item.
{2}da <number(s)>{1} - download best available audio file(s).
{2}dv <number(s)>{1} - download best available video file(s).
{2}dapl <url or id>{1} - download YouTube playlist (audio) by url or id.
{2}dvpl <url or id>{1} - download YouTube playlist (video) by url or id.
{2}daupl <username>{1} - download user's YouTube playlists (audio).
{2}dvupl <username>{1} - download user's YouTube playlists (video).
{2}dlurl <url or id>{1} download a YouTube video by url or video id.
{2}playurl <url or id>{1} play a YouTube video by url or id.

{2}all{1} or {2}*{1} - play all displayed items.
{2}repeat <number(s)>{1} - play and repeat the specified items.
{2}shuffle <number(s)>{1} - play specified items in random order.
""".format(c.ul, c.w, c.y)),

    ("dl-command", "Downloading Using External Application", """
{0}Download Using A Custom Application{1}

Use {2}set download_command <command>{1} to specify a custom command to use for
downloading.

mps-youtube will make the following substitutions:

%u - url of the remote file to download
%d - download directory as set in DDIR in mps-youtube config
%f - filename (determined by title and filetype)
%F - full file path (%d/%f)

for example, to download using aria2c (http://aria2.sourceforge.net), enter:

    {2}set download_command aria2c --dir=%d --out=%f %u{1}

Note that using a custom download command does not support transcoding the
downloaded file to another format using mps-youtube.
""".format(c.ul, c.w, c.y)),


    ("encode", "Encoding to MP3 and other formats", """
{0}Encoding to MP3 and other formats{1}

Enter {2}encoders{1} to view available encoding presets
Enter {2}set encoder <number>{1} to apply an encoding preset for downloads

This feature requires that ffmpeg or avconv is installed on your system and is
available in the system path.

The encoding presets can be modified by editing the text config file which
resides at:
   {3}
""".format(c.ul, c.w, c.y, g.TCFILE)),

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
""".format(c.ul, c.w, c.y)),

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
""".format(c.ul, c.w, c.y)),

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
{2}set download_command <command>{1} - type {2}help dl-command{1} for info
{2}set encoder <number>{1} - set encoding preset for downloaded files
{2}set fullscreen true|false{1} - output video content in full-screen mode
{2}set max_res <number>{1} - play / download maximum video resolution height{3}
{2}set notifier <notifier app>{1} - call <notifier app> with each new song title
{2}set order <relevance|date|views|rating>{1} search result ordering
{2}set user_order <<nothing>|relevance|date|views|rating>{1} user upload list
    result ordering, leave blank for the same as order setting
{2}set overwrite true|false{1} - overwrite existing files (skip if false)
{2}set player <player app>{1} - use <player app> for playback
{2}set playerargs <args>{1} - use specified arguments with player
{2}set search_music true|false{1} - search only music (all categories if false)
{2}set show_mplayer_keys true|false{1} - show keyboard help for mplayer and mpv
{2}set show_status true|false{1} - show status messages and progress
{2}set show_video true|false{1} - show video output (audio only if false)
{2}set window_pos <top|bottom>-<left|right>{1} - set player window position
{2}set window_size <number>x<number>{1} - set player window width & height
{2}set api_key <key>{1} - use a different API key for accessing the YouTube Data API
""".format(c.ul, c.w, c.y, '\n{0}set max_results <number>{1} - show <number> re'
           'sults when searching (max 50)'.format(c.y, c.w) if not
           g.detectable_size else '')),

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
""".format(c.ul, c.w, c.y)),

    ("new", "New Features", """
{0}New Features in v0.2.2{1}

 - Display playing resolution / bitrate in status line (Brebiche38)

 - Skip to previously played item (ids1024)

 - Enable custom keymap using mplayer/mpv input.conf file (ids1024)

 - Enable custom downloader application (ids1024 & np1){2}

""".format(c.ul, c.w, c.y))]

if __name__ == "__main__":
    init()
    main()
