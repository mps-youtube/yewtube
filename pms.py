#!/usr/bin/python

''' pms
    Copyright (C)  2013 nagev

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.  '''

__version__ = "0.06"
__author__ = "nagev"
__license__ = "GPLv3"

import logging
import time
import json
import sys
import re
import os
from subprocess import call

# Python 3 compatibility hack
PY3 = False
compat_input = None
if sys.version_info[:2] >= (3, 0):
    PY3 = True
    from urllib.request import build_opener
    compat_input = input
else:
    from urllib2 import build_opener
    compat_input = raw_input

#logging.basicConfig(level=logging.DEBUG)

PLAYER = "mplayer"
PLAYERARGS = "-nolirc -nocache -prefer-ipv4 -really-quiet"
COLOURS = True
DDIR = os.path.join(os.path.expanduser("~"), "Downloads", "PMS")

if os.name == "nt":  # Disable colours for Windows
    COLOURS = False
else:
    try:
        import readline  # import realine if not running on windows
        readline.get_history_length()  # redundant, prevents unused import warn
    except ImportError:
        pass  # no biggie

opener = build_opener()
ua = ("Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64;"
      "Trident/5.0)")
opener.addheaders = [('User-Agent', ua)]
urlopen = opener.open


def tidy(raw, field):
    if field == "duration":
        raw = time.strftime('%M:%S', time.gmtime(int(raw)))
    else:
        for r in (("&#039;", "'"), ("&amp;#039;", "'"), ("&amp;amp;", "&"),
                 ("  ", " "), ("&amp;", "&"), ("&quot;", '"')):
            raw = raw.replace(r[0], r[1])
    return raw


def get_tracks_from_page(page):
    r" Gets search results from web page "
    fields = "duration file_id singer song link rate size source".split(" ")
    matches = re.findall(r"\<li.(duration[^>]+)\>", page)
    songs = []
    if matches:
        for song in matches:
            cursong = {}
            for f in fields:
                v = re.search(r'%s=\"([^"]+)"' % f, song)
                if v:
                    cursong[f] = tidy(v.group(1), f)
                else:
                    logging.error("Couldn't get " + f)
                    raise Exception("wtf1")
            songs.append(cursong)
    else:
        logging.error("got unexpected webpage")
        return False
    return songs


def generate_song_meta(song):
    r" Generates formatted song metadata "
    fields = "singer song duration rate size".split(" ")
    names = "Artist Title Length Bitrate Size".split(" ")
    maxlen = max([len(song.get(f) or "-" * 18) for f in fields])
    hyphens = min(78, maxlen + 10)
    hyphenstr = ("  " + "-" * hyphens + "\n")
    fmt = "  %s%-7s%s : %s%s%s\n"
    out = "\n" + hyphenstr
    for n, name in enumerate(names):
        if song[fields[n]]:
            out += (fmt % (c.y, name, c.w, c.g, song[fields[n]], c.w))
    return(out + hyphenstr)


def generate_choices(songs):
    r" Generates list of choices from a song list"
    fmthd = "%s%-6s %-7s %-21s %-22s %-8s %-8s%s\n"
    out = (fmthd % (c.g, "Item", "Size", "Artist", "Track", "Length",
           "Bitrate", c.w))
    out += (fmthd % (c.w, "----", "----", "------", "-----", "------",
            "-------", c.w))
    fmtrow = "%s%-6s %-7s %-21s %-22s %-8s %-8s%s\n"
    for n, x in enumerate(songs):
        col = c.p
        if n % 2 == 0:
            col = c.r
        size = x.get('size') or 0
        title = x.get('song') or "unknown title"
        artist = x.get('singer') or "unknown artist"
        duration = x.get('duration') or "unknown length"
        bitrate = x.get('rate') or "unknown"
        out += (fmtrow % (col, str(n + 1), str(size)[:3] + " Mb", artist[:20],
                title[:21], duration[:8], bitrate[:3], c.w))
    return(out)


def get_stream(song):
    r" Takes a song, returns the real url"
    if not "curl" in song:
        logging.debug("API call: " + song['link'])
        URL = 'http://pleer.com/site_api/files/get_url'
        url = URL + "?action=download&id=%s" % song['link']
        wdata = urlopen(url).read().decode("utf8")
        j = json.loads(wdata)
        curl = j['track_link']
        return(curl)
    else:
        return song['curl']


def reqinput(songs):
    r'gets input, returns action/value pair and songlist'
    if not songs:
        return("nilinput", None, None)
    txt = ("[{0}1-{1}{2}] to play or [{0}d 1-{1}{2}] to download or [{0}q{2}]"
           "uit or enter new search\n > ".format(c.g, len(songs), c.w))
    r = {'nil': r'\s*$',
         'play': r'\s*(\d{1,3})',
         'dl': r'\s*(?:d|dl|download|down)(?:\s)*(\d{1,3})',
         'quit': r'\s*(q|quit)\s*$'}
    choice = compat_input(txt)
    retval = ()
    for k in r.keys():
        r[k] = re.compile(r[k], re.IGNORECASE)
    if r['quit'].match(choice):
        sys.exit("{}(c) 2013 nagev.  Thanks for coming..{}".format(c.b, c.w))
    elif r['nil'].match(choice):
        retval = ("nilerror", None, songs)
    elif r['play'].match(choice):
        songnum = int(r['play'].match(choice).group(1))
        if songnum > len(songs):
            return ("rangeerror", songnum, songs)
        retval = ("play", songs[songnum - 1], songs)
    elif r['dl'].match(choice):
        songnum = int(r['dl'].match(choice).group(1))
        if songnum > len(songs):
            return ("rangeerror", songnum, songs)
        retval = ("download", songs[songnum - 1], songs)
    else:
        retval = ("search", choice, songs)
    return retval


def playsong(song):
    r'play song, uses mplayer by default'
    curl = get_stream(song)
    song['curl'] = curl
    print("Playing - [%sq%s] to quit.." % (c.y, c.w))
    print("")
    try:
        opener.open(curl).headers['content-length']
    except IOError:
        print("\nSorry, this track no longer exists!")
    try:
        callx = [PLAYER] + PLAYERARGS.split() + [song['curl']]
        call(callx)
    except OSError:
        print("{}{}{} not found on this system".format(c.y, PLAYER, c.w))
        time.sleep(2)


def dosearch(term):
    # perform search on term, returns songs or false
    if not term:
        logging.debug("no search term")
        return False
    else:
        print("\nSearch for '%s%s%s'\n" % (c.y, term, c.w))
        url = "http://pleer.com/search?q=%s&target=tracks&page=%s"
        url = url % (term.replace(" ", "+"), 1)
        wdata = urlopen(url).read().decode("utf8")
        songs = get_tracks_from_page(wdata)
        if not songs:
            return False
        return songs


def main():
    args = sys.argv[1:]
    args = " ".join(args).strip()
    start(args)


def download(song):
    r'Downloads file, shows status'
    if not os.path.exists(DDIR):
        os.makedirs(DDIR)
    filename = song['singer'][:30] + " - " + song['song'][:30] + ".mp3"
    filename = os.path.join(DDIR, filename)
    print("\nDownloading %s%s%s .." % (c.g, filename, c.w))
    status_string = ('  {0}{1:,}{2} Bytes [{0}{3:.2%}{2}] received. Rate: '
                     '[{0}{4:4.0f} kbps{2}].  ETA: [{0}{5:.0f} secs{2}]')
    url = get_stream(song)
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
        progress_stats = (c.y, bytesdone, c.w, bytesdone * 1.0 / total, rate,
                          eta)
        if not chunk:
            outfh.close()
            break
        status = status_string.format(*progress_stats)
        sys.stdout.write("\r" + status + ' ' * 4 + "\r")
        sys.stdout.flush()
    print("\n%sDone\n" % c.y)


def songaction(action, value, songs):
    if action == "play":
        print(generate_song_meta(value))
        playsong(value)
    elif action == "download":
        download(value)
    elif action == "rangeerror" or action == "nilerror":
        value = value or "zilch"
        return("Sorry, %s%s%s is not a valid choice" % (c.g, value, c.w))


def start(args):
    songs = dosearch(args)
    if not args:
        inp = compat_input("Enter artist/song to search : ")
        start(inp)
    elif not songs:
        print("Sorry, nothing matched %s%s%s" % (c.g, args, c.w))
        start(None)
    elif songs:
        text = generate_choices(songs)
        print(text.encode("utf8"))
        a, v, s = reqinput(songs)
        sactions = "play download rangeerror nilerror".split(" ")
        while a in sactions:
            status = songaction(a, v, s)
            print(generate_choices(songs))
            if status:
                print(status)
            a, v, s = reqinput(songs)
        if a == "search":
            start(v)


class c(object):
    white = "\033[0m"
    #red, green, yellow, blue, pink = ["\033[%sm" % n for n in range(91, 96)]
    red, green, yellow, blue, pink = ["\x1b[%sm" % n for n in range(91, 96)]
    if not COLOURS:
        red = green = yellow = blue = pink = white = ""
    r, g, y, b, p, w = red, green, yellow, blue, pink, white

main()
