import os
import re
import sys
import logging
import tempfile
import argparse
import platform
import multiprocessing

import pafy

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

from . import cache, g, __version__, __notes__, screen, c, paths, config
from .util import has_exefile, dbg, xprint, load_player_info
from .helptext import helptext

mswin = os.name == "nt"


def init():
    """ Initial setup. """

    _process_cl_args()

    # set player to mpv or mplayer if found, otherwise unset
    suffix = ".exe" if mswin else ""
    mplayer, mpv = "mplayer" + suffix, "mpv" + suffix

    if not os.path.exists(g.CFFILE):

        if has_exefile(mpv):
            config.PLAYER.set(mpv)

        elif has_exefile(mplayer):
            config.PLAYER.set(mplayer)

        config.save()

    else:
        config.load()

    _init_readline()
    cache.load()
    _init_transcode()

    # ensure encoder is not set beyond range of available presets
    if config.ENCODER.get >= len(g.encoders):
        config.ENCODER.set("0")

    # check mpv/mplayer version
    if has_exefile(config.PLAYER.get):
        load_player_info(config.PLAYER.get)

    # setup colorama
    if has_colorama and mswin:
        # Colorama converts ansi escape codes to Windows system calls
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
    pafy.set_api_key(config.API_KEY.get)


def _init_transcode():
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


def _init_readline():
    """ Enable readline for input history. """
    if g.command_line:
        return

    if has_readline:
        g.READLINE_FILE = os.path.join(paths.get_config_dir(), "input_history")

        if os.path.exists(g.READLINE_FILE):
            readline.read_history_file(g.READLINE_FILE)
            dbg(c.g + "Read history file" + c.w)


def _process_cl_args():
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
        screen.msgexit(_get_version_info())

    elif args.help:
        screen.msgexit('\n'.join(i[2] for i in helptext()))

    if args.debug or os.environ.get("mpsytdebug") == "1":
        xprint(_get_version_info())
        g.debug_mode = True
        g.no_clear_screen = True

    if args.logging or os.environ.get("mpsytlog") == "1" or g.debug_mode:
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


def _get_version_info():
    """ Return version and platform info. """
    pafy_version = pafy.__version__
    youtube_dl_version = None
    if tuple(map(int, pafy_version.split('.'))) >= (0, 5, 0):
        pafy_version += " (" + pafy.backend + " backend)"
        if pafy.backend == "youtube-dl":
            import youtube_dl
            youtube_dl_version = youtube_dl.version.__version__

    out = "mpsyt version      : " + __version__
    out += "\n   notes           : " + __notes__
    out += "\npafy version       : " + pafy_version
    if youtube_dl_version:
        out += "\nyoutube-dl version : " + youtube_dl_version
    out += "\nPython version     : " + sys.version
    out += "\nProcessor          : " + platform.processor()
    out += "\nMachine type       : " + platform.machine()
    out += "\nArchitecture       : %s, %s" % platform.architecture()
    out += "\nPlatform           : " + platform.platform()
    out += "\nsys.stdout.enc     : " + sys.stdout.encoding
    out += "\ndefault enc        : " + sys.getdefaultencoding()
    out += "\nConfig dir         : " + paths.get_config_dir()

    for env in "TERM SHELL LANG LANGUAGE".split():
        value = os.environ.get(env)
        out += "\nenv:%-15s: %s" % (env, value) if value else ""

    return out
