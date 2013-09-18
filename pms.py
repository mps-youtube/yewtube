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

__version__ = "0.01"
__author__ = "nagev"
__license__ = "GPLv3"

import sys
import logging
import argparse
from json import loads
from subprocess import call

# python 2/3 compatibility
PY3 = False
if sys.version_info[:2] >= (3, 0):
    PY3 = True
    from urllib.request import urlopen
    raw_input = input
else:
    from urllib2 import urlopen

#logging.basicConfig(level=logging.DEBUG)

PLAYER = "mplayer"
PLAYERARGS = "-nocache -prefer-ipv4 -really-quiet"

def compat_content_length(resp):
    if PY3:
        return(resp.getheader("Content-Length"))
    else:
        return(resp.info().getheaders("Content-Length")[0])

def getclean(songs, num):
    # return dict of songs for working urls
    # add size inf
    clean = []
    logging.debug(len(songs))
    for song in songs:
        url = song['url']
        try:
            resp = urlopen(url, None, 2)
            if not resp:
                raise Exception
            size = compat_content_length(resp)
            size = float(size) / 1024 ** 2
            if not size:
                raise Exception
            url = resp.geturl()
            if "soundcloud" in url:
                logging.debug("bah soundcloud")
                # the soundcloud url's don't seem to play in mplayer
                # works with vlc though
                if "mplayer" in PLAYER.lower():
                    raise Exception
        except:
            #pass
            sys.stdout.write("-")
            sys.stdout.flush()
            continue
            #raise
        url = url.replace("#_=_", "")
        song['curl'] = url
        for field in "title artist album".split(" "):
            song["c" + field] = song.get(field, "Unknown") 
        song['csize'] = size
        song['ctags'] = ", ".join(song.get("tags"))
        clean.append(song)
        sys.stdout.write("+")
        sys.stdout.flush()
        if len(clean) >= num:
            break
    return clean

def dosearch(results, term):
    url = "http://ex.fm/api/v3/song/search/%s?start=0&results=%s"
    url = url % (term, results)
    try:
        rawdata = urlopen(url, None, 15).read().decode("utf8")
    except:
        print("Timed out..")
        sys.exit()
    songs = loads(rawdata)['songs']
    return songs
    
def getargs():
    parser = argparse.ArgumentParser(description="PMS Music Seeker")
    parser.add_argument(
            'query', 
            nargs="+",
            type=str,
            help = "song and/or artist"
            )
    parser.add_argument(
            "-c", 
            "--count",
            default=1,
            choices=range(21),
            type=int,
            metavar="N",
            required=False,
            help="number of results"
            )
    return(parser.parse_args())

def playsong(song):
    callx = [PLAYER] + PLAYERARGS.split() + [song['curl']]
    call(callx)

def generate_choices(songs):
    fmt = "%-6s %-7s %-21s %-22s %-23s"
    print("\n")
    print(fmt % ("ITEM", "SIZE", "ARTIST", "TRACK", "ALBUM"))
    print(fmt % ("----", "----", "------", "-----", "-----"))
    fmt = "%s%-6s %-7s %-21s %-22s %-23s"
    for n, x in enumerate(songs):
        white = "\033[0m"
        col = white
        if n % 2 == 0:
            col = "\033[93m"
        size = x.get('csize') or 0
        title = x.get('ctitle') or "unknown title"
        artist = x.get('cartist') or "unknown artist"
        album = x.get('calbum') or "unknown album"
        print(fmt % (col, str(n+1), str(size)[:3] + " Mb", artist[:20],
            title[:21], album[:23]))
    print(white)

def show_song_meta(song):
    fields = "cartist ctitle calbum ckeywords ctags".split(" ")
    hyphens = max([len(song.get(f) or "-" * 18) for f in fields]) + 9
    hyphens = min(78, hyphens)
    print("\n  " + "-" * hyphens)
    print("  \033[93martist\033[0m : \033[92m%s\033[0m " % song['cartist'])
    print("  \033[93mtitle\033[0m  : \033[92m%s\033[0m " % song['ctitle'])
    print("  \033[93malbum\033[0m  : \033[92m%s\033[0m " % song['calbum'])
    if song['ctags']:
        print("  \033[93mtags\033[0m   : \033[92m%s\033[0m " % song['ctags'])
    print("  \033[93msize\033[0m   : \033[92m%.2f MB\033[0m" % song['csize'])
    print("  " + "-" * hyphens)

def reqinput(songlist):
    col = '\033[92m'
    white = '\033[0m'
    if len(songlist) > 1:
        txt = "\n[%s1-%s%s] or [%sq%s]uit  : " 
        txt = txt  % (col, len(songlist), white, col, white)
        choice = raw_input(txt)
        if choice.lower() == "q" or choice.lower() == "quit":
            sys.exit("Laters")
        elif choice == "l":
            #generate_choices(songlist)
            pass
        else:
            try:
                selected = int(choice)
                song = songlist[int(choice) - 1]
                show_song_meta(song)
                print("\nPlaying - press [%sq%s] to quit.." % (col, white))
                playsong(song)
            except:
                print("WTF ?")
        choice = None
        generate_choices(songlist)
        reqinput(songlist)

def main():
    col = '\033[92m'
    white = '\033[0m'
    args = getargs()
    searchfor = " ".join(args.query)
    searchsrv = "+".join(args.query)
    count = args.count
    print("Searching for '%s'\n" % searchfor),
    try:
        exresults = dosearch(count+10, searchsrv)
    except:
        print("Oops, something went wrong.  Try again in a few seconds...")
        raise
    clean = getclean(exresults, count)
    if clean and len(clean) > 1:
        generate_choices(clean)
        reqinput(clean)
    if clean and len(clean) == 1:
        song = clean[0]
    if clean:
        show_song_meta(song)
        print("\nPlaying - press [%sq%s] to quit.." % (col, white))
        playsong(song)
        reqinput(clean)
    else:
        print("Nothing matched, sorry geeza")
main()
