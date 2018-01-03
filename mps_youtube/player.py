import os
import sys
import random
import tempfile
import logging
import json
import re
import math
import time
import shlex
from urllib.error import HTTPError, URLError

from . import g, screen, c, streams, history, content, paths, config, util

mswin = os.name == "nt"
not_utf8_environment = mswin or "UTF-8" not in sys.stdout.encoding



from abc import ABCMeta, abstractmethod

class Player(metaclass=ABCMeta):

    def play(self, songlist, shuffle=False, repeat=False, override=False):
        """ Play a range of songs, exit cleanly on keyboard interrupt. """
        self.songlist = songlist
        self.shuffle = shuffle
        self.repeat = repeat
        self.override = override
        if shuffle:
            random.shuffle(self.songlist)

        self.song_no = 0
        while 0 <= self.song_no <= len(self.songlist)-1:
            song = self.songlist[self.song_no]
            g.content = self._playback_progress(self.song_no, self.songlist, repeat=repeat)

            if not g.command_line:
                screen.update(fill_blank=False)

            hasnext = len(self.songlist) > self.song_no + 1

            if hasnext:
                streams.preload(self.songlist[self.song_no + 1], override=self.override)

            if config.SET_TITLE.get:
                util.set_window_title(song.title + " - mpsyt")

            softrepeat = repeat and len(self.songlist) == 1

            try:
                video, stream = stream_details(song, override=self.override, softrepeat=softrepeat)
                returncode = self._playsong(song, stream, video, override=self.override, softrepeat=softrepeat)

            except KeyboardInterrupt:
                logging.info("Keyboard Interrupt")
                util.xprint(c.w + "Stopping...                          ")
                screen.reset_terminal()
                g.message = c.y + "Playback halted" + c.w
                raise KeyboardInterrupt
                break

            # skip forbidden, video removed/no longer available, etc. tracks
            except TypeError:
                pass

            if self.song_no == -1:
                self.song_no = len(songlist) - 1 if repeat else 0

            elif self.song_no == len(songlist) and repeat:
                self.song_no = 0

    #TODO
    def next(self):
        pass

    def previous(self):
        pass

    def stop(self):
        pass

    #Maybe make these abstract methods
    #for mpris control
    def play_pause(self):
        pass

    def seek(self):
        pass

    def set_position(self):
        pass
    #TODO^

    def _playsong(self, song, stream, video, failcount=0, override=False, softrepeat=False):
        """ Play song using config.PLAYER called with args config.PLAYERARGS."""
        # pylint: disable=R0911,R0912
        if not config.PLAYER.get or not util.has_exefile(config.PLAYER.get):
            g.message = "Player not configured! Enter %sset player <player_app> "\
                "%s to set a player" % (c.g, c.w)
            return

        if config.NOTIFIER.get:
            subprocess.Popen(shlex.split(config.NOTIFIER.get) + [song.title])

        size = streams.get_size(song.ytid, stream['url'])
        songdata = (song.ytid, stream['ext'] + " " + stream['quality'],
                    int(size / (1024 ** 2)))
        songdata = "%s; %s; %s Mb" % songdata
        screen.writestatus(songdata)

        cmd = self._generate_real_playerargs(song, override, stream, video, softrepeat)
        returncode = self._launch_player(song, songdata, cmd)
        failed = returncode not in (0, 42, 43)

        if failed and failcount < g.max_retries:
            util.dbg(c.r + "stream failed to open" + c.w)
            util.dbg("%strying again (attempt %s)%s", c.r, (2 + failcount), c.w)
            screen.writestatus("error: retrying")
            time.sleep(1.2)
            failcount += 1
            return self._playsong(song, stream, video, failcount=failcount, override=override, softrepeat=softrepeat)

        history.add(song)
        return returncode

    def _launch_player(self, song, songdata, cmd):
        """ Launch player application. """

        util.dbg("playing %s", song.title)
        util.dbg("calling %s", " ".join(cmd))

        # Fix UnicodeEncodeError when title has characters
        # not supported by encoding
        cmd = [util.xenc(i) for i in cmd]

        metadata = util._get_metadata(song.title)

        if metadata == None :
            arturl = "https://i.ytimg.com/vi/%s/default.jpg" % song.ytid
            metadata = (song.ytid, song.title, song.length, arturl, [''], '')
        else :
            arturl = metadata['album_art_url']
            metadata = (song.ytid, metadata['track_title'], song.length, arturl, [metadata['artist']], metadata['album'])

        try:
            if g.mprisctl:
                g.mprisctl.send(('metadata', metadata))

            self.launch_player(cmd)


        except OSError:
            g.message = util.F('no player') % config.PLAYER.get
            return None

        finally:
            if g.mprisctl:
                g.mprisctl.send(('stop', True))

            if self.p and self.p.poll() is None:
                self.p.terminate()  # make sure to kill mplayer if mpsyt crashes

            self.clean_up()

    def _playback_progress(self, idx, allsongs, repeat=False):
        """ Generate string to show selected tracks, indicate current track. """
        # pylint: disable=R0914
        # too many local variables
        cw = util.getxy().width
        out = "  %s%-XXs%s%s\n".replace("XX", str(cw - 9))
        out = out % (c.ul, "Title", "Time", c.w)
        show_key_help = (util.is_known_player(config.PLAYER.get) and
                config.SHOW_MPLAYER_KEYS.get)
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

        if show_key_help:
            out += "\n" + keys

        else:
            playing = "{}{}{}{} of {}{}{}\n".format(*pos) if multi else "\n"
            out += "\n" + " " * (cw - 19) if multi else ""

        fmt = playing, c.r, cur[0].strip()[:cw - 19], c.w, c.w, cur[2], c.w
        out += "%s    %s%s%s %s[%s]%s" % fmt
        out += "    REPEAT MODE" if repeat else ""
        return out


    @abstractmethod
    def _generate_real_playerargs(self, song, override, stream, isvideo, softrepeat):
        pass

    @abstractmethod
    def clean_up(self):
        pass

    @abstractmethod
    def launch_player(self, cmd):
        pass

    @abstractmethod
    def _help(self, short=True):
        pass



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

        return (video, stream)

    except (HTTPError) as e:

        # Fix for invalid streams (gh-65)
        util.dbg("----htterror in stream_details call to gen_real_args %s", str(e))
        if failcount < g.max_retries:
            failcount += 1
            return stream_details(song, failcount=failcount, override=override, softrepeat=softrepeat)
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

def check_player(player):
    if player == 'mpv':
        from .players.mpv import mpv
        return mpv()

if not config.PLAYER.get or not util.has_exefile(config.PLAYER.get):
    g.message = "Player not configured! Enter %sset player <player_app> "\
                "%s to set a player" % (c.g, c.w)

else:
    player = check_player(config.PLAYER.get)
