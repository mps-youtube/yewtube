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

from . import g, screen, c, streams, history, content, paths, config, util

mswin = os.name == "nt"
not_utf8_environment = mswin or "UTF-8" not in sys.stdout.encoding


def play_range(songlist, shuffle=False, repeat=False, override=False):
    """ Play a range of songs, exit cleanly on keyboard interrupt. """
    if shuffle:
        random.shuffle(songlist)

    n = 0
    while 0 <= n <= len(songlist)-1:
        song = songlist[n]
        g.content = _playback_progress(n, songlist, repeat=repeat)

        if not g.command_line:
            screen.update(fill_blank=False)

        hasnext = len(songlist) > n + 1

        if hasnext:
            streams.preload(songlist[n + 1], override=override)

        util.set_window_title(song.title + " - mpsyt")
        try:
            returncode = _playsong(song, override=override)

        except KeyboardInterrupt:
            logging.info("Keyboard Interrupt")
            util.xprint(c.w + "Stopping...                          ")
            screen.reset_terminal()
            g.message = c.y + "Playback halted" + c.w
            break
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


def _playback_progress(idx, allsongs, repeat=False):
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
    keys = _mplayer_help(short=(not multi and not repeat))
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


def _mplayer_help(short=True):
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


def _playsong(song, failcount=0, override=False):
    """ Play song using config.PLAYER called with args config.PLAYERARGS."""
    # pylint: disable=R0911,R0912
    if not config.PLAYER.get or not util.has_exefile(config.PLAYER.get):
        g.message = "Player not configured! Enter %sset player <player_app> "\
            "%s to set a player" % (c.g, c.w)
        return

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
            return _playsong(song, failcount=failcount, override=override)

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

    except (HTTPError) as e:

        # Fix for invalid streams (gh-65)
        util.dbg("----htterror in _playsong call to gen_real_args %s", str(e))
        if failcount < g.max_retries:
            failcount += 1
            return _playsong(song, failcount=failcount, override=override)
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

    size = streams.get_size(song.ytid, stream['url'])
    songdata = (song.ytid, stream['ext'] + " " + stream['quality'],
                int(size / (1024 ** 2)))
    songdata = "%s; %s; %s Mb" % songdata
    screen.writestatus(songdata)

    cmd = _generate_real_playerargs(song, override, stream, video)
    returncode = _launch_player(song, songdata, cmd)
    failed = returncode not in (0, 42, 43)

    if failed and failcount < g.max_retries:
        util.dbg(c.r + "stream failed to open" + c.w)
        util.dbg("%strying again (attempt %s)%s", c.r, (2 + failcount), c.w)
        screen.writestatus("error: retrying")
        time.sleep(1.2)
        failcount += 1
        return _playsong(song, failcount=failcount, override=override)

    history.add(song)
    return returncode


def _generate_real_playerargs(song, override, stream, isvideo):
    """ Generate args for player command.

    Return args.

    """
    # pylint: disable=R0914
    # pylint: disable=R0912

    if "uiressl=yes" in stream['url'] and "mplayer" in config.PLAYER.get:
        ver = g.mplayer_version
        # Mplayer too old to support https
        if not (ver > (1,1) if isinstance(ver, tuple) else ver >= 37294):
            raise IOError("%s : Sorry mplayer doesn't support this stream. "
                          "Use mpv or update mplayer to a newer version" % song.title)

    # pylint: disable=E1103
    # pylint thinks PLAYERARGS.get might be bool
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

        if "mplayer" in config.PLAYER.get:
            util.list_update("-really-quiet", args, remove=True)
            util.list_update("-noquiet", args)
            util.list_update("-prefer-ipv4", args)

        elif "mpv" in config.PLAYER.get:
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

    elif "vlc" in config.PLAYER.get:
        util.list_update("--play-and-exit", args)

    return [config.PLAYER.get] + args + [stream['url']]


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


def _launch_player(song, songdata, cmd):
    """ Launch player application. """

    util.dbg("playing %s", song.title)
    util.dbg("calling %s", " ".join(cmd))

    # Fix UnicodeEncodeError when title has characters
    # not supported by encoding
    cmd = [util.xenc(i) for i in cmd]

    arturl = "http://i.ytimg.com/vi/%s/default.jpg" % song.ytid
    input_file = None
    if ("mplayer" in config.PLAYER.get) or ("mpv" in config.PLAYER.get):
        input_file = _get_input_file()
    sockpath = None
    fifopath = None

    try:
        if "mplayer" in config.PLAYER.get:
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
            _player_status(p, songdata + "; ", song.length)
            returncode = p.wait()

        elif "mpv" in config.PLAYER.get:
            cmd.append('--input-conf=' + input_file)

            if g.mpv_usesock:
                sockpath = tempfile.mktemp('.sock', 'mpsyt-mpv')
                cmd.append(g.mpv_usesock + '=' + sockpath)

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

            _player_status(p, songdata + "; ", song.length, mpv=True,
                          sockpath=sockpath)
            returncode = p.wait()

        else:
            with open(os.devnull, "w") as devnull:
                returncode = subprocess.call(cmd, stderr=devnull)
            p = None

        return returncode

    except OSError:
        g.message = util.F('no player') % config.PLAYER.get
        return None

    finally:
        if input_file:
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


def _player_status(po_obj, prefix, songlength=0, mpv=False, sockpath=None):
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
                    line = _make_status_line(elapsed_s, prefix, songlength,
                                            volume=volume_level)

                    if line != last_displayed_line:
                        screen.writestatus(line)
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

                    line = _make_status_line(elapsed_s, prefix, songlength,
                                            volume=volume_level)

                    if line != last_displayed_line:
                        screen.writestatus(line)
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


def _make_status_line(elapsed_s, prefix, songlength=0, volume=None):
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

    cw = util.getxy().width
    prog_bar_size = cw - len(prefix) - len(status_line) - len(vol_suffix) - 7
    progress = int(math.ceil(pct / 100 * prog_bar_size))
    status_line += " [%s]" % ("=" * (progress - 1) +
                              ">").ljust(prog_bar_size, ' ')
    return prefix + status_line + vol_suffix
