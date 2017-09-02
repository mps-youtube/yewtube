import re
from datetime import datetime
import socket
import traceback
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from .. import player

try:
    # pylint: disable=F0401
    import pyperclip
    has_pyperclip = True

except ImportError:
    has_pyperclip = False

try:
    import readline
    has_readline = True
except ImportError:
    has_readline = False

import pafy

from .. import g, c, __version__, content, screen, cache
from .. import streams, history, config, util
from ..helptext import get_help
from ..content import generate_songlist_display, logo
from . import command
from .songlist import paginatesongs


@command(r'clearcache')
def clearcache():
    """ Clear cached items - for debugging use. """
    g.pafs = {}
    g.streams = {}
    util.dbg("%scache cleared%s", c.p, c.w)
    g.message = "cache cleared"


@command(r'(?:help|h)(?:\s+([-_a-zA-Z]+))?')
def show_help(choice):
    """ Print help message. """

    g.content = get_help(choice)


@command(r'(?:q|quit|exit)')
def quits(showlogo=True):
    """ Exit the program. """
    if has_readline:
        readline.write_history_file(g.READLINE_FILE)
        util.dbg("Saved history file")

    cache.save()

    screen.clear()
    msg = logo(c.r, version=__version__) if showlogo else ""
    msg += util.F("exitmsg", 2)

    if config.CHECKUPDATE.get and showlogo:

        try:
            url = "https://raw.githubusercontent.com/mps-youtube/mps-youtube/master/VERSION"
            v = urlopen(url, timeout=1).read().decode()
            v = re.search(r"^version\s*([\d\.]+)\s*$", v, re.MULTILINE)

            if v:
                v = v.group(1)

                if v > __version__:
                    msg += "\n\nA newer version is available (%s)\n" % v

        except (URLError, HTTPError, socket.timeout):
            util.dbg("check update timed out")

    screen.msgexit(msg)

def _format_comment(snippet, n, qnt, reply=False):
    poster = snippet.get('authorDisplayName')
    shortdate = util.yt_datetime(snippet.get('publishedAt', ''))[1]
    text = snippet.get('textDisplay', '')
    cid = ("%s%s/%s %s" % ('└── ' if reply else '', n, qnt, c.c("g", poster)))
    return ("%-39s %s\n" % (cid, shortdate)) + \
            c.c("y", text.strip()) + '\n\n'

def _fetch_commentreplies(parentid):
    return pafy.call_gdata('comments', {
        'parentId': parentid,
        'part': 'snippet',
        'textFormat': 'plainText',
        'maxResults': 50}).get('items', [])

def fetch_comments(item):
    """ Fetch comments for item using gdata. """
    # pylint: disable=R0912
    # pylint: disable=R0914
    ytid, title = item.ytid, item.title
    util.dbg("Fetching comments for %s", c.c("y", ytid))
    screen.writestatus("Fetching comments for %s" % c.c("y", title[:55]))
    qs = {'textFormat': 'plainText',
          'videoId': ytid,
          'maxResults': 50,
          'part': 'snippet'}

    jsdata = pafy.call_gdata('commentThreads', qs)

    coms = [x.get('snippet', {}) for x in jsdata.get('items', [])]

    # skip blanks
    coms = [x for x in coms
            if len(x.get('topLevelComment', {}).get('snippet', {}).get('textDisplay', '').strip())]

    if not len(coms):
        g.message = "No comments for %s" % item.title[:50]
        g.content = generate_songlist_display()
        return

    commentstext = ''

    for n, com in enumerate(coms, 1):
        snippet = com.get('topLevelComment', {}).get('snippet', {})
        commentstext += _format_comment(snippet, n, len(coms))
        if com.get('totalReplyCount') > 0:
            replies = _fetch_commentreplies(com.get('topLevelComment').get('id'))
            for n, com in enumerate(reversed(replies), 1):
                commentstext += _format_comment(com.get('snippet', {}),
                                                n, len(replies), True)

    g.current_page = 0
    g.content = content.StringContent(commentstext)


@command(r'c\s?(\d{1,4})')
def comments(number):
    """ Receive use request to view comments. """
    if g.browse_mode == "normal":
        item = g.model[int(number) - 1]
        fetch_comments(item)

    else:
        g.content = generate_songlist_display()
        g.message = "Comments only available for video items"


@command(r'x\s*(\d+)')
def clipcopy_video(num):
    """ Copy video/playlist url to clipboard. """
    if g.browse_mode == "ytpl":

        p = g.ytpls[int(num) - 1]
        link = "https://youtube.com/playlist?list=%s" % p['link']

    elif g.browse_mode == "normal":
        item = (g.model[int(num) - 1])
        link = "https://youtube.com/watch?v=%s" % item.ytid

    else:
        g.message = "clipboard copy not valid in this mode"
        g.content = generate_songlist_display()
        return

    if has_pyperclip:

        try:
            pyperclip.copy(link)
            g.message = c.y + link + c.w + " copied"
            g.content = generate_songlist_display()

        except Exception as e:
            g.content = generate_songlist_display()
            g.message = link + "\nError - couldn't copy to clipboard.\n" + \
                    ''.join(traceback.format_exception_only(type(e), e))

    else:
        g.message = "pyperclip module must be installed for clipboard support\n"
        g.message += "see https://pypi.python.org/pypi/pyperclip/"
        g.content = generate_songlist_display()


@command(r'X\s*(\d+)')
def clipcopy_stream(num):
    """ Copy content stream url to clipboard. """
    if g.browse_mode == "normal":

        item = (g.model[int(num) - 1])
        details = player.stream_details(item)[1]
        stream = details['url']

    else:
        g.message = "clipboard copy not valid in this mode"
        g.content = generate_songlist_display()
        return

    if has_pyperclip:

        try:
            pyperclip.copy(stream)
            g.message = c.y + stream + c.w + " copied"
            g.content = generate_songlist_display()

        except Exception as e:
            g.content = generate_songlist_display()
            g.message = stream + "\nError - couldn't copy to clipboard.\n" + \
                    ''.join(traceback.format_exception_only(type(e), e))

    else:
        g.message = "pyperclip module must be installed for clipboard support\n"
        g.message += "see https://pypi.python.org/pypi/pyperclip/"
        g.content = generate_songlist_display()


@command(r'i\s*(\d{1,4})')
def video_info(num):
    """ Get video information. """
    if g.browse_mode == "ytpl":
        p = g.ytpls[int(num) - 1]

        # fetch the playlist item as it has more metadata
        if p['link'] in g.pafy_pls:
            ytpl = g.pafy_pls[p['link']][0]
        else:
            g.content = logo(col=c.g)
            g.message = "Fetching playlist info.."
            screen.update()
            util.dbg("%sFetching playlist using pafy%s", c.y, c.w)
            ytpl = pafy.get_playlist2(p['link'])
            g.pafy_pls[p['link']] = (ytpl, util.IterSlicer(ytpl))

        ytpl_desc = ytpl.description
        g.content = generate_songlist_display()
        created = util.yt_datetime_local(p['created'])
        updated = util.yt_datetime_local(p['updated'])
        out = c.ul + "Playlist Info" + c.w + "\n\n"
        out += p['title']
        out += "\n" + ytpl_desc
        out += ("\n\nAuthor     : " + p['author'])
        out += "\nSize       : " + str(p['size']) + " videos"
        out += "\nCreated    : " + created[1] + " " + created[2]
        out += "\nUpdated    : " + updated[1] + " " + updated[2]
        out += "\nID         : " + str(p['link'])
        out += ("\n\n%s[%sPress enter to go back%s]%s" % (c.y, c.w, c.y, c.w))
        g.content = out

    elif g.browse_mode == "normal":
        g.content = logo(c.b)
        screen.update()
        screen.writestatus("Fetching video metadata..")
        item = (g.model[int(num) - 1])
        streams.get(item)
        p = util.get_pafy(item)
        pub = datetime.strptime(str(p.published), "%Y-%m-%d %H:%M:%S")
        pub = util.utc2local(pub)
        screen.writestatus("Fetched")
        out = c.ul + "Video Info" + c.w + "\n\n"
        out += p.title or ""
        out += "\n" + (p.description or "") + "\n"
        out += "\nAuthor     : " + str(p.author)
        out += "\nPublished  : " + pub.strftime("%c")
        out += "\nView count : " + str(p.viewcount)
        out += "\nRating     : " + str(p.rating)[:4]
        out += "\nLikes      : " + str(p.likes)
        out += "\nDislikes   : " + str(p.dislikes)
        out += "\nCategory   : " + str(p.category)
        out += "\nLink       : " + "https://youtube.com/watch?v=%s" % p.videoid
        out += "\n\n%s[%sPress enter to go back%s]%s" % (c.y, c.w, c.y, c.w)
        g.content = out


@command(r's\s*(\d{1,4})')
def stream_info(num):
    """ Get stream information. """
    if g.browse_mode == "normal":
        g.content = logo(c.b)
        screen.update()
        screen.writestatus("Fetching stream metadata..")
        item = (g.model[int(num) - 1])
        streams.get(item)
        p = util.get_pafy(item)
        setattr(p, 'ytid', p.videoid)
        details = player.stream_details(p)[1]
        screen.writestatus("Fetched")
        out = "\n\n" + c.ul + "Stream Info" + c.w + "\n"
        out += "\nExtension   : " + details['ext']
        out += "\nSize        : " + str(details['size'])
        out += "\nQuality     : " + details['quality']
        out += "\nRaw bitrate : " + str(details['rawbitrate'])
        out += "\nMedia type  : " + details['mtype']
        out += "\nLink        : " + details['url']
        out += "\n\n%s[%sPress enter to go back%s]%s" % (c.y, c.w, c.y, c.w)
        g.content = out


@command(r'history')
def view_history(duplicates=True):
    """ Display the user's play history """
    history = g.userhist.get('history')
    #g.last_opened = ""
    try:
        hist_list = list(reversed(history.songs))
        message = "Viewing play history"
        if not duplicates:
            # List unique elements and preserve order.
            seen = set()
            seen_add = seen.add  # it makes calls to add() faster
            hist_list = [x for x in hist_list if not (x in seen or seen_add(x))]
            message = "Viewing recent played songs"
        paginatesongs(hist_list)
        g.message = message

    except AttributeError:
        g.content = logo(c.r)
        g.message = "History empty"


@command(r'history recent')
def recent_history():
    """ Display the recent user's played songs """
    view_history(duplicates=False)


@command(r'history clear')
def clear_history():
    """ Clears the user's play history """
    g.userhist['history'].songs = []
    history.save()
    g.message = "History cleared"
    g.content = logo()


@command(r'history export')
def export_history():
    """ Export the user's play history to play_history.txt. """
    if 'history' in g.userhist:
        history.export()
        g.message = "History exported to: " + g.HISTFILE + ".txt"
    else:
        g.message = "No history to export."
    g.content = logo()
