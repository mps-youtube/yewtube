import sys
import webbrowser
from urllib.error import HTTPError, URLError

from .. import g, c, streams, util, content
from . import command, WORD, RS
from .songlist import plist
from .search import yt_url
from ..player import play_range


@command(r'play\s+(%s|\d+)' % WORD)
def play_pl(name):
    """ Play a playlist by name. """
    if name.isdigit():
        name = int(name)
        name = sorted(g.userpl)[name - 1]

    saved = g.userpl.get(name)

    if not saved:
        name = util.get_near_name(name, g.userpl)
        saved = g.userpl.get(name)

    if saved:
        g.model.songs = list(saved.songs)
        play_all("", "", "")

    else:
        g.message = util.F("pl not found") % name
        g.content = content.playlists_display()


@command(r'(%s{0,3})([-,\d\s\[\]]{1,250})\s*(%s{0,3})$' %
        (RS, RS))
def play(pre, choice, post=""):
    """ Play choice.  Use repeat/random if appears in pre/post. """
    # pylint: disable=R0914
    # too many local variables

    if g.browse_mode == "ytpl":

        if choice.isdigit():
            return plist(g.ytpls[int(choice) - 1]['link'])
        else:
            g.message = "Invalid playlist selection: %s" % c.y + choice + c.w
            g.content = content.generate_songlist_display()
            return

    if not g.model:
        g.message = c.r + "There are no tracks to select" + c.w
        g.content = g.content or content.generate_songlist_display()

    else:
        shuffle = "shuffle" in pre + post
        repeat = "repeat" in pre + post
        novid = "-a" in pre + post
        fs = "-f" in pre + post
        nofs = "-w" in pre + post
        forcevid = "-v" in pre + post

        if ((novid and fs) or (novid and nofs) or (nofs and fs)
           or (novid and forcevid)):
            raise IOError("Conflicting override options specified")

        override = False
        override = "audio" if novid else override
        override = "fullscreen" if fs else override
        override = "window" if nofs else override

        if (not fs) and (not nofs):
            override = "forcevid" if forcevid else override

        selection = util.parse_multi(choice)
        songlist = [g.model[x - 1] for x in selection]

        # cache next result of displayed items
        # when selecting a single item
        if len(songlist) == 1:
            chosen = selection[0] - 1

            if len(g.model) > chosen + 1:
                streams.preload(g.model[chosen + 1], override=override)

        play_range(songlist, shuffle, repeat, override)
        g.content = content.generate_songlist_display()


@command(r'(%s{0,3})(?:\*|all)\s*(%s{0,3})' %
        (RS, RS))
def play_all(pre, choice, post=""):
    """ Play all tracks in model (last displayed). shuffle/repeat if req'd."""
    options = pre + choice + post
    play(options, "1-" + str(len(g.model)))


@command(r'playurl\s(.*[-_a-zA-Z0-9]{11}[^\s]*)(\s-(?:f|a|w))?')
def play_url(url, override):
    """ Open and play a youtube video url. """
    override = override if override else "_"
    g.browse_mode = "normal"
    yt_url(url, print_title=1)

    if len(g.model) == 1:
        play(override, "1", "_")

    if g.command_line:
        sys.exit()


@command(r'browserplay\s(\d{1,50})')
def browser_play(number):
    """Open a previously searched result in the browser."""
    if (len(g.model) == 0):
        g.message = c.r + "No previous search." + c.w
        g.content = content.logo(c.r)
        return

    try:
        index = int(number) - 1

        if (0 <= index < len(g.model)):
            base_url = "https://www.youtube.com/watch?v="
            video = g.model[index]
            url = base_url + video.ytid
            webbrowser.open(url)
            g.content = g.content or content.generate_songlist_display()

        else:
            g.message = c.r + "Out of range." + c.w
            g.content = g.content or content.generate_songlist_display()
            return

    except (HTTPError, URLError, Exception) as e:
        g.message = c.r + str(e) + c.w
        g.content = g.content or content.generate_songlist_display()
        return
