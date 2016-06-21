import math
import copy
import random

import pafy

from . import g, c, config, screen, streams
from .util import getxy, fmt_time, uea_pad, yt_datetime, F

# In the future, this could support more advanced features
class Content:
    pass


class PaginatedContent(Content):
    def getPage(self, page):
        raise NotImplementedError

    def numPages(self):
        raise NotImplementedError


class LineContent(PaginatedContent):
    def getPage(self, page):
        max_results = getxy().max_results
        s = page * max_results
        e = (page + 1) * max_results
        return self.get_text(s, e)

    def numPages(self):
        return math.ceil(self.get_count()/getxy().max_results)

    def get_text(self, s, e):
        raise NotImplementedError

    def get_count(self):
        raise NotImplementedError


class StringContent(LineContent):
    def __init__(self, string):
        self._lines = string.splitlines()

    def get_text(self, s, e):
        return '\n'.join(self._lines[s:e])

    def get_count(self):
        width = getxy().width
        count = sum(len(i) // width + 1 for i in self._lines)
        return count


class SearchList(LineContent):
    def __init__(self, items, length=None, msg=None, failmsg=None, loadmsg=None):
        self._items = items
        self._length = length
        if length is None:
            self._length = len(songs)
        self._msg = msg
        self._failmsg = failmsg
        self._loadmsg = loadmsg

    def get_text(self, s, e):
        screen.update(content=logo(col=c.b),
                message=(self._loadmsg or ''))

        if callable(self._items):
            items = self._items(s, e)
        else:
            items = self._items[s:e]

        if not items:
            g.message = self._failmsg or g.message
            return
        else:
            g.message = self._msg or g.message

        return self.display_items(items, s)

    def get_count(self):
        return self._length

    def display_items(self, startidx):
        raise NotImplementedError


class SongList(SearchList):
    def display_items(self, songs, startidx):
        # preload first result url
        streams.preload(songs[0], delay=0)

        return _generate_songlist_display(songs, startidx)


class PlistList(SearchList):
    def display_items(self, ytpls, startidx):
        return _generate_playlist_display(ytpls, startidx)


def page_msg(page=0):
    """ Format information about currently displayed page to a string. """
    if isinstance(g.content, PaginatedContent):
        page_count = g.content.numPages()
    else:
        page_count = 0

    if page_count > 1:
        pagemsg = "{}{}/{}{}"
        #start_index = max_results * g.current_page
        return pagemsg.format('<' if page > 0 else '[',
                              "%s%s%s" % (c.y, page+1, c.w),
                              page_count,
                              '>' if page + 1 < page_count else ']')
    return None


def _generate_songlist_display(songs, startidx, song=False, zeromsg=None):
    """ Generate list of choices from a song list."""
    # pylint: disable=R0914

    if not songs:
        g.message = zeromsg or "Enter /search-term to search or [h]elp"
        return logo(c.g) + "\n\n"

    have_meta = all(x.ytid in g.meta for x in songs)
    user_columns = _get_user_columns() if have_meta else []
    maxlength = max(x.length for x in songs)
    lengthsize = 8 if maxlength > 35999 else 7
    lengthsize = 5 if maxlength < 6000 else lengthsize
    reserved = 9 + lengthsize + len(user_columns)
    cw = getxy().width
    cw -= 1
    title_size = cw - sum(1 + x['size'] for x in user_columns) - reserved
    before = [{"name": "idx", "size": 3, "heading": "Num"},
              {"name": "title", "size": title_size, "heading": "Title"}]
    after = [{"name": "length", "size": lengthsize, "heading": "Time"}]
    columns = before + user_columns + after

    for n, column in enumerate(columns):
        column['idx'] = n
        column['sign'] = "-" if not column['name'] == "length" else ""

    fmt = ["%{}{}s  ".format(x['sign'], x['size']) for x in columns]
    fmtrow = fmt[0:1] + ["%s  "] + fmt[2:]
    fmt, fmtrow = "".join(fmt).strip(), "".join(fmtrow).strip()
    titles = tuple([x['heading'][:x['size']] for x in columns])
    hrow = c.ul + fmt % titles + c.w
    out = "\n" + hrow + "\n"

    for n, x in enumerate(songs, startidx):
        col = (c.r if n % 2 == 0 else c.p) if not song else c.b
        details = {'title': x.title, "length": fmt_time(x.length)}
        details = copy.copy(g.meta[x.ytid]) if have_meta else details
        otitle = details['title']
        details['idx'] = "%2d" % (n + 1)
        details['title'] = uea_pad(columns[1]['size'], otitle)
        cat = details.get('category') or '-'
        details['category'] = pafy.get_categoryname(cat)
        data = []

        for z in columns:
            fieldsize, field = z['size'], z['name']
            if len(details[field]) > fieldsize:
                details[field] = details[field][:fieldsize]

            data.append(details[field])

        line = fmtrow % tuple(data)
        col = col if not song or song != songs[n] else c.p
        line = col + line + c.w
        out += line + "\n"

    return out + "\n" * (5 - len(songs)) if not song else out


def _generate_playlist_display(ytpls, startidx):
    """ Generate list of playlists. """
    if not ytpls:
        g.message = c.r + "No playlists found!"
        return logo(c.g) + "\n\n"

    cw = getxy().width
    fmtrow = "%s%-5s %s %-12s %-8s  %-2s%s\n"
    fmthd = "%s%-5s %-{}s %-12s %-9s %-5s%s\n".format(cw - 36)
    head = (c.ul, "Item", "Playlist", "Author", "Updated", "Count", c.w)
    out = "\n" + fmthd % head

    for n, x in enumerate(ytpls, startidx):
        col = (c.g if n % 2 == 0 else c.w)
        length = x.get('size') or "?"
        length = "%4s" % length
        title = x.get('title') or "unknown"
        author = x.get('author') or "unknown"
        updated = yt_datetime(x.get('updated'))[1]
        title = uea_pad(cw - 36, title)
        out += (fmtrow % (col, str(n + 1), title, author[:12], updated, str(length), c.w))

    return out + "\n" * (5 - len(ytpls))


def _get_user_columns():
    """ Get columns from user config, return dict. """
    total_size = 0
    user_columns = config.COLUMNS.get
    user_columns = user_columns.replace(",", " ").split()

    defaults = {"views": dict(name="viewCount", size=4, heading="View"),
                "rating": dict(name="rating", size=4, heading="Rtng"),
                "comments": dict(name="commentCount", size=4, heading="Comm"),
                "date": dict(name="uploaded", size=8, heading="Date"),
                "user": dict(name="uploaderName", size=10, heading="User"),
                "likes": dict(name="likes", size=4, heading="Like"),
                "dislikes": dict(name="dislikes", size=4, heading="Dslk"),
                "category": dict(name="category", size=8, heading="Category")}

    ret = []
    for column in user_columns:
        namesize = column.split(":")
        name = namesize[0]

        if name in defaults:
            z = defaults[name]
            nm, sz, hd = z['name'], z['size'], z['heading']

            if len(namesize) == 2 and namesize[1].isdigit():
                sz = int(namesize[1])

            total_size += sz
            cw = getxy().width
            if total_size < cw - 18:
                ret.append(dict(name=nm, size=sz, heading=hd))

    return ret


def logo(col=None, version=""):
    """ Return text logo. """
    col = col if col else random.choice((c.g, c.r, c.y, c.b, c.p, c.w))
    logo_txt = r"""                                             _         _
 _ __ ___  _ __  ___       _   _  ___  _   _| |_ _   _| |__   ___
| '_ ` _ \| '_ \/ __|_____| | | |/ _ \| | | | __| | | | '_ \ / _ \
| | | | | | |_) \__ \_____| |_| | (_) | |_| | |_| |_| | |_) |  __/
|_| |_| |_| .__/|___/      \__, |\___/ \__,_|\__|\__,_|_.__/ \___|
          |_|              |___/"""
    version = " v" + version if version else ""
    logo_txt = col + logo_txt + c.w + version
    lines = logo_txt.split("\n")
    length = max(len(x) for x in lines)
    x, y, _ = getxy()
    indent = (x - length - 1) // 2
    newlines = (y - 12) // 2
    indent, newlines = (0 if x < 0 else x for x in (indent, newlines))
    lines = [" " * indent + l for l in lines]
    logo_txt = "\n".join(lines) + "\n" * newlines
    return "" if g.debug_mode else logo_txt


def playlists_display():
    """ Produce a list of all playlists. """
    if not g.userpl:
        g.message = F("no playlists")
        return generate_songlist_display() if g.model else (logo(c.y) + "\n\n")

    maxname = max(len(a) for a in g.userpl)
    out = "      {0}Local Playlists{1}\n".format(c.ul, c.w)
    start = "      "
    fmt = "%s%s%-3s %-" + str(maxname + 3) + "s%s %s%-7s%s %-5s%s"
    head = (start, c.b, "ID", "Name", c.b, c.b, "Count", c.b, "Duration", c.w)
    out += "\n" + fmt % head + "\n\n"

    for v, z in enumerate(sorted(g.userpl)):
        n, p = z, g.userpl[z]
        l = fmt % (start, c.g, v + 1, n, c.w, c.y, str(len(p)), c.y,
                   p.duration, c.w) + "\n"
        out += l

    return out
