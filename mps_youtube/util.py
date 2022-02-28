import collections
import ctypes
import json
import logging
import os
import platform
import re
import subprocess
import sys
import time
import unicodedata
import urllib
from datetime import datetime, timezone
from importlib import import_module

from . import c, description_parser, g, terminalsize
from .playlist import Video

macos = platform.system() == "Darwin"

mswin = os.name == "nt"
not_utf8_environment = mswin or (
    "UTF-8" not in sys.stdout.encoding if sys.stdout.encoding else False
)

XYTuple = collections.namedtuple('XYTuple', 'width height max_results')


class IterSlicer():
    """ Class that takes an iterable and allows slicing,
        loading from the iterable as needed."""

    def __init__(self, iterable, length=None):
        self.ilist = []
        self.iterable = iter(iterable)
        self.length = length
        if length is None:
            try:
                self.length = len(iterable)
            except TypeError:
                pass

    def __getitem__(self, sliced):
        if isinstance(sliced, slice):
            stop = sliced.stop
        else:
            stop = sliced
        # To get the last item in an iterable, must iterate over all items
        if (stop is None) or (stop < 0):
            stop = None
        while (stop is None) or (stop > len(self.ilist) - 1):
            try:
                self.ilist.append(next(self.iterable))
            except StopIteration:
                break

        return self.ilist[sliced]

    def __len__(self):
        if self.length is None:
            self.length = len(self[:])
        return self.length


def has_exefile(filename):
    """ Check whether file exists in path and is executable.

    :param filename: name of executable
    :type filename: str
    :returns: Path to file or False if not found
    :rtype: str or False
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


def dbg(*args):
    """Emit a debug message."""
    # Uses xenc to deal with UnicodeEncodeError when writing to terminal
    logging.debug(*(xenc(i) for i in args))


def utf8_replace(txt):
    """
    Replace unsupported characters in unicode string.

    :param txt: text to filter
    :type txt: str
    :returns: Unicode text without any characters unsupported by locale
    :rtype: str
    """
    sse = sys.stdout.encoding
    txt = str(txt)
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

def sanitize_filename(filename, ignore_slashes=False):
    """ Sanitize filename """
    if not ignore_slashes:
        filename = filename.replace('/', '-')
    if macos:
        filename = filename.replace(':', '_')
    if mswin:
        filename = utf8_replace(filename) if not_utf8_environment else filename
        allowed = re.compile(r'[^\\?*$\'"%&:<>|]')
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
            return name
    return begin


def F(key, nb=0, na=0, textlib=None):
    """Format text.

    :param nb: newline before
    :type nb: int
    :param na: newline after
    :type na: int
    :param textlib: the dictionary to use (defaults to g.text if not given)
    :type textlib: dict
    :returns: A string, potentially containing one or more %s
    :rtype: str
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
    """
    Get pafy object for an item.

    :param item: video to retrieve
    :type item: :class:`mps_youtube.playlist.Video` or str
    :param force: ignore cache and retrieve anyway
    :type force: bool
    :param callback: callpack to pass to pafy
    :type callback: func
    :rtype: Pafy
    """

    if isinstance(item, Video):
        ytid = item.ytid
    else:
        ytid = item
    callback_fn = callback or (lambda x: None)
    cached = g.pafs.get(ytid)

    if not force and cached and cached.expiry > time.time():
        dbg("get pafy cache hit for %s", cached.title)
        cached.fresh = False
        return cached

    else:

        try:
            p = None#pafy.new(ytid, callback=callback_fn)

        except IOError as e:

            if "pafy" in str(e):
                dbg(c.p + "retrying failed pafy get: " + ytid + c.w)
                p = None#pafy.new(ytid, callback=callback)

            else:
                raise

        g.pafs[ytid] = p
        p.fresh = True
        thread = "preload: " if not callback else ""
        dbg("%s%sgot new pafy object: %s%s" % (c.y, thread, p.title[:26], c.w))
        dbg("%s%sgot new pafy object: %s%s" % (c.y, thread, p.videoid, c.w))
        return p


def getxy():
    """
    Get terminal size, terminal width and max-results.

    :rtype: :class:`XYTuple`
    """
    # Import here to avoid circular dependency
    from . import config
    if g.detectable_size:
        x, y = terminalsize.get_terminal_size()
        max_results = y - 4 if y < 54 else 50
        max_results = 1 if y <= 5 else max_results

    else:
        x, max_results = config.CONSOLE_WIDTH.get, config.MAX_RESULTS.get
        y = max_results + 4

    return XYTuple(x, y, max_results)


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

def correct_truncate(text, max_len):
    """ Truncate a string taking into account East Asian width chars."""
    str_len, out = 0, ''

    for c in text:
        str_len += real_len(c)

        if str_len <= max_len:
            out += c

        else:
            break

    return out


def uea_pad(num, t, direction="<", notrunc=False):
    """ Right pad with spaces taking into account East Asian width chars. """
    direction = direction.strip() or "<"

    t = ' '.join(str(t).split('\n'))

    # TODO: Find better way of dealing with this?
    if num <= 0:
        return ''

    if not notrunc:
        # Truncate to max of num characters
        t = correct_truncate(t, num)

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


def yt_datetime(yt_date_time):
    """ Return a time object, locale formated date string and locale formatted time string. """
    if yt_date_time is None:
        return ['Unknown', 'Unknown', 'Unknown']
    time_obj = time.strptime(yt_date_time, "%Y-%m-%dT%H:%M:%SZ")
    locale_date = time.strftime("%x", time_obj)
    locale_time = time.strftime("%X", time_obj)
    # strip first two digits of four digit year
    short_date = re.sub(r"(\d\d\D\d\d\D)20(\d\d)$", r"\1\2", locale_date)
    return time_obj, short_date, locale_time


def yt_datetime_local(yt_date_time):
    """ Return a datetime object, locale converted and formated date string and locale converted and formatted time string. """
    datetime_obj = datetime.strptime(yt_date_time, "%Y-%m-%dT%H:%M:%SZ")
    datetime_obj = utc2local(datetime_obj)
    locale_date = datetime_obj.strftime("%x")
    locale_time = datetime_obj.strftime("%X")
    # strip first two digits of four digit year
    short_date = re.sub(r"(\d\d\D\d\d\D)20(\d\d)$", r"\1\2", locale_date)
    return datetime_obj, short_date, locale_time


def utc2local(utc):
    return utc.replace(tzinfo=timezone.utc).astimezone(tz=None)


def parse_multi(choice, end=None):
    """
    Handle ranges like 5-9, 9-5, 5- and -5 with optional repetitions number [n]

    eg. 2-4[2] is the same as 2 3 4 2 3 4 and 3[4] is 3 3 3 3

    Return list of ints.

    """
    end = end or str(len(g.model))
    pattern = r'(?<![-\d\[\]])(\d+-\d+|-\d+|\d+-|\d+)(?:\[(\d+)\])?(?![-\d\[\]])'
    items = re.findall(pattern, choice)
    alltracks = []

    for x, nreps in items:
        # nreps is in the inclusive range [1,100]
        nreps = min(int(nreps), 100) if nreps else 1
        for _ in range(nreps):

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


def is_known_player(player):
    """ Return true if the set player is known. """
    for allowed_player in g.playerargs_defaults:
        regex = r'(?:\b%s($|\.[a-zA-Z0-9]+$))' % re.escape(allowed_player)
        match = re.search(regex, player)

        if mswin:
            match = re.search(regex, player, re.IGNORECASE)

        if match:
            return allowed_player

    return None


def load_player_info(player):
    if "mpv" in player:
        g.mpv_version = _get_mpv_version(player)
        g.mpv_options = subprocess.check_output(
                [player, "--list-options"]).decode()

        if not mswin:
            if "--input-unix-socket" in g.mpv_options:
                g.mpv_usesock = "--input-unix-socket"
                dbg(c.g + "mpv supports --input-unix-socket" + c.w)
            elif "--input-ipc-server" in g.mpv_options:
                g.mpv_usesock = "--input-ipc-server"
                dbg(c.g + "mpv supports --input-ipc-server" + c.w)

    elif "mplayer" in player:
        g.mplayer_version = _get_mplayer_version(player)


def fetch_songs(text, title="Unknown"):
    return description_parser.parse(text, title)


def number_string_to_list(text):
    """ Parses comma separated lists """
    text = [x.strip() for x in text.split(",")]
    vals = []
    for line in text:
        k = line
        if "-" in line:
            separated = [int(x.strip()) for x in k.split("-")]
            for number in list(range(separated[0]-1, separated[1])):
                vals.append(number)
        else:
            vals.append(k)

    return [int(x) - 1 for x in vals]


def _get_mpv_version(exename):
    """ Get version of mpv as 3-tuple. """
    o = subprocess.check_output([exename, "--version"]).decode()
    re_ver = re.compile(r"mpv (\d+)\.(\d+)\.(\d+)")

    for line in o.split("\n"):
        m = re_ver.match(line)

        if m:
            v = tuple(map(int, m.groups()))
            dbg("%s version %s.%s.%s detected", exename, *v)
            return v

    dbg("%sFailed to detect mpv version%s", c.r, c.w)
    return -1, 0, 0


def _get_mplayer_version(exename):
    o = subprocess.check_output([exename]).decode()
    m = re.search('MPlayer SVN[\s-]r([0-9]+)', o, re.MULTILINE|re.IGNORECASE)

    ver = 0
    if m:
        ver = int(m.groups()[0])
    else:
        m = re.search('MPlayer ([0-9])+.([0-9]+)', o, re.MULTILINE)
        if m:
            ver = tuple(int(i) for i in m.groups())

        else:
            dbg("%sFailed to detect mplayer version%s", c.r, c.w)

    return ver


def _get_metadata(song_title):
    ''' Get metadata from a song title '''
    t = re.sub("[\(\[].*?[\)\]]", "", song_title.lower())
    t = t.split('-')

    if len(t) != 2:  # If len is not 2, no way of properly knowing title for sure
        t = t[0]
        t = t.split(':')
        if len(t) != 2:  # Ugly, but to be safe in case all these chars exist, Will improve
            t = t[0]
            t = t.split('|')
            if len(t) != 2:
                return None

    t[0] = re.sub("(ft |ft.|feat |feat.).*.", "", t[0])
    t[1] = re.sub("(ft |ft.|feat |feat.).*.", "", t[1])

    t[0] = t[0].strip()
    t[1] = t[1].strip()

    metadata = _get_metadata_from_lastfm(t[0], t[1])

    if metadata is not None:
        return metadata

    metadata = _get_metadata_from_lastfm(t[1], t[0])
    return metadata


def _get_metadata_from_lastfm(artist, track):
    ''' Try to get metadata with a given artist and track '''
    url = 'https://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=12dec50313f885d407cf8132697b8712&'
    url += urllib.parse.urlencode({"artist":  artist}) + '&'
    url += urllib.parse.urlencode({"track":  track}) + '&'
    url += '&format=json'

    try:
        resp = urllib.request.urlopen(url)
        metadata = dict()
        # Prior to Python 3.6, json.loads cannot take a bytes object
        data = json.loads(resp.read().decode('utf-8'))
        metadata['track_title'] = data['track']['name']
        metadata['artist'] = data['track']['artist']['name']
        metadata['album'] = data['track']['album']['title']
        metadata['album_art_url'] = data['track']['album']['image'][-1]['#text']
    except (KeyError, IndexError):
        return None
    except (urllib.error.HTTPError, urllib.error.URLError):
        return None
    return metadata


def assign_player(player):
    module_name = player

    if '/' in module_name:
        module_name = module_name.split('/')[-1]
    if module_name.endswith('.com') or module_name.endswith('.exe'):
        module_name = module_name.split('.')[0]

    try:
        module = import_module('mps_youtube.players.{0}'.format(module_name))
        pl = getattr(module, module_name)
        g.PLAYER_OBJ = pl(player)

    except ImportError:
        from mps_youtube.players import GenericPlayer
        g.PLAYER_OBJ = GenericPlayer.GenericPlayer(player)


class CommandCompleter:

    COMMANDS = []

    def __init__(self):
        from . import config
        self.SET_COMMANDS = ['set ' + i.lower() for i in config]

    def complete_command(self, text, state):
        if text.startswith('set'):
            results = [x for x in self.SET_COMMANDS if x.startswith(text)] + [None]
        else:
            results = [x for x in self.COMMANDS if x.startswith(text)] + [None]
        return results[state]
    def add_cmd(self, val):
        if(not val in self.COMMANDS):
            self.COMMANDS.append(val)

def parse_video_length(duration):
    '''
    Converts HH:MM:SS to a single integer .i.e. total number of seconds
    '''
    if duration:
        duration_tokens = duration.split(":")
        if len(duration_tokens) == 2:
            return int(duration_tokens[0]) * 60 + int(duration_tokens[1])
        else:
            return int(duration_tokens[0]) * 3600 + int(duration_tokens[1]) * 60 + int(duration_tokens[2])
    else:
        return 10
