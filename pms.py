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

__version__ = "0.02"
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
if sys.version_info[:2] >= (3, 0):
    PY3 = True
    from urllib.request import build_opener
    raw_input = input
else:
    from urllib2 import build_opener

#logging.basicConfig(level=logging.DEBUG)

PLAYER = "mplayer"
PLAYERARGS = "-nocache -prefer-ipv4 -really-quiet"
COLOURS = True # Change to false if you experience display issues

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
            ("  ", " "), ("&amp;", "&")):
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
                    logging.error("Couldn't get %s" % f)
                    raise Exception("wtf1")
            songs.append(cursong)
    else:
        logging.debug("couldn't find regex: <li.duration[^>]+)\>")
        return False
    return songs

def generate_song_meta(song):
    r" Generates formatted song metadata "
    out = ""
    fields = "singer song duration rate size".split(" ")
    names = "Artist Title Length Bitrate Size".split(" ")
    maxlen = max([len(song.get(f) or "-" * 18) for f in fields])
    hyphens = min(78, maxlen + 10)
    hyphenstr = ("  " + "-" * hyphens + "\n")
    fmt = "  %s%-7s%s : %s%s%s\n"
    for n, name in enumerate(names):
        if song[fields[n]]:
            out += (fmt % (c.y, name, c.w, c.g, song[fields[n]], c.w))
    return("\n" + hyphenstr + out + hyphenstr)

def generate_choices(songs):
    r" Generates list of choices from a song list"
    fmthd = "%s%-6s %-7s %-21s %-22s %-8s %-8s%s\n"
    out = (fmthd % (c.g, "ITEM", "SIZE", "ARTIST", "TRACK", "LENGTH",
        "BITRATE", c.w))
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
        out += (fmtrow % (col, str(n+1), str(size)[:3] + " Mb", artist[:20],
            title[:21], duration[:8], bitrate[:3], c.w))
    return(out)

def get_stream(song):
    r" Takes a song, returns the real url"
    if not "curl" in song:
        logging.debug("API call: %s" % song['link'])
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
    intset = False
    if len(songs) > 1:
        txt = ("[%s1-%s%s] to play or [%sd 1-%s%s] to download or [%sq%s]uit"
            " or enter new search\n : ")
        txt = txt  % (c.g, len(songs), c.w, c.g, len(songs), c.w, c.g, c.w)
        choice = raw_input(txt)
        if choice.lower() == "q" or choice.lower() == "quit":
            sys.exit("Laters")
        elif not choice:
            return("nilerror", None, songs)
        else:
            try:
                intset = int(choice)
                song = songs[int(choice) - 1]
                return("play", song, songs)
            except: # Nan
                dl = re.match(r'(?:d|D)(?:\s)*(\d+)', choice)
                if intset:
                    return("rangeerror", intset, songs)
                elif dl:
                    song = songs[int(dl.group(1)) -1]
                    return("download", song, songs)
                else:
                    return("search", choice, songs)

def playsong(song):
    r'play song, uses mplayer by default'
    curl = get_stream(song)
    song['curl'] = curl
    print("Playing - [%sq%s] to quit.." % (c.y, c.w))
    print("")
    callx = [PLAYER] + PLAYERARGS.split() + [song['curl']]
    call(callx)

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
    filename = song['singer'][:30] + " - " + song['song'][:30] + ".mp3"
    print("\nDownloading %s%s%s .." % (c.g, filename, c.w))
    status_string = ('  {}{:,}{} Bytes [{}{:.2%}{}] received. Rate: [{}{:4.0f}'
                     ' kbps{}].  ETA: [{}{:.0f} secs{}]')
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
        progress_stats = (c.y, bytesdone, c.w, c.y, bytesdone * 1.0 / total,
                c.w, c.y, rate, c.w, c.y, eta, c.w)
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
        return("Sorry, %s%s%s is not a valid choice"  %(c.g, value, c.w))

def start(args):
    songs = dosearch(args)
    if not args:
        inp = raw_input("Enter artist/song to search : ")
        start(inp)
    elif not songs:
        print("Sorry, nothing matched %s%s%s" % (c.g, args, c.w))
        start(None)
    elif songs:
        text = generate_choices(songs)
        print(text)
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

class c:
    white = "\033[0m"
    red, green, yellow, blue, pink = ["\033[%sm" % n for n in range(91,96)]
    if not COLOURS:
        red = green = yellow = blue = pink = white = ""
    r, g, y, b, p, w = red, green, yellow, blue, pink, white

main()
