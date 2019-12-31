import re

from .. import g, c, playlists, content, util
from ..playlist import Playlist
from . import command, WORD
from .songlist import paginatesongs, songlist_rm_add


@command(r'rmp\s*(\d+|%s)' % WORD, 'rmp')
def playlist_remove(name):
    """ Delete a saved playlist by name - or purge working playlist if *all."""
    if name.isdigit() or g.userpl.get(name):

        if name.isdigit():
            name = int(name) - 1
            name = sorted(g.userpl)[name]

        playlists.delete(name)
        g.message = "Deleted playlist %s%s%s" % (c.y, name, c.w)
        g.content = content.playlists_display()
        #playlists.save()

    else:
        g.message = util.F('pl not found advise ls') % name
        g.content = content.playlists_display()


@command(r'add\s*(-?\d[-,\d\s]{1,250})(%s)' % WORD, 'add')
def playlist_add(nums, playlist):
    """ Add selected song nums to saved playlist. """
    nums = util.parse_multi(nums)
    # Replacing spaces with hyphens before checking if playlist already exist.
    # See https://github.com/mps-youtube/mps-youtube/issues/1046.
    playlist = playlist.replace(" ", "-")

    if not g.userpl.get(playlist):
        g.userpl[playlist] = Playlist(playlist)

    for songnum in nums:
        g.userpl[playlist].songs.append(g.model[songnum - 1])
        dur = g.userpl[playlist].duration
        f = (len(nums), playlist, len(g.userpl[playlist]), dur)
        g.message = util.F('added to saved pl') % f

    if nums:
        playlists.save()

    g.content = content.generate_songlist_display()


@command(r'mv\s*(\d{1,3})\s*(%s)' % WORD, 'mv')
def playlist_rename_idx(_id, name):
    """ Rename a playlist by ID. """
    _id = int(_id) - 1
    playlist_rename(sorted(g.userpl)[_id] + " " + name)


@command(r'mv\s*(%s\s+%s)' % (WORD, WORD), 'mv')
def playlist_rename(playlists_):
    """ Rename a playlist using mv command. """
    # Deal with old playlist names that permitted spaces
    a, b = "", playlists_.split(" ")
    while a not in g.userpl:
        a = (a + " " + (b.pop(0))).strip()
        if not b and a not in g.userpl:
            g.message = util.F('no pl match for rename')
            g.content = g.content or content.playlists_display()
            return

    b = "-".join(b)
    g.userpl[b] = Playlist(b)
    g.userpl[b].songs = list(g.userpl[a].songs)
    playlist_remove(a)
    g.message = util.F('pl renamed') % (a, b)
    playlists.save()


@command(r'(rm|add)\s(?:\*|all)', 'rm', 'add')
def add_rm_all(action):
    """ Add all displayed songs to current playlist.

    remove all displayed songs from view.

    """
    if action == "rm":
        g.model.songs.clear()
        msg = c.b + "Cleared all songs" + c.w
        g.content = content.generate_songlist_display(zeromsg=msg)

    elif action == "add":
        size = len(g.model)
        songlist_rm_add("add", "-" + str(size))


@command(r'save', 'save')
def save_last():
    """ Save command with no playlist name. """
    if g.last_opened:
        open_save_view("save", g.last_opened)

    else:
        saveas = ""

        # save using artist name in postion 1
        if g.model:
            saveas = g.model[0].title[:18].strip()
            saveas = re.sub(r"[^-\w]", "-", saveas, flags=re.UNICODE)

        # loop to find next available name
        post = 0

        while g.userpl.get(saveas):
            post += 1
            saveas = g.model[0].title[:18].strip() + "-" + str(post)

        # Playlists are not allowed to start with a digit
        # TODO: Possibly change this, but ban purely numerical names
        saveas = saveas.lstrip("0123456789")

        open_save_view("save", saveas)


@command(r'(open|save|view)\s*(%s)' % WORD, 'open', 'save', 'view')
def open_save_view(action, name):
    """ Open, save or view a playlist by name.  Get closest name match. """
    name = name.replace(" ", "-")
    if action == "open" or action == "view":
        saved = g.userpl.get(name)

        if not saved:
            name = util.get_near_name(name, g.userpl)
            saved = g.userpl.get(name)

        elif action == "open":
            g.active.songs = list(saved.songs)
            g.last_opened = name
            msg = util.F("pl loaded") % name
            paginatesongs(g.active, msg=msg)

        elif action == "view":
            g.last_opened = ""
            msg = util.F("pl viewed") % name
            paginatesongs(list(saved.songs), msg=msg)

        elif not saved and action in "view open".split():
            g.message = util.F("pl not found") % name
            g.content = content.playlists_display()

    elif action == "save":
        if not g.model:
            g.message = "Nothing to save. " + util.F('advise search')
            g.content = content.generate_songlist_display()

        else:
            g.userpl[name] = Playlist(name, list(g.model.songs))
            g.message = util.F('pl saved') % name
            playlists.save()
            g.content = content.generate_songlist_display()


@command(r'(open|view)\s*(\d{1,4})', 'open', 'view')
def open_view_bynum(action, num):
    """ Open or view a saved playlist by number. """
    srt = sorted(g.userpl)
    name = srt[int(num) - 1]
    open_save_view(action, name)


@command(r'ls', 'ls')
def ls():
    """ List user saved playlists. """
    if not g.userpl:
        g.message = util.F('no playlists')
        g.content = g.content or \
                content.generate_songlist_display(zeromsg=g.message)

    else:
        g.content = content.playlists_display()
        g.message = util.F('pl help')


@command(r'vp', 'vp')
def vp():
    """ View current working playlist. """

    msg = util.F('current pl')
    txt = util.F('advise add') if g.model else util.F('advise search')
    failmsg = util.F('pl empty') + " " + txt

    paginatesongs(g.active, msg=msg, failmsg=failmsg)
