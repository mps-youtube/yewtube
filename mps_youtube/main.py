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

__version__ = "0.2.6-dev"
__notes__ = "development version"
__author__ = "np1"
__license__ = "GPLv3"
__url__ = "http://github.com/np1/mps-youtube"

from xml.etree import ElementTree as ET
import multiprocessing
import unicodedata
import collections
import subprocess
import threading
import argparse
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
import copy
import sys
import re
import os
import pickle
from urllib.request import urlopen, build_opener
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

import pafy

from . import terminalsize, g, c, cache, streams
from .playlist import Playlist, Video
from .paths import get_config_dir
from .config import Config, known_player_set, import_config
from .util import has_exefile, get_mpv_version, dbg, list_update, get_near_name
from .util import get_mplayer_version, get_pafy
from .util import xenc, xprint, mswinfn, set_window_title, clear_screen, F
from .helptext import helptext, get_help

try:
    # pylint: disable=F0401
    import colorama
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
    import pyperclip
    has_pyperclip = True

except ImportError:
    has_pyperclip = False


mswin = os.name == "nt"
not_utf8_environment = mswin or "UTF-8" not in sys.stdout.encoding

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


def get_content_length(url, preloading=False):
    """ Return content length of a url. """
    prefix = "preload: " if preloading else ""
    dbg(c.y + prefix + "getting content-length header" + c.w)
    response = urlopen(url)
    headers = response.headers
    cl = headers['content-length']
    return int(cl)


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


def process_cl_args():
    """ Process command line arguments. """

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('commands', nargs='*')
    parser.add_argument('--help', '-h', action='store_true')
    parser.add_argument('--version', '-v', action='store_true')
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--logging', '-l', action='store_true')
    parser.add_argument('--no-autosize', action='store_true')
    parser.add_argument('--no-preload', action='store_true')
    args = parser.parse_args()

    if args.version:
        xprint(get_version_info())
        xprint("")
        sys.exit()

    elif args.help:
        for x in helptext():
            xprint(x[2])
        sys.exit()

    if args.debug or os.environ.get("mpsytdebug") == "1":
        xprint(get_version_info())
        g.debug_mode = True
        g.no_clear_screen = True
        logfile = os.path.join(tempfile.gettempdir(), "mpsyt.log")
        logging.basicConfig(level=logging.DEBUG, filename=logfile)
        logging.getLogger("pafy").setLevel(logging.DEBUG)

    elif args.logging or os.environ.get("mpsytlog") == "1":
        logfile = os.path.join(tempfile.gettempdir(), "mpsyt.log")
        logging.basicConfig(level=logging.DEBUG, filename=logfile)
        logging.getLogger("pafy").setLevel(logging.DEBUG)

    if args.no_autosize:
        g.detectable_size = False

    g.command_line = "playurl" in args.commands or "dlurl" in args.commands
    if g.command_line:
        g.no_clear_screen = True

    if args.no_preload:
        g.preload_disabled = True

    g.argument_commands = args.commands


def init():
    """ Initial setup. """

    if not os.path.exists(g.CFFILE):

        if has_exefile(mpv):
            Config.PLAYER.set(mpv)

        elif has_exefile(mplayer):
            Config.PLAYER.set(mplayer)

        Config.save()

    else:
        import_config()

    init_readline()
    cache.init()
    init_transcode()

    # set player to mpv or mplayer if found, otherwise unset
    suffix = ".exe" if mswin else ""
    mplayer, mpv = "mplayer" + suffix, "mpv" + suffix

    # ensure encoder is not set beyond range of available presets
    if Config.ENCODER.get >= len(g.encoders):
        Config.ENCODER.set("0")

    # check mpv/mplayer version
    if "mpv" in Config.PLAYER.get and has_exefile(Config.PLAYER.get):
        g.mpv_version = get_mpv_version(Config.PLAYER.get)
        if not mswin:
            options = subprocess.check_output(
                [Config.PLAYER.get, "--list-options"]).decode()

            if "--input-unix-socket" in options:
                g.mpv_usesock = True
                dbg(c.g + "mpv supports --input-unix-socket" + c.w)

    elif "mplayer" in Config.PLAYER.get and has_exefile(Config.PLAYER.get):
        g.mplayer_version = get_mplayer_version(Config.PLAYER.get)

    # setup colorama
    if has_colorama and mswin:
        colorama.init()

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

    process_cl_args()


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


def init_readline():
    """ Enable readline for input history. """
    if g.command_line:
        return

    if has_readline:
        g.READLINE_FILE = os.path.join(get_config_dir(), "input_history")

        if os.path.exists(g.READLINE_FILE):
            readline.read_history_file(g.READLINE_FILE)
            dbg(c.g + "Read history file" + c.w)


def showconfig(_):
    """ Dump config data. """
    width = getxy().width
    width -= 30
    s = "  %s%-17s%s : %s\n"
    out = "  %s%-17s   %s%s%s\n" % (c.ul, "Key", "Value", " " * width, c.w)

    for setting in Config:
        val = Config[setting]

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


def setconfig(key, val):
    """ Set configuration variable. """
    key = key.replace("-", "_")
    if key.upper() == "ALL" and val.upper() == "DEFAULT":

        for ci in Config:
            Config[ci].value = Config[ci].default

        Config.save()
        message = "Default configuration reinstated"

    elif not key.upper() in Config:
        message = "Unknown config item: %s%s%s" % (c.r, key, c.w)

    elif val.upper() == "DEFAULT":
        att = Config[key.upper()]
        att.value = att.default
        message = "%s%s%s set to %s%s%s (default)"
        dispval = att.display or "None"
        message = message % (c.y, key, c.w, c.y, dispval, c.w)
        Config.save()

    else:
        # Config.save() will be called by Config.set() method
        message = Config[key.upper()].set(val)

    showconfig(1)
    g.message = message


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
    qs = copy.copy(qs)
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

    wdata = call_gdata('videos', qs)

    items_vidinfo = wdata.get('items', [])
    # enhance search results by adding information from videos API response
    for searchresult, vidinfoitem in zip(items, items_vidinfo):
        searchresult.update(vidinfoitem)

    # populate list of video objects
    songs = []
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
    clear_screen()

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


def uea_pad(num, t, direction="<", notrunc=False):
    """ Right pad with spaces taking into account East Asian width chars. """
    direction = direction.strip() or "<"

    t = ' '.join(t.split('\n'))
    
    # TODO: Find better way of dealing with this?
    if num <= 0:
        return ''

    if not notrunc:
        # Truncate to max of num characters
        t = t[:num]

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
                              '>' if (g.more_pages is not None or
                                       (page < page_count)) else ']')
    return None


def generate_songlist_display(song=False, zeromsg=None, frmat="search"):
    """ Generate list of choices from a song list."""
    # pylint: disable=R0914
    if g.browse_mode == "ytpl":
        return generate_playlist_display()

    max_results = getxy().max_results

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

    for n, x in enumerate(songs[:max_results]):
        col = (c.r if n % 2 == 0 else c.p) if not song else c.b
        details = {'title': x.title, "length": fmt_time(x.length)}
        details = copy.copy(g.meta[x.ytid]) if have_meta else details
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
        xprint(text, end='\r')


def generate_real_playerargs(song, override, failcount):
    """ Generate args for player command.

    Return args and songdata status.

    """
    # pylint: disable=R0914
    # pylint: disable=R0912
    video = Config.SHOW_VIDEO.get
    video = True if override in ("fullscreen", "window", "forcevid") else video
    video = False if override == "audio" else video
    m4a = "mplayer" not in Config.PLAYER.get
    q, audio, cached = failcount, not video, g.streams[song.ytid]
    stream = streams.select(cached, q=q, audio=audio, m4a_ok=m4a)

    # handle no audio stream available, or m4a with mplayer
    # by switching to video stream and suppressing video output.
    if not stream and not video or failcount and not video:
        dbg(c.r + "no audio or mplayer m4a, using video stream" + c.w)
        override = "a-v"
        video = True
        stream = streams.select(cached, q=q, audio=False, maxres=1600)

    if not stream and video:
        raise IOError("No streams available")

    if "uiressl=yes" in stream['url'] and "mplayer" in Config.PLAYER.get:
        ver = g.mplayer_version
        # Mplayer too old to support https
        if not (ver > (1,1) if isinstance(ver, tuple) else ver >= 37294):
            raise IOError("%s : Sorry mplayer doesn't support this stream. "
                          "Use mpv or update mplayer to a newer version" % song.title)

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
        subprocess.Popen(shlex.split(Config.NOTIFIER.get) + [song.title])

    # don't interrupt preloading:
    while song.ytid in g.preloading:
        writestatus("fetching item..")
        time.sleep(0.1)

    try:
        streams.get(song, force=failcount, callback=writestatus)

    except (IOError, URLError, HTTPError, socket.timeout) as e:
        dbg("--ioerror in playsong call to streams.get %s", str(e))

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
        dbg("----valueerror in playsong call to streams.get")
        return

    try:
        cmd, songdata = generate_real_playerargs(song, override, failcount)

    except (HTTPError) as e:

        # Fix for invalid streams (gh-65)
        dbg("----htterror in playsong call to gen_real_args %s", str(e))
        if failcount < g.max_retries:
            failcount += 1
            return playsong(song, failcount=failcount, override=override)
        else:
            g.message = str(e)
            return

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
    wdata = call_gdata('search', qs)
    songs = get_tracks_from_json(wdata)

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
        if Config.SEARCH_MUSIC:
            failmsg = """User %s not found or has no videos in the Music category.
Use 'set search_music False' to show results not in the Music category.""" % termuser[1]
        else:
            failmsg = "User %s not found or has no videos."  % termuser[1]
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

        pldata = call_gdata('search', qs)
        id_list = [i.get('id', {}).get('playlistId')
                    for i in pldata.get('items', ())]
        # page info
        get_page_info_from_json(pldata, len(id_list))

    qs = {'part': 'contentDetails,snippet',
          'maxResults': 50}

    if is_user:
        if page:
            qs['pageToken'] = token(page)
        qs['channelId'] = channel_id
    else:
        qs['id'] = ','.join(id_list)

    pldata = call_gdata('playlists', qs)
    playlists = get_pl_from_json(pldata)

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

    jsdata = call_gdata('commentThreads', qs)

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

    if ext:
        extension = ext

    else:
        stream = streams.select(streams.get(song),
                audio=av == "audio", m4a_ok=True)
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


def external_download(song, filename, url):
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
    cmd_list = list_string_sub("%i", song.ytid, cmd_list)
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
        stream = streams.select(streams.get(song), audio=audio, m4a_ok=True)
        url = stream['url']

    # if an external download command is set, use it
    if Config.DOWNLOAD_COMMAND.get:
        title = c.y + os.path.splitext(os.path.basename(filename))[0] + c.w
        xprint("Downloading %s using custom command" % title)
        external_download(song, filename, url)
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




def play_pl(name):
    """ Play a playlist by name. """
    if name.isdigit():
        name = int(name)
        name = sorted(g.userpl)[name - 1]

    saved = g.userpl.get(name)

    if not saved:
        name = get_near_name(name, g.userpl)
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
            name = get_near_name(name, g.userpl)
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
            g.result_count = len(g.model.songs)
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
        g.result_count = len(g.model.songs)
        g.content = generate_songlist_display()


def down_plist(dltype, parturl):
    """ Download YouTube playlist. """

    plist(parturl, page=0, splash=True, dumps=True)
    title = g.pafy_pls[parturl]['title']
    subdir = mswinfn(title.replace("/", "-"))
    down_many(dltype, "1-", subdir=subdir)
    msg = g.message
    plist(parturl, page=0, splash=True)
    g.message = msg


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
        nofs = "-w" in pre + post
        forcevid = "-v" in pre + post

        if ((novid and fs) or (novid and nofs) or (nofs and fs)
           or (novid and forcevid)):
            raise IOError("Conflicting override options specified")

        override = False
        override = "audio" if novid else override
        override = "fullscreen" if fs else override
        override = "window" if nofs else override

        if (not fs) and (not nofs):
            override = "forcevid" if forcevid else override

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
    video = True if override in ("fullscreen", "window", "forcevid") else video
    video = False if override == "audio" else video

    try:
        m4a = "mplayer" not in Config.PLAYER.get
        stream = streams.select(streams.get(song), audio=not video, m4a_ok=m4a)

        if not stream and not video:
            # preload video stream, no audio available
            stream = streams.select(streams.get(song),
                    g.streams[ytid], audio=False)

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

    g.content = get_help(choice)


def quits(showlogo=True):
    """ Exit the program. """
    if has_readline:
        readline.write_history_file(g.READLINE_FILE)
        dbg("Saved history file")

    cache.save()

    clear_screen()
    msg = logo(c.r, version=__version__) if showlogo else ""
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
    streamlist = [x for x in p.allstreams]

    if mediatype == "audio":
        streamlist = [x for x in p.audiostreams]

    l = len(streamlist)
    for n, stream in enumerate(streamlist):
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

    if has_pyperclip:

        try:
            pyperclip.copy(link)
            g.message = c.y + link + c.w + " copied"
            g.content = generate_songlist_display()

        except Exception as e:
            xprint(link)
            xprint("Error - couldn't copy to clipboard.")
            xprint(e.__doc__)
            xprint("")
            input("Press Enter to continue.")
            g.content = generate_songlist_display()

    else:
        g.message = "pyperclip module must be installed for clipboard support\n"
        g.message += "see https://pypi.python.org/pypi/pyperclip/"
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
        streams.get(item)
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
    g.result_count = len(g.ytpl['items'])
    g.more_pages = max_results < len(g.ytpl['items'])
    g.model.songs = songs[:max_results] if not dumps else songs[::]
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


def _do_query(url, query, err='query failed', report=False):
    """ Perform http request using mpsyt user agent header.

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
    clear_screen()
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

            except GdataError as e:
                g.message = F('no data') % e
                g.content = g.content

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

    arg_inp = ' '.join(g.argument_commands)

    # input types
    word = r'[^\W\d][-\w\s]{,100}'
    rs = r'(?:repeat\s*|shuffle\s*|-a\s*|-v\s*|-f\s*|-w\s*)'
    pl = r'\S*((?:RD|PL)[-_0-9a-zA-Z]+)$\S*'
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
