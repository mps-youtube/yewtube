import re
import difflib
import time
import threading
from xml.etree import ElementTree as ET
from urllib.error import HTTPError, URLError
from urllib.request import build_opener

import mps_youtube as mpsyt
from mps_youtube import c, dbg

class AlbumSearchPlugin(mpsyt.Plugin):
    pass


@AlbumSearchPlugin.command(r'album\s*(.{0,500})', 'search',
        '{2}album <album title>{1} - '
        'Search for matching tracks using album title')
def search_album(term, page=0, splash=True):
    """Search for albums. """
    # pylint: disable=R0914,R0912
    if not term:
        show_message("Enter album name:", c.g, update=True)
        term = input("> ")

        if not term or len(term) < 2:
            g.message = c.r + "Not enough input!" + c.w
            g.content = generate_songlist_display()
            return

    album = _get_mb_album(term)

    if not album:
        show_message("Album '%s' not found!" % term)
        return

    out = "'%s' by %s%s%s\n\n" % (album['title'],
                                  c.g, album['artist'], c.w)
    out += ("[Enter] to continue, [q] to abort, or enter artist name for:\n"
            "    %s" % (c.y + term + c.w + "\n"))

    if splash:
        g.message, g.content = out, logo(c.b)
        screen_update()

    prompt = "Artist? [%s] > " % album['artist']
    xprint(prompt, end="")
    artistentry = input().strip()

    if artistentry:

        if artistentry == "q":
            show_message("Album search abandoned!")
            return

        album = _get_mb_album(term, artist=artistentry)

        if not album:
            show_message("Album '%s' by '%s' not found!" % (term, artistentry))
            return

    title, artist = album['title'], album['artist']
    mb_tracks = _get_mb_tracks(album['aid'])

    if not mb_tracks:
        show_message("Album '%s' by '%s' has 0 tracks!" % (title, artist))
        return

    msg = "%s%s%s by %s%s%s\n\n" % (c.g, title, c.w, c.g, artist, c.w)
    msg += "Enter to begin matching or [q] to abort"
    g.message = msg
    g.content = "Tracks:\n"
    for n, track in enumerate(mb_tracks, 1):
        g.content += "%02s  %s" % (n, track['title'])
        g.content += "\n"

    screen_update()
    entry = input("Continue? [Enter] > ")

    if entry == "":
        pass

    else:
        show_message("Album search abandoned!")
        return

    songs = []
    clear_screen()
    itt = _match_tracks(artist, title, mb_tracks)

    stash = Config.SEARCH_MUSIC.get, Config.ORDER.get
    Config.SEARCH_MUSIC.value = True
    Config.ORDER.value = "relevance"

    try:
        songs.extend(itt)

    except KeyboardInterrupt:
        xprint("%sHalted!%s" % (c.r, c.w))

    finally:
        Config.SEARCH_MUSIC.value, Config.ORDER.value = stash

    if songs:
        g.model.songs = songs
        kwa = {"song": songs[0], "delay": 0}
        t = threading.Thread(target=preload, kwargs=kwa)
        t.start()
        xprint("\n%s / %s songs matched" % (len(songs), len(mb_tracks)))
        input("Press Enter to continue")
        g.message = "Contents of album %s%s - %s%s %s(%d/%d)%s:" % (
            c.y, artist, title, c.w, c.b, len(songs), len(mb_tracks), c.w)
        g.last_opened = ""
        g.last_search_query = ""
        g.current_page = page
        g.result_count = len(songs)
        g.more_pages = False
        g.content = generate_songlist_display()

    else:
        g.message = "Found no album tracks for %s%s%s" % (c.y, title, c.w)
        g.content = generate_songlist_display()
        g.current_page = 0
        g.last_search_query = ""


def _do_query(url, query, err='query failed', report=False):
    """ Perform http request using mpsyt user agent header.

    if report is True, return whether response is from memo

    """
    # create url opener
    ua = "mps-youtube/%s ( %s )" % (mpsyt.__version__, mpsyt.__url__)
    mpsyt_opener = build_opener()
    mpsyt_opener.addheaders = [('User-agent', ua)]

    # convert query to sorted list of tuples (needed for consistent url_memo)
    query = [(k, query[k]) for k in sorted(query.keys())]
    url = "%s?%s" % (url, urlencode(query))

    try:
        wdata = mpsyt_opener.open(url).read().decode()

    except (URLError, HTTPError) as e:
        g.message = "%s: %s (%s)" % (err, e, url)
        g.content = logo(c.r)
        return None if not report else (None, False)

    return wdata if not report else (wdata, False)


def _best_song_match(songs, title, duration):
    """ Select best matching song based on title, length.

    Score from 0 to 1 where 1 is best.

    """
    # pylint: disable=R0914
    seqmatch = difflib.SequenceMatcher

    def variance(a, b):
        """ Return difference ratio. """
        return float(abs(a - b)) / max(a, b)

    candidates = []

    ignore = "music video lyrics new lyrics video audio".split()
    extra = "official original vevo".split()

    for song in songs:
        dur, tit = int(song.length), song.title
        dbg("Title: %s, Duration: %s", tit, dur)

        for word in extra:
            if word in tit.lower() and word not in title.lower():
                pattern = re.compile(word, re.I)
                tit = pattern.sub("", tit)

        for word in ignore:
            if word in tit.lower() and word not in title.lower():
                pattern = re.compile(word, re.I)
                tit = pattern.sub("", tit)

        replacechars = re.compile(r"[\]\[\)\(\-]")
        tit = replacechars.sub(" ", tit)
        multiple_spaces = re.compile(r"(\s)(\s*)")
        tit = multiple_spaces.sub(r"\1", tit)

        title_score = seqmatch(None, title.lower(), tit.lower()).ratio()
        duration_score = 1 - variance(duration, dur)
        dbg("Title score: %s, Duration score: %s", title_score,
            duration_score)

        # apply weightings
        score = duration_score * .5 + title_score * .5
        candidates.append((score, song))

    best_score, best_song = max(candidates, key=lambda x: x[0])
    percent_score = int(100 * best_score)
    return best_song, percent_score


def _match_tracks(artist, title, mb_tracks):
    """ Match list of tracks in mb_tracks by performing multiple searches. """
    # pylint: disable=R0914
    dbg("artists is %s", artist)
    dbg("title is %s", title)
    title_artist_str = c.g + title + c.w, c.g + artist + c.w
    xprint("\nSearching for %s by %s\n\n" % title_artist_str)

    def dtime(x):
        """ Format time to M:S. """
        return time.strftime('%M:%S', time.gmtime(int(x)))

    # do matching
    for track in mb_tracks:
        ttitle = track['title']
        length = track['length']
        xprint("Search :  %s%s - %s%s - %s" % (c.y, artist, ttitle, c.w,
                                               dtime(length)))
        q = "%s %s" % (artist, ttitle)
        w = q = ttitle if artist == "Various Artists" else q
        query = generate_search_qs(w, 0, result_count=50)
        dbg(query)
        have_results = _search(q, query, splash=False, pre_load=False)

        if not have_results:
            xprint(c.r + "Nothing matched :(\n" + c.w)
            continue

        results = g.model.songs
        s, score = _best_song_match(results, artist + " " + ttitle, length)
        cc = c.g if score > 85 else c.y
        cc = c.r if score < 75 else cc
        xprint("Matched:  %s%s%s - %s \n[%sMatch confidence: "
               "%s%s]\n" % (c.y, s.title, c.w, fmt_time(s.length),
                            cc, score, c.w))
        yield s


def _get_mb_tracks(albumid):
    """ Get track listing from MusicBraiz by album id. """
    ns = {'mb': 'http://musicbrainz.org/ns/mmd-2.0#'}
    url = "http://musicbrainz.org/ws/2/release/" + albumid
    query = {"inc": "recordings"}
    wdata = _do_query(url, query, err='album search error')

    if not wdata:
        return None

    root = ET.fromstring(wdata)
    tlist = root.find("./mb:release/mb:medium-list/mb:medium/mb:track-list",
                      namespaces=ns)
    mb_songs = tlist.findall("mb:track", namespaces=ns)
    tracks = []
    path = "./mb:recording/mb:"

    for track in mb_songs:

        try:
            title, length, rawlength = "unknown", 0, 0
            title = track.find(path + "title", namespaces=ns).text
            rawlength = track.find(path + "length", namespaces=ns).text
            length = int(round(float(rawlength) / 1000))

        except (ValueError, AttributeError):
            xprint("not found")

        tracks.append(dict(title=title, length=length, rawlength=rawlength))

    return tracks


def _get_mb_album(albumname, **kwa):
    """ Return artist, album title and track count from MusicBrainz. """
    url = "http://musicbrainz.org/ws/2/release/"
    qargs = dict(
        release='"%s"' % albumname,
        primarytype=kwa.get("primarytype", "album"),
        status=kwa.get("status", "official"))
    qargs.update({k: '"%s"' % v for k, v in kwa.items()})
    qargs = ["%s:%s" % item for item in qargs.items()]
    qargs = {"query": " AND ".join(qargs)}
    g.message = "Album search for '%s%s%s'" % (c.y, albumname, c.w)
    wdata = _do_query(url, qargs)

    if not wdata:
        return None

    ns = {'mb': 'http://musicbrainz.org/ns/mmd-2.0#'}
    root = ET.fromstring(wdata)
    rlist = root.find("mb:release-list", namespaces=ns)

    if int(rlist.get('count')) == 0:
        return None

    album = rlist.find("mb:release", namespaces=ns)
    artist = album.find("./mb:artist-credit/mb:name-credit/mb:artist",
                        namespaces=ns).find("mb:name", namespaces=ns).text
    title = album.find("mb:title", namespaces=ns).text
    aid = album.get('id')
    return dict(artist=artist, title=title, aid=aid)


def show_message(message, col=c.r, update=False):
    """ Show message using col, update screen if required. """
    g.content = generate_songlist_display()
    g.message = col + message + c.w

    if update:
        update()
