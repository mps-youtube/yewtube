import os
import sys
import random
import tempfile
import subprocess
import logging
import json
import re
import socket
import math
import time
import shlex
from urllib.error import HTTPError, URLError

from .. import g, screen, c, streams, history, content, paths, config, util


mswin = os.name == "nt"
not_utf8_environment = mswin or "UTF-8" not in sys.stdout.encoding


from ..player import Player

class mpv(Player):
    def _generate_real_playerargs(self, song, override, stream, isvideo, softrepeat):
        """ Generate args for player command.

        Return args.

        """


        args = config.PLAYERARGS.get.strip().split()

        known_player = util.is_known_player(config.PLAYER.get)
        if known_player:
            pd = g.playerargs_defaults[known_player]
            args.extend((pd["title"], song.title))

            if pd['geo'] not in args:
                geometry = config.WINDOW_SIZE.get or ""

                if config.WINDOW_POS.get:
                    wp = config.WINDOW_POS.get
                    xx = "+1" if "left" in wp else "-1"
                    yy = "+1" if "top" in wp else "-1"
                    geometry += xx + yy

                if geometry:
                    args.extend((pd['geo'], geometry))

            # handle no audio stream available
            if override == "a-v":
                util.list_update(pd["novid"], args)

            elif ((config.FULLSCREEN.get and override != "window")
                    or override == "fullscreen"):
                util.list_update(pd["fs"], args)

            # prevent ffmpeg issue (https://github.com/mpv-player/mpv/issues/579)
            if not isvideo and stream['ext'] == "m4a":
                util.dbg("%susing ignidx flag%s")
                util.list_update(pd["ignidx"], args)

            if "--ytdl" in g.mpv_options:
                util.list_update("--no-ytdl", args)

            msglevel = pd["msglevel"]["<0.4"]

            #  undetected (negative) version number assumed up-to-date
            if g.mpv_version[0:2] < (0, 0) or g.mpv_version[0:2] >= (0, 4):
                msglevel = pd["msglevel"][">=0.4"]

            if not g.debug_mode:
                if g.mpv_usesock:
                    util.list_update("--really-quiet", args)
                else:
                    util.list_update("--really-quiet", args, remove=True)
                    util.list_update(msglevel, args)

            if g.volume:
                util.list_update("--volume=" + str(g.volume), args)
            if softrepeat:
                util.list_update("--loop-file", args)

        return [config.PLAYER.get] + args + [stream['url']]

    def clean_up(self):
        if self.input_file:
            os.unlink(self.input_file)

    def launch_player(self, cmd):
        self.input_file = _get_input_file()
        cmd.append('--input-conf=' + self.input_file)
        self.sockpath = tempfile.mktemp('.sock', 'mpsyt-mpv')

        with open(os.devnull, "w") as devnull:
            self.p = subprocess.Popen(cmd, shell=False, stderr=devnull)
            #TODO
            #_player_status(self.p, songdata + "; ", song.length, mpv=True,
            #              sockpath=self.sockpath)
            returncode = self.p.wait()

    def _help(self, short=True):
        """ Mplayer help.  """
        # pylint: disable=W1402

        volume = "[{0}9{1}] volume [{0}0{1}]      [{0}CTRL-C{1}] return"
        seek = "[{0}\u2190{1}] seek [{0}\u2192{1}]"
        pause = "[{0}\u2193{1}] SEEK [{0}\u2191{1}]       [{0}space{1}] pause"

        if not_utf8_environment:
            seek = "[{0}<-{1}] seek [{0}->{1}]"
            pause = "[{0}DN{1}] SEEK [{0}UP{1}]       [{0}space{1}] pause"

        single = "[{0}q{1}] next"
        next_prev = "[{0}>{1}] next/prev [{0}<{1}]"
        # ret = "[{0}q{1}] %s" % ("return" if short else "next track")
        ret = single if short and config.AUTOPLAY.get else ""
        ret = next_prev if not short else ret
        fmt = "    %-20s       %-20s"
        lines = fmt % (seek, volume) + "\n" + fmt % (pause, ret)
        return lines.format(c.g, c.w)

def _get_input_file():
    """ Check for existence of custom input file.

    Return file name of temp input file with mpsyt mappings included
    """
    confpath = conf = ''

    if "mpv" in config.PLAYER.get:
        confpath = os.path.join(paths.get_config_dir(), "mpv-input.conf")

    elif "mplayer" in config.PLAYER.get:
        confpath = os.path.join(paths.get_config_dir(), "mplayer-input.conf")

    if os.path.isfile(confpath):
        util.dbg("using %s for input key file", confpath)

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
