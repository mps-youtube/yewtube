import abc
import abc
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
from ..player import Player

class Vlc(Player):

    def play_range(self, songlist, shuffle=False, repeat=False, override=False):
        """ Play a range of songs, exit cleanly on keyboard interrupt. """
        if shuffle:
            random.shuffle(songlist)

        n = 0
        while 0 <= n <= len(songlist)-1:
            song = songlist[n]
            g.content = self._playback_progress(n, songlist, repeat=repeat)

            if not g.command_line:
                screen.update(fill_blank=False)

            hasnext = len(songlist) > n + 1

            if hasnext:
                streams.preload(songlist[n + 1], override=override)

            if config.SET_TITLE.get:
                util.set_window_title(song.title + " - mpsyt")
            try:
                returncode = self._playsong(song, override=override)

            except KeyboardInterrupt:
                logging.info("Keyboard Interrupt")
                util.xprint(c.w + "Stopping...                          ")
                screen.reset_terminal()
                g.message = c.y + "Playback halted" + c.w
                raise KeyboardInterrupt
                break
            if config.SET_TITLE.get:
                util.set_window_title("mpsyt")

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

    def _playback_progress(self, idx, allsongs, repeat=False):
        """ Generate string to show selected tracks, indicate current track. """
        # pylint: disable=R0914
        # too many local variables
        cw = util.getxy().width
        out = "  %s%-XXs%s%s\n".replace("XX", str(cw - 9))
        out = out % (c.ul, "Title", "Time", c.w)

        multi = len(allsongs) > 1

        for n, song in enumerate(allsongs):
            length_orig = util.fmt_time(song.length)
            length = " " * (8 - len(length_orig)) + length_orig
            i = util.uea_pad(cw - 14, song.title), length, length_orig
            fmt = (c.w, "  ", c.b, i[0], c.w, c.y, i[1], c.w)

            if n == idx:
                fmt = (c.y, "> ", c.p, i[0], c.w, c.p, i[1], c.w)
                cur = i

            out += "%s%s%s%s%s %s%s%s\n" % fmt

        out += "\n" * (3 - len(allsongs))
        pos = 8 * " ", c.y, idx + 1, c.w, c.y, len(allsongs), c.w
        playing = "{}{}{}{} of {}{}{}\n\n".format(*pos) if multi else "\n\n"

        out = out if multi else content.generate_songlist_display(song=allsongs[0])

        playing = "{}{}{}{} of {}{}{}\n".format(*pos) if multi else "\n"
        out += "\n" + " " * (cw - 19) if multi else ""

        fmt = playing, c.r, cur[0].strip()[:cw - 19], c.w, c.w, cur[2], c.w
        out += "%s    %s%s%s %s[%s]%s" % fmt
        out += "    REPEAT MODE" if repeat else ""
        return out

    def _playsong(self, song, failcount=0, override=False):
        """ Play song using config.PLAYER called with args config.PLAYERARGS."""

        # pylint: disable=R0911,R0912
        # perhaps we can split these funcionalities to more methods and use less local variables

        if config.NOTIFIER.get:
            subprocess.Popen(shlex.split(config.NOTIFIER.get) + [song.title])

        # don't interrupt preloading:

        while song.ytid in g.preloading:
            screen.writestatus("fetching item..")
            time.sleep(0.1)

        try:
            streams.get(song, force=failcount, callback=screen.writestatus)

        except (IOError, URLError, HTTPError, socket.timeout) as e:
            util.dbg("--ioerror in _playsong call to streams.get %s", str(e))

            if "Youtube says" in str(e):
                g.message = util.F('cant get track') % (song.title + " " + str(e))
                return

            elif failcount < g.max_retries:
                util.dbg("--ioerror - trying next stream")
                failcount += 1
                return self._playsong(song, failcount=failcount, override=override)

            elif "pafy" in str(e):
                g.message = str(e) + " - " + song.ytid
                return

        except ValueError:
            g.message = util.F('track unresolved')
            util.dbg("----valueerror in _playsong call to streams.get")
            return

        try:
            video = ((config.SHOW_VIDEO.get and override != "audio") or
                     (override in ("fullscreen", "window", "forcevid")))
            cached = g.streams[song.ytid]

            # m4a_ok is True for all players, only m4a with mplayer is False.

            stream = streams.select(cached, q=failcount, audio=(not video), m4a_ok=True)

            # handle no audio stream available by switching to video stream and suppressing video output.

            if (not stream or failcount) and not video:
                util.dbg(c.r + "no audio, using video stream" + c.w)
                override = "a-v"
                video = True
                stream = streams.select(cached, q=failcount, audio=False, maxres=1600)

            if not stream:
                raise IOError("No streams available")

        except (HTTPError) as e:

            # Fix for invalid streams (gh-65)

            util.dbg("----htterror in _playsong call to gen_real_args %s", str(e))
            if failcount < g.max_retries:
                failcount += 1
                return self._playsong(song, failcount=failcount, override=override)
            else:
                g.message = str(e)
                return

        size = streams.get_size(song.ytid, stream['url'])
        songdata = (song.ytid, stream['ext'] + " " + stream['quality'],
                    int(size / (1024 ** 2)))
        songdata = "%s; %s; %s Mb" % songdata
        screen.writestatus(songdata)

        cmd = self._generate_real_playerargs(stream)
        returncode = self._launch_player(song, songdata, cmd)
        failed = returncode not in (0, 42, 43)

        if failed and failcount < g.max_retries:
            util.dbg(c.r + "stream failed to open" + c.w)
            util.dbg("%strying again (attempt %s)%s", c.r, (2 + failcount), c.w)
            screen.writestatus("error: retrying")
            time.sleep(1.2)
            failcount += 1
            return self._playsong(song, failcount=failcount, override=override)

        history.add(song)
        return returncode

    def _generate_real_playerargs(self, stream):
        """ Generate args for player command.Return args. """

        # pylint: disable=R0914
        # pylint: disable=R0912
        # pylint: disable=E1103
        # pylint thinks PLAYERARGS.get might be bool

        args = config.PLAYERARGS.get.strip().split()
        util.list_update("--play-and-exit", args)

        return [config.PLAYER.get] + args + [stream['url']]


    def _launch_player(self, song, songdata, cmd):
        """ Launch player application. """

        util.dbg("playing %s", song.title)
        util.dbg("calling %s", " ".join(cmd))

        # Fix UnicodeEncodeError when title has characters
        # not supported by encoding
        cmd = [util.xenc(i) for i in cmd]

        arturl = "https://i.ytimg.com/vi/%s/default.jpg" % song.ytid

        sockpath = None
        fifopath = None
        p = None

        """
        Perhaps more things can be omitted.
        """

        try:
            with open(os.devnull, "w") as devnull:
                returncode = subprocess.call(cmd, stderr=devnull)

            return returncode

        except OSError:
            g.message = util.F('no player') % config.PLAYER.get
            return None

        finally:

            if sockpath and os.path.exists(sockpath):
                os.unlink(sockpath)

            if fifopath:
                os.unlink(fifopath)

            if g.mprisctl:
                g.mprisctl.send(('stop', True))

            if p and p.poll() is None:
                p.terminate()
