import logging
import math
import os
import random
import shlex
import socket
import subprocess
import sys
import time
from abc import ABCMeta, abstractmethod
from urllib.error import HTTPError, URLError

from . import c, config, content, g, history, screen, streams, util
from .commands import lastfm
from .util import not_utf8_environment

mswin = os.name == "nt"

class BasePlayer:
    _playbackStatus = "Paused"
    _last_displayed_line = None

    @property
    def PlaybackStatus(self):
        return self._playbackStatus

    @PlaybackStatus.setter
    def PlaybackStatus(self, value):
        self._playbackStatus = value
        if value == 'Playing':
            paused = False
        else:
            paused = True
        g.mprisctl.send(('pause', paused))

    def play(self, songlist, shuffle=False, repeat=False, override=False):
        """ Play a range of songs, exit cleanly on keyboard interrupt. """

        if config.ALWAYS_REPEAT.get:
            repeat = True

        self.songlist = songlist
        self.shuffle = shuffle
        self.repeat = repeat
        self.override = override
        if shuffle:
            random.shuffle(self.songlist)

        self.song_no = 0
        while 0 <= self.song_no <= len(self.songlist)-1:
            self.song = self.songlist[self.song_no]
            g.content = self._playback_progress(self.song_no, self.songlist,
                                                repeat=repeat)

            if not g.command_line:
                screen.update(fill_blank=False)

            hasnext = len(self.songlist) > self.song_no + 1

            if hasnext:
                streams.preload(self.songlist[self.song_no + 1],
                                override=self.override)

            if config.SET_TITLE.get:
                util.set_window_title(self.song.title + " - yewtube")

            self.softrepeat = repeat and len(self.songlist) == 1

            if g.scrobble:
                lastfm.set_now_playing(g.artist, g.scrobble_queue[self.song_no])

            try:
                self.video, self.stream, self.override = stream_details(
                                                            self.song,
                                                            override=self.override,
                                                            softrepeat=self.softrepeat)
                self._playsong()

            except KeyboardInterrupt:
                logging.info("Keyboard Interrupt")
                util.xprint(c.w + "Stopping...                          ")
                screen.reset_terminal()
                g.message = c.y + "Playback halted" + c.w
                raise KeyboardInterrupt
                break

            # skip forbidden, video removed/no longer available, etc. tracks
            except TypeError as e:
                import traceback
                traceback.print_exception(type(e), e, e.__traceback__)
                self.song_no += 1
                pass

            if config.SET_TITLE.get:
                util.set_window_title("yewtube")

            if self.song_no == -1:
                self.song_no = len(songlist) - 1 if repeat else 0
            elif self.song_no == len(self.songlist) and repeat:
                self.song_no = 0

    # To be defined by subclass based on being cmd player or library
    # When overriding next and previous don't forget to add the following
    # if g.scrobble:
    #   lastfm.scrobble_track(g.artist, g.album, g.scrobble_queue[self.song_no])
    def next(self):
        pass

    def previous(self):
        pass

    def stop(self):
        pass
    ###############

    def seek(self):
        pass

    def _playsong(self, failcount=0, softrepeat=False):
        """ Play song using config.PLAYER called with args config.PLAYERARGS.

        """
        # pylint: disable=R0911,R0912
        if not config.PLAYER.get or not util.has_exefile(config.PLAYER.get):
            g.message = "Player not configured! Enter %sset player <player_app> "\
                "%s to set a player" % (c.g, c.w)
            return

        if config.NOTIFIER.get:
            subprocess.Popen(shlex.split(config.NOTIFIER.get) + [self.song.title])

        size = streams.get_size(self.song.ytid, self.stream['url'])
        songdata = (self.song.ytid, '' if self.stream.get('ext') is None else self.stream.get('ext') + " " + self.stream['quality'],
                    int(size / (1024 ** 2)))
        self.songdata = "%s; %s; %s Mb" % songdata
        screen.writestatus(self.songdata)

        self._launch_player()

        if config.HISTORY.get:
            history.add(self.song)

    def _launch_player(self):
        """ Launch player application. """
        pass

    def send_metadata_mpris(self):
        metadata = util._get_metadata(self.song.title) if config.LOOKUP_METADATA.get else None

        if metadata is None:
            arturl = "https://i.ytimg.com/vi/%s/default.jpg" % self.song.ytid
            metadata = (self.song.ytid, self.song.title, self.song.length,
                        arturl, [''], '')
        else:
            arturl = metadata['album_art_url']
            metadata = (self.song.ytid, metadata['track_title'],
                        self.song.length, arturl,
                        [metadata['artist']], metadata['album'])

        if g.mprisctl:
            g.mprisctl.send(('metadata', metadata))

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
        keys = self._help(short=(not multi and not repeat))
        out = out if multi else content.generate_songlist_display(song=allsongs[0])

        if config.SHOW_PLAYER_KEYS.get and keys is not None:
            out += "\n" + keys

        else:
            playing = "{}{}{}{} of {}{}{}\n".format(*pos) if multi else "\n"
            out += "\n" + " " * (cw - 19) if multi else ""

        fmt = playing, c.r, cur[0].strip()[:cw - 19], c.w, c.w, cur[2], c.w
        out += "%s    %s%s%s %s[%s]%s" % fmt
        out += "    REPEAT MODE" if repeat else ""
        return out

    def make_status_line(self, elapsed_s, prefix, songlength=0, volume=None):
        self._line = self._make_status_line(elapsed_s, prefix, songlength,
                                            volume=volume)

        if self._line != self._last_displayed_line:
            screen.writestatus(self._line)
            self._last_displayed_line = self._line

    def _make_status_line(self, elapsed_s, prefix, songlength=0, volume=None):
        """ Format progress line output.  """
        # pylint: disable=R0914

        display_s = elapsed_s
        display_h = display_m = 0

        if elapsed_s >= 60:
            display_m = display_s // 60
            display_s %= 60

            if display_m >= 60:
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

        cw = util.getxy().width
        prog_bar_size = cw - len(prefix) - len(status_line) - len(vol_suffix) - 7
        progress = int(math.ceil(pct / 100 * prog_bar_size))
        status_line += " [%s]" % ("=" * (progress - 1) +
                                  ">").ljust(prog_bar_size, ' ')
        return prefix + status_line + vol_suffix


class CmdPlayer(BasePlayer):

    def next(self):
        if g.scrobble:
            lastfm.scrobble_track(g.artist, g.album,
                                  g.scrobble_queue[self.song_no])
        self.terminate_process()
        self.song_no += 1

    def previous(self):
        if g.scrobble:
            lastfm.scrobble_track(g.artist, g.album,
                                  g.scrobble_queue[self.song_no])
        self.terminate_process()
        self.song_no -= 1

    def stop(self):
        self.terminate_process()
        self.song_no = len(self.songlist)

    def terminate_process(self):
        self.p.terminate()
        # If using shell=True or the player
        # requires some obscure way of killing the process
        # the child class can define this function

    def _generate_real_playerargs(self):
        pass

    def clean_up(self):
        pass

    def launch_player(self, cmd):
        pass

    def _help(self, short=True):
        pass

    def _launch_player(self):
        """ Launch player application. """

        cmd = self._generate_real_playerargs()

        util.dbg("playing %s", self.song.title)
        util.dbg("calling %s", " ".join(cmd))

        # Fix UnicodeEncodeError when title has characters
        # not supported by encoding
        cmd = [util.xenc(i) for i in cmd]

        self.send_metadata_mpris()
        try:
            self.launch_player(cmd)

        except OSError:
            g.message = util.F('no player') % config.PLAYER.get
            return None

        finally:
            if g.mprisctl:
                g.mprisctl.send(('stop', True))

            if self.p and self.p.poll() is None:
                self.p.terminate()  # make sure to kill mplayer if yewtube crashes

            self.clean_up()


def stream_details(song, failcount=0, override=False, softrepeat=False):
    """Fetch stream details for a song."""
    # don't interrupt preloading:
    while song.ytid in g.preloading:
        screen.writestatus("fetching item..")
        time.sleep(0.1)

    try:
        streams.get(song, force=failcount, callback=screen.writestatus)

    except (IOError, URLError, HTTPError, socket.timeout) as e:
        util.dbg("--ioerror in stream_details call to streams.get %s", str(e))

        if "Youtube says" in str(e):
            g.message = util.F('cant get track') % (song.title + " " + str(e))
            return

        elif failcount < g.max_retries:
            util.dbg("--ioerror - trying next stream")
            failcount += 1
            return stream_details(song, failcount=failcount, override=override, softrepeat=softrepeat)

        elif "pafy" in str(e):
            g.message = str(e) + " - " + song.ytid
            return

    except ValueError:
        g.message = util.F('track unresolved')
        util.dbg("----valueerror in stream_details call to streams.get")
        return

    if failcount == g.max_retries:
        raise TypeError()

    try:
        video = ((config.SHOW_VIDEO.get and override != "audio") or
                 (override in ("fullscreen", "window", "forcevid")))
        m4a = "mplayer" not in config.PLAYER.get
        cached = g.streams[song.ytid]
        stream = streams.select(cached, q=failcount, audio=(not video), m4a_ok=m4a)

        # handle no audio stream available, or m4a with mplayer
        # by switching to video stream and suppressing video output.
        if (not stream or failcount) and not video:
            util.dbg(c.r + "no audio or mplayer m4a, using video stream" + c.w)
            override = "a-v"
            video = True
            stream = streams.select(cached, q=failcount, audio=False, maxres=1600)

        if not stream:
            raise IOError("No streams available")

        return (video, stream, override)

    except (HTTPError) as e:

        # Fix for invalid streams (gh-65)
        util.dbg("----htterror in stream_details call to gen_real_args %s", str(e))
        if failcount < g.max_retries:
            failcount += 1
            return stream_details(song, failcount=failcount,
                                  override=override, softrepeat=softrepeat)
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
