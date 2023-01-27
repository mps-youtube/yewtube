import os
import re
import sys
import time
import shlex
import random
import subprocess
from urllib.request import urlopen
from urllib.error import HTTPError

from .. import g, c, screen, streams, content, config, util, pafy
from . import command, PL
from .search import yt_url, user_pls
from .songlist import dump, plist


@command(r'(dv|da|d|dl|download)\s*(\d{1,4})', 'da', 'dv', 'd', 'dl', 'download')
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
        g.content = content.generate_songlist_display()
        return

    elif g.browse_mode != "normal":
        g.message = "Download must refer to a specific video item"
        g.message = c.y + g.message + c.w
        g.content = content.generate_songlist_display()
        return

    screen.writestatus("Fetching video info...")
    song = (g.model[int(num) - 1])

    # best = dltype.startswith("dv") or dltype.startswith("da")
    #
    # if not best:
    #
    #     try:
    #         # user prompt for download stream
    #         url, ext, url_au, ext_au = prompt_dl(song)
    #
    #     except KeyboardInterrupt:
    #         g.message = c.r + "Download aborted!" + c.w
    #         g.content = content.generate_songlist_display()
    #         return
    #
    #     if not url or ext_au == "abort":
    #         # abort on invalid stream selection
    #         g.content = content.generate_songlist_display()
    #         g.message = "%sNo download selected / invalid input%s" % (c.y, c.w)
    #         return
    #
    #     else:
    #         # download user selected stream(s)
    #         filename = _make_fname(song, ext)
    #         args = (song, filename, url)
    #
    #         if url_au and ext_au:
    #             # downloading video and audio stream for muxing
    #             audio = False
    #             filename_au = _make_fname(song, ext_au)
    #             args_au = (song, filename_au, url_au)
    #
    #         else:
    #             audio = ext in ("m4a", "ogg")
    #
    #         kwargs = dict(audio=audio)
    #
    # elif best:
    #     # set updownload without prompt
    #     url_au = None
    #     av = "audio" if dltype.startswith("da") else "video"
    #     audio = av == "audio"
    #     filename = _make_fname(song, None, av=av)
    #     args = (song, filename)
    #     kwargs = dict(url=None, audio=audio)

    try:
        # perform download(s)
        # dl_filenames = [args[1]]
        # f = _download(*args, **kwargs)
        success = pafy.download_video(song.ytid, config.DDIR.get, True if dltype.startswith("da") else False)
        if success:
            g.message = "Saved \'" + song.title + "\' to " + c.g + config.DDIR.get + c.w

        # if url_au:
        #     dl_filenames += [args_au[1]]
        #     _download(*args_au, allow_transcode=False, **kwargs)

    except KeyboardInterrupt:
        g.message = c.r + "Download halted!" + c.w

        # try:
        #     for downloaded in dl_filenames:
        #         os.remove(downloaded)
        #
        # except IOError:
        #     pass

    # if url_au:
    #     # multiplex
    #     name, ext = os.path.splitext(args[1])
    #     tmpvideoname = name + '.' +str(random.randint(10000, 99999)) + ext
    #     os.rename(args[1], tmpvideoname)
    #     mux_cmd = [g.muxapp, "-i", tmpvideoname, "-i", args_au[1], "-c",
    #                "copy", name + ".mp4"]
    #
    #     try:
    #         subprocess.call(mux_cmd)
    #         g.message = "Saved to :" + c.g + mux_cmd[7] + c.w
    #         os.remove(tmpvideoname)
    #         os.remove(args_au[1])
    #
    #     except KeyboardInterrupt:
    #         g.message = "Audio/Video multiplex aborted!"

    g.content = content.generate_songlist_display()


@command(r'(da|dv)\s+((?:\d+\s\d+|-\d+|\d+-|\d+,)(?:[\d\s,-]*))', 'da', 'dv')
def down_many(dltype, choice, subdir=None):
    """ Download multiple items. """
    choice = util.parse_multi(choice)
    choice = list(set(choice))
    downsongs = [g.model[int(x) - 1] for x in choice]
    temp = g.model[::]
    g.model.songs = downsongs[::]
    count = len(downsongs)
    av = "audio" if dltype.startswith("da") else "video"
    msg = ""

    def handle_error(message):
        """ Handle error in download. """
        g.message = message
        g.content = disp
        screen.update()
        time.sleep(2)
        g.model.songs.pop(0)

    try:
        for song in downsongs:
            g.result_count = len(g.model)
            disp = content.generate_songlist_display()
            title = "Download Queue (%s):%s\n\n" % (av, c.w)
            disp = re.sub(r"(Num\s*?Title.*?\n)", title, disp)
            g.content = disp
            screen.update()

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
        g.result_count = len(g.model)
        g.content = content.generate_songlist_display()


@command(r'(da|dv)pl\s+%s' % PL, 'dapl', 'dvpl')
def down_plist(dltype, parturl):
    """ Download YouTube playlist. """

    plist(parturl)
    dump(False)
    title = g.pafy_pls[parturl][0].title
    # Remove double quotes for convenience
    subdir = util.sanitize_filename(title.replace('"', ''))
    down_many(dltype, "1-", subdir=subdir)
    msg = g.message
    plist(parturl)
    g.message = msg


@command(r'(da|dv)upl\s+(.*)', 'daupl', 'dvupl')
def down_user_pls(dltype, user):
    """ Download all user playlists. """
    user_pls(user)
    for i in g.ytpls:
        down_plist(dltype, i.get('link'))

    return


def _make_fname(song, ext=None, av=None, subdir=None):
    """" Create download directory, generate filename. """
    # pylint: disable=E1103
    # Instance of 'bool' has no 'extension' member (some types not inferable)
    ddir = os.path.join(config.DDIR.get, subdir) if subdir else config.DDIR.get
    if not os.path.exists(ddir):
        os.makedirs(ddir)

    if not ext:
        stream = streams.select(streams.get(song),
                audio=av == "audio", m4a_ok=True)
        ext = stream['ext']

    # filename = song.title[:59] + "." + ext
    filename = song.title + "." + ext
    # Remove double quotes for convenience
    filename = filename.replace('"', '')
    filename = os.path.join(ddir, util.sanitize_filename(filename))
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
    util.dbg("starting remux")
    temp_file = filename + "." + str(random.randint(10000, 99999))
    os.rename(filename, temp_file)
    meta = extract_metadata(title)
    metadata = ["title=%s" % meta["title"]]

    if meta["artist"]:
        metadata = ["title=%s" % meta["title"], "-metadata",
                    "artist=%s" % meta["artist"]]

    cmd = [g.muxapp, "-y", "-i", temp_file, "-acodec", "copy", "-metadata"]
    cmd += metadata + ["-vn", filename]
    util.dbg(cmd)

    try:
        with open(os.devnull, "w") as devnull:
            subprocess.call(cmd, stdout=devnull, stderr=subprocess.STDOUT)

    except OSError:
        util.dbg("Failed to remux audio using %s", g.muxapp)
        os.rename(temp_file, filename)

    else:
        os.unlink(temp_file)
        util.dbg("remuxed audio file using %s" % g.muxapp)


def transcode(filename, enc_data):
    """ Re encode a download. """
    base = os.path.splitext(filename)[0]
    exe = g.muxapp if g.transcoder_path == "auto" else g.transcoder_path

    # ensure valid executable
    if not exe or not os.path.exists(exe) or not os.access(exe, os.X_OK):
        util.xprint("Encoding failed. Couldn't find a valid encoder :(\n")
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
    cmd = config.DOWNLOAD_COMMAND.get
    ddir, basename = config.DDIR.get, os.path.basename(filename)
    cmd_list = shlex.split(cmd)

    def list_string_sub(orig, repl, lst):
        """ Replace substrings for items in a list. """
        return [x if orig not in x else x.replace(orig, repl) for x in lst]

    cmd_list = list_string_sub("%F", filename, cmd_list)
    cmd_list = list_string_sub("%d", ddir, cmd_list)
    cmd_list = list_string_sub("%f", basename, cmd_list)
    cmd_list = list_string_sub("%u", url, cmd_list)
    cmd_list = list_string_sub("%i", song.ytid, cmd_list)
    util.dbg("Downloading using: %s", " ".join(cmd_list))
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
    if config.DOWNLOAD_COMMAND.get:
        title = c.y + os.path.splitext(os.path.basename(filename))[0] + c.w
        util.xprint("Downloading %s using custom command" % title)
        external_download(song, filename, url)
        return None

    if not config.OVERWRITE.get:
        if os.path.exists(filename):
            util.xprint("File exists. Skipping %s%s%s ..\n" %
                    (c.r, filename, c.w))
            time.sleep(0.2)
            return filename

    util.xprint("Downloading to %s%s%s .." % (c.r, filename, c.w))
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
        rate = 0
        if elapsed != 0:
            rate = (bytesdone / 1024) / elapsed
        if rate:
            eta = (total - bytesdone) / (rate * 1024)
        else:
            eta = 0
        stats = (c.y, bytesdone, c.w, bytesdone * 1.0 / total, rate, eta)

        if not chunk:
            outfh.close()
            break

        status = status_string.format(*stats)
        sys.stdout.write("\r" + status + ' ' * 4 + "\r")
        sys.stdout.flush()

    active_encoder = g.encoders[config.ENCODER.get]
    ext = filename.split(".")[-1]
    valid_ext = ext in active_encoder['valid'].split(",")

    if audio and g.muxapp:
        remux_audio(filename, song.title)

    if config.ENCODER.get != 0 and valid_ext and allow_transcode:
        filename = transcode(filename, active_encoder)

    return filename


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
    screen.update()

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
    mediatype = [i for i in dl_data if i['url'] == url][0]['mediatype']

    if mediatype == "video" and g.muxapp and not config.DOWNLOAD_COMMAND.get:
        # offer mux if not using external downloader
        dl_data, p = get_dl_data(song, mediatype="audio")
        dl_text = gen_dl_text(dl_data, song, p)
        au_choices = "1" if len(dl_data) == 1 else "1-%s" % len(dl_data)
        footer = [util.F('-audio') % ext, util.F('select mux') % au_choices]
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
    hdr.append("  [" + util.fmt_time(song.length) + "]")
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


def get_dl_data(song, mediatype="any"):
    """ Get filesize and metadata for all streams, return dict. """
    def mbsize(x):
        """ Return size in MB. """
        return str(int(x / (1024 ** 2)))

    p = util.get_pafy(song)
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
            util.dbg(c.r + "---Error getting stream size" + c.w)
            size = 0

        item = {'mediatype': stream.mediatype,
                'size': size,
                'ext': stream.extension,
                'quality': stream.quality,
                'notes': stream.notes,
                'url': stream.url}

        dldata.append(item)

    screen.writestatus("")
    return dldata, p


@command(r'dlurl\s(.*[-_a-zA-Z0-9]{11}.*)', 'dlurl')
def dl_url(url):
    """ Open and prompt for download of youtube video url. """
    g.browse_mode = "normal"
    yt_url(url)

    if len(g.model) == 1:
        download("download", "1")

    if g.command_line:
        sys.exit()


@command(r'daurl\s(.*[-_a-zA-Z0-9]{11}.*)', 'daurl')
def da_url(url):
    """ Open and prompt for download of youtube best audio from url. """
    g.browse_mode = "normal"
    yt_url(url)

    if len(g.model) == 1:
        download("da", "1")

    if g.command_line:
        sys.exit()
