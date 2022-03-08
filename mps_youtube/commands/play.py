import random
import sys
import typing as T
import webbrowser
from urllib.error import HTTPError, URLError

from .. import c, config, content, g, streams, util
from . import RS, WORD, command
from .search import related, yt_url
from .songlist import plist


@command(r'play\s+(%s|\d+)' % WORD, 'play')
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

    # Im just highjacking this if g.content is a
    # content.Content class
    if isinstance(g.content, content.Content):
        play_call = getattr(g.content, "_play", None)
        if callable(play_call):
            play_call(pre, choice, post)
        return

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

        if g.scrobble:
            old_queue = g.scrobble_queue
            g.scrobble_queue = [g.scrobble_queue[x - 1] for x in selection]

        try:
            if not config.PLAYER.get or not util.has_exefile(config.PLAYER.get):
                g.message = "Player not configured! Enter %sset player <player_app> "\
                            "%s to set a player" % (c.g, c.w)
                return
            g.PLAYER_OBJ.play(songlist, shuffle, repeat, override)
        except KeyboardInterrupt:
            return
        finally:
            g.content = content.generate_songlist_display()

        if g.scrobble:
            g.scrobble_queue = old_queue

        if config.AUTOPLAY.get:
            related(selection.pop())
            play(pre, str(random.randint(1, 15)), post="")


@command(r'(%s{0,3})(?:\*|all)\s*(%s{0,3})' %
        (RS, RS))
def play_all(pre, choice, post=""):
    """ Play all tracks in model (last displayed). shuffle/repeat if req'd."""
    options = pre + choice + post
    play(options, "1-" + str(len(g.model)))


@command(r'playurl\s(.*[-_a-zA-Z0-9]{11}[^\s]*)(\s-(?:f|a|w))?', 'playurl')
def play_url(url: str, override: T.Any):
    """Open and play a youtube video url.

    Args:
        url: url to be played
        override: override

    Raises:
        SystemExit: If run from command line
    """
    # @fixme check override type hint
    override = override if override else "_"
    g.browse_mode = "normal"
    yt_url(url, print_title=True)

    if len(g.model) == 1:
        play(override, "1", "_")

    if g.command_line:
        sys.exit()


@command(r'browserplay\s(\d{1,50})', 'browserplay')
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
