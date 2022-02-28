import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import time

from .. import c, config, g, paths, screen, util
from ..player import CmdPlayer
from ..util import not_utf8_environment

mswin = os.name == "nt"


class mpv(CmdPlayer):
    def __init__(self, player):
        self.player = player
        self.mpv_version = _get_mpv_version(player)
        self.mpv_options = subprocess.check_output(
                [player, "--list-options"]).decode()

        self.mpv_usesock = ""
        if not mswin:
            if "--input-unix-socket" in self.mpv_options:
                self.mpv_usesock = "--input-unix-socket"
                util.dbg(c.g + "mpv supports --input-unix-socket" + c.w)
            elif "--input-ipc-server" in self.mpv_options:
                self.mpv_usesock = "--input-ipc-server"
                util.dbg(c.g + "mpv supports --input-ipc-server" + c.w)

    def _generate_real_playerargs(self):
        """ Generate args for player command.

        Return args.

        """

        args = config.PLAYERARGS.get.strip().split()

        pd = g.playerargs_defaults['mpv']
        # Use new mpv syntax
        # https://github.com/mps-youtube/mps-youtube/issues/1052
        completetitle = '='.join((pd["title"], '"{0}"'.format(self.song.title)))
        util.list_update(completetitle, args)

        if pd['geo'] not in args:
            geometry = config.WINDOW_SIZE.get or ""

            if config.WINDOW_POS.get:
                wp = config.WINDOW_POS.get
                xx = "+1" if "left" in wp else "-1"
                yy = "+1" if "top" in wp else "-1"
                geometry += xx + yy

            if geometry:
                # Use new mpv syntax
                # See: https://github.com/mps-youtube/mps-youtube/issues/1052
                newgeometry = '='.join((pd['geo'], geometry))
                util.list_update(newgeometry, args)

        # handle no audio stream available
        if self.override == "a-v":
            util.list_update(pd["novid"], args)

        elif ((config.FULLSCREEN.get and self.override != "window")
                or self.override == "fullscreen"):
            util.list_update(pd["fs"], args)

        # prevent ffmpeg issue (https://github.com/mpv-player/mpv/issues/579)
        if not self.video and self.stream['ext'] == "m4a":
            util.dbg("%susing ignidx flag%s")
            util.list_update(pd["ignidx"], args)

        if "--ytdl" in self.mpv_options:
            util.list_update("--no-ytdl", args)

        msglevel = pd["msglevel"]["<0.4"]

        #  undetected (negative) version number assumed up-to-date
        if self.mpv_version[0:2] < (0, 0) or self.mpv_version[0:2] >= (0, 4):
            msglevel = pd["msglevel"][">=0.4"]

        if not g.debug_mode:
            if self.mpv_usesock:
                util.list_update("--really-quiet", args)
            else:
                util.list_update("--really-quiet", args, remove=True)
                util.list_update(msglevel, args)

        if g.volume:
            util.list_update("--volume=" + str(g.volume), args)
        if self.softrepeat:
            util.list_update("--loop-file", args)

        return [self.player] + args + [self.stream['url']]

    def clean_up(self):
        if self.input_file:
            os.unlink(self.input_file)

        if self.sockpath and os.path.exists(self.sockpath):
            os.unlink(self.sockpath)

        if self.fifopath and os.path.exists(self.fifopath):
            os.unlink(self.fifopath)

    def launch_player(self, cmd):
        self.input_file = _get_input_file()
        cmd.append('--input-conf=' + self.input_file)
        self.sockpath = None
        self.fifopath = None

        if self.mpv_usesock:
            self.sockpath = tempfile.mktemp('.sock', 'mpsyt-mpv')
            cmd.append(self.mpv_usesock + '=' + self.sockpath)

            with open(os.devnull, "w") as devnull:
                self.p = subprocess.Popen(cmd, shell=False, stderr=devnull)

            if g.mprisctl:
                g.mprisctl.send(('socket', self.sockpath))
        else:
            if g.mprisctl:
                self.fifopath = tempfile.mktemp('.fifo', 'mpsyt-mpv')
                os.mkfifo(self.fifopath)
                cmd.append('--input-file=' + self.fifopath)
                g.mprisctl.send(('mpv-fifo', self.fifopath))

            self.p = subprocess.Popen(cmd, shell=False, stderr=subprocess.PIPE,
                                      bufsize=0)

        self._player_status(self.songdata + "; ", self.song.length)
        returncode = self.p.wait()

        if returncode == 42:
            self.previous()

        elif returncode == 43:
            self.stop()

        else:
            self.next()

    def _player_status(self, prefix, songlength=0):
        """ Capture time progress from player output. Write status line. """
        # pylint: disable=R0914, R0912
        re_player = re.compile(r".{,15}AV?:\s*(\d\d):(\d\d):(\d\d)")
        re_volume = re.compile(r"Volume:\s*(?P<volume>\d+)\s*%")
        last_displayed_line = None
        buff = ''
        volume_level = None
        last_pos = None

        if self.sockpath:
            s = socket.socket(socket.AF_UNIX)

            tries = 0
            while tries < 10 and self.p.poll() is None:
                time.sleep(.5)
                try:
                    s.connect(self.sockpath)
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
                        if resp.get('data') is not None:
                            elapsed_s = int(resp['data'])

                    elif resp.get('event') == 'property-change' and resp['id'] == 2:
                        volume_level = int(resp['data'])

                    if(volume_level and volume_level != g.volume):
                        g.volume = volume_level
                    if elapsed_s:
                        self.make_status_line(elapsed_s, prefix, songlength,
                                              volume=volume_level)

            except socket.error:
                pass

        else:
            elapsed_s = 0

            while self.p.poll() is None:
                stdstream = self.p.stderr
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
                                elapsed_s = int(match_object.group('elapsed_s')
                                                or '0')

                            except ValueError:
                                continue

                        if volume_level and volume_level != g.volume:
                            g.volume = volume_level
                        self.make_status_line(elapsed_s, prefix, songlength,
                                              volume=volume_level)

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

    def _help(self, short=True):
        """ Mplayer help.  """

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

    Return file name of temp input file with yewtube mappings included
    """
    confpath = conf = ''

    confpath = os.path.join(paths.get_config_dir(), "mpv-input.conf")

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


def _get_mpv_version(exename):
    """ Get version of mpv as 3-tuple. """
    o = subprocess.check_output([exename, "--version"]).decode()
    re_ver = re.compile(r"mpv (\d+)\.(\d+)\.(\d+)")

    for line in o.split("\n"):
        m = re_ver.match(line)

        if m:
            v = tuple(map(int, m.groups()))
            util.dbg("%s version %s.%s.%s detected", exename, *v)
            return v

    util.dbg("%sFailed to detect mpv version%s", c.r, c.w)
    return -1, 0, 0
