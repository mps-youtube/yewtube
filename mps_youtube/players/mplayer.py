import os
import re
import subprocess
import sys
import tempfile
import typing as T

from .. import c, config, g, paths, screen, util
from ..player import CmdPlayer
from ..util import not_utf8_environment

mswin = os.name == "nt"


class mplayer(CmdPlayer):
    def __init__(self, player):
        self.player = player
        self.mplayer_version = _get_mplayer_version(player)

    def _generate_real_playerargs(self):
        """ Generate args for player command.

        Return args.

        """

        if "uiressl=yes" in self.stream['url']:
            ver = self.mplayer_version
            # Mplayer too old to support https
            if not (ver > (1, 1) if isinstance(ver, tuple) else ver >= 37294):
                raise IOError("%s : Sorry mplayer doesn't support this stream. "
                              "Use mpv or update mplayer to a newer version" % self.song.title)

        args = config.PLAYERARGS.get.strip().split()

        pd = g.playerargs_defaults['mplayer']
        args.extend((pd["title"], '"{0}"'.format(self.song.title)))

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
        if self.override == "a-v":
            util.list_update(pd["novid"], args)

        elif ((config.FULLSCREEN.get and self.override != "window")
                or self.override == "fullscreen"):
            util.list_update(pd["fs"], args)

        # prevent ffmpeg issue (https://github.com/mpv-player/mpv/issues/579)
        if not self.video and self.stream['ext'] == "m4a":
            util.dbg("%susing ignidx flag%s")
            util.list_update(pd["ignidx"], args)

        if g.volume:
            util.list_update("-volume", args)
            util.list_update(str(g.volume), args)
        util.list_update("-really-quiet", args, remove=True)
        util.list_update("-noquiet", args)
        util.list_update("-prefer-ipv4", args)
        util.list_update("-cache", args)
        util.list_update("4096", args)

        return [self.player] + args + [self.stream['url']]

    def clean_up(self):
        if self.fifopath:
            os.unlink(self.fifopath)

    def launch_player(self, cmd):
        self.input_file = _get_input_file()
        self.sockpath = None
        self.fifopath = None

        cmd.append('-input')

        if mswin:
            # Mplayer does not recognize path starting with drive letter,
            # or with backslashes as a delimiter.
            self.input_file = self.input_file[2:].replace('\\', '/')

        cmd.append('conf=' + self.input_file)

        if g.mprisctl:
            self.fifopath = tempfile.mktemp('.fifo', 'mpsyt-mplayer')
            os.mkfifo(self.fifopath)
            cmd.extend(['-input', 'file=' + self.fifopath])
            g.mprisctl.send(('mplayer-fifo', self.fifopath))

        self.p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, bufsize=0)
        self._player_status(self.songdata + "; ", self.song.length)
        returncode = self.p.wait()
        print(returncode)

        if returncode == 42:
            self.previous()

        elif returncode == 43:
            self.stop()

        else:
            self.next()

    def _player_status(self, prefix, songlength=0):
        """ Capture time progress from player output. Write status line. """
        # pylint: disable=R0914, R0912
        re_player = re.compile(r"A:\s*(?P<elapsed_s>\d+)\.\d\s*")
        re_volume = re.compile(r"Volume:\s*(?P<volume>\d+)\s*%")
        last_displayed_line = None
        buff = ''
        volume_level = None
        last_pos = None

        elapsed_s = 0
        while self.p.poll() is None:
            stdstream = self.p.stdout
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


def _get_mplayer_version(exename: str) -> T.Union[int, T.Tuple[int, ...]]:
    """get mplayer version.

    Args:
        exename: mplayer executable name.

    Returns:
       single integer value or tuple of mplayer version. Return `0` if failed

    Raises:
        OSError: if `exename` is invalid
        FileNotFoundError: if no mplayer found
        PermissionError: if user dont have permission to run `exename`
        TypeError: if `exename` return invalid type
    """
    try:
        o = subprocess.check_output([exename]).decode()
    except FileNotFoundError:
        raise

    m = re.search(r"MPlayer \S*?SVN[\s-]r([0-9]+)", o, re.MULTILINE | re.IGNORECASE)

    ver = 0
    if m:
        ver = int(m.groups()[0])
    else:
        m = re.search('MPlayer ([0-9])+.([0-9]+)', o, re.MULTILINE)
        if m:
            ver = tuple(int(i) for i in m.groups())

        else:
            util.dbg("%sFailed to detect mplayer version%s", c.r, c.w)

    return ver
