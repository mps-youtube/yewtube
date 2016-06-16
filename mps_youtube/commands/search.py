import re
import json
import math
import base64
import logging

import pafy

from .. import g, c, screen, config, util, content
from ..playlist import Video
from . import command
from .songlist import plist, paginatesongs


ISO8601_TIMEDUR_EX = re.compile(r'PT((\d{1,3})H)?((\d{1,3})M)?((\d{1,2})S)?')


def _search(progtext, qs=None, msg=None, failmsg=None):
    """ Perform memoized url fetch, display progtext. """
    
    loadmsg = "Searching for '%s%s%s'" % (c.y, progtext, c.w)

    wdata = pafy.call_gdata('search', qs)

    def iter_songs():
        wdata2 = wdata
        while True:
            for song in get_tracks_from_json(wdata2):
                yield song

            if not wdata2.get('nextPageToken'):
                break
            qs['pageToken'] = wdata2['nextPageToken']
            wdata2 = pafy.call_gdata('search', qs)

    # The youtube search api returns a maximum of 500 results
    length = min(wdata['pageInfo']['totalResults'], 500)
    slicer = util.IterSlicer(iter_songs(), length)

    paginatesongs(slicer, length=length, msg=msg, failmsg=failmsg,
            loadmsg=loadmsg)


def token(page):
    """ Returns a page token for a given start index. """
    index = (page or 0) * util.getxy().max_results
    k = index//128 - 1
    index -= 128 * k
    f = [8, index]
    if k > 0 or index > 127:
        f.append(k+1)
    f += [16, 0]
    b64 = base64.b64encode(bytes(f)).decode('utf8')
    return b64.strip('=')


def generate_search_qs(term, match='term'):
    """ Return query string. """

    aliases = dict(views='viewCount')
    qs = {
        'q': term,
        'maxResults': 50,
        'safeSearch': "none",
        'order': aliases.get(config.ORDER.get, config.ORDER.get),
        'part': 'id,snippet',
        'type': 'video',
        'key': config.API_KEY.get
    }

    if match == 'related':
        qs['relatedToVideoId'] = term
        del qs['q']

    if config.SEARCH_MUSIC.get:
        qs['videoCategoryId'] = 10

    return qs


def userdata_cached(userterm):
    """ Check if user name search term found in cache """
    userterm = ''.join([t.strip().lower() for t in userterm.split(' ')])
    return g.username_query_cache.get(userterm)


def cache_userdata(userterm, username, channel_id):
    """ Cache user name and channel id tuple """
    userterm = ''.join([t.strip().lower() for t in userterm.split(' ')])
    g.username_query_cache[userterm] = (username, channel_id)
    util.dbg('Cache data for username search query "{}": {} ({})'.format(
        userterm, username, channel_id))

    while len(g.username_query_cache) > 300:
        g.username_query_cache.popitem(last=False)
    return (username, channel_id)


def channelfromname(user):
    """ Query channel id from username. """

    cached = userdata_cached(user)
    if cached:
        user, channel_id = cached
    else:
        # if the user is looked for by their display name,
        # we have to sent an additional request to find their
        # channel id
        qs = {'part': 'id,snippet',
              'maxResults': 1,
              'q': user,
              'type': 'channel'}

        try:
            userinfo = pafy.call_gdata('search', qs)['items']
            if len(userinfo) > 0:
                snippet = userinfo[0].get('snippet', {})
                channel_id = snippet.get('channelId', user)
                username = snippet.get('title', user)
                user = cache_userdata(user, username, channel_id)[0]
            else:
                g.message = "User {} not found.".format(c.y + user + c.w)
                return

        except pafy.GdataError as e:
            g.message = "Could not retrieve information for user {}\n{}".format(
                c.y + user + c.w, e)
            util.dbg('Error during channel request for user {}:\n{}'.format(
                user, e))
            return

    # at this point, we know the channel id associated to a user name
    return (user, channel_id)


@command(r'user\s+(.+)')
def usersearch(q_user, identify='forUsername'):
    """ Fetch uploads by a YouTube user. """

    user, _, term = (x.strip() for x in q_user.partition("/"))
    if identify == 'forUsername':
        ret = channelfromname(user)
        if not ret: # Error
            return
        user, channel_id = ret

    else:
        channel_id = user

    # at this point, we know the channel id associated to a user name
    usersearch_id(user, channel_id, term)


def usersearch_id(user, channel_id, term):
    """ Performs a search within a user's (i.e. a channel's) uploads
    for an optional search term with the user (i.e. the channel)
    identified by its ID """

    query = generate_search_qs(term)
    aliases = dict(views='viewCount')  # The value of the config item is 'views' not 'viewCount'
    if config.USER_ORDER.get:
        query['order'] = aliases.get(config.USER_ORDER.get,
                config.USER_ORDER.get)
    query['channelId'] = channel_id

    termuser = tuple([c.y + x + c.w for x in (term, user)])
    if term:
        msg = "Results for {1}{3}{0} (by {2}{4}{0})"
        progtext = "%s by %s" % termuser
        failmsg = "No matching results for %s (by %s)" % termuser
    else:
        msg = "Video uploads by {2}{4}{0}"
        progtext = termuser[1]
        if config.SEARCH_MUSIC:
            failmsg = """User %s not found or has no videos in the Music category.
Use 'set search_music False' to show results not in the Music category.""" % termuser[1]
        else:
            failmsg = "User %s not found or has no videos."  % termuser[1]
    msg = str(msg).format(c.w, c.y, c.y, term, user)

    _search(progtext, query, msg, failmsg)


def related_search(vitem):
    """ Fetch uploads by a YouTube user. """
    query = generate_search_qs(vitem.ytid, match='related')

    if query.get('videoCategoryId'):
        del query['videoCategoryId']

    t = vitem.title
    ttitle = t[:48].strip() + ".." if len(t) > 49 else t

    msg = "Videos related to %s%s%s" % (c.y, ttitle, c.w)
    failmsg = "Related to %s%s%s not found" % (c.y, vitem.ytid, c.w)
    _search(ttitle, query, msg, failmsg)


# Note: [^./] is to prevent overlap with playlist search command
@command(r'(?:search|\.|/)\s*([^./].{1,500})')
def search(term):
    """ Perform search. """
    if not term or len(term) < 2:
        g.message = c.r + "Not enough input" + c.w
        g.content = content.generate_songlist_display()
        return

    logging.info("search for %s", term)
    query = generate_search_qs(term)
    msg = "Search results for %s%s%s" % (c.y, term, c.w)
    failmsg = "Found nothing for %s%s%s" % (c.y, term, c.w)
    _search(term, query, msg, failmsg)


@command(r'u(?:ser)?pl\s(.*)')
def user_pls(user):
    """ Retrieve user playlists. """
    return pl_search(user, is_user=True)


@command(r'(?:\.\.|\/\/|pls(?:earch)?\s)\s*(.*)')
def pl_search(term, page=0, splash=True, is_user=False):
    """ Search for YouTube playlists.

    term can be query str or dict indicating user playlist search.

    """
    if not term or len(term) < 2:
        g.message = c.r + "Not enough input" + c.w
        g.content = content.generate_songlist_display()
        return

    if splash:
        g.content = content.logo(c.g)
        prog = "user: " + term if is_user else term
        g.message = "Searching playlists for %s" % c.y + prog + c.w
        screen.update()

    if is_user:
        ret = channelfromname(term)
        if not ret: # Error
            return
        user, channel_id = ret

    else:
        # playlist search is done with the above url and param type=playlist
        logging.info("playlist search for %s", prog)
        qs = generate_search_qs(term)
        qs['pageToken'] = token(page)
        qs['type'] = 'playlist'
        if 'videoCategoryId' in qs:
            del qs['videoCategoryId'] # Incompatable with type=playlist

        pldata = pafy.call_gdata('search', qs)
        id_list = [i.get('id', {}).get('playlistId')
                    for i in pldata.get('items', ())]

        result_count = min(pldata['pageInfo']['totalResults'], 500)

    qs = {'part': 'contentDetails,snippet',
          'maxResults': 50}

    if is_user:
        if page:
            qs['pageToken'] = token(page)
        qs['channelId'] = channel_id
    else:
        qs['id'] = ','.join(id_list)

    pldata = pafy.call_gdata('playlists', qs)
    playlists = get_pl_from_json(pldata)[:util.getxy().max_results]

    if is_user:
        result_count = pldata['pageInfo']['totalResults']

    if playlists:
        g.last_search_query = (pl_search, {"term": term, "is_user": is_user})
        g.browse_mode = "ytpl"
        g.current_page = page
        g.result_count = result_count
        g.ytpls = playlists
        g.message = "Playlist results for %s" % c.y + prog + c.w
        g.content = content.generate_playlist_display()

    else:
        g.message = "No playlists found for: %s" % c.y + prog + c.w
        g.current_page = 0
        g.content = content.generate_songlist_display(zeromsg=g.message)


def get_pl_from_json(pldata):
    """ Process json playlist data. """

    try:
        items = pldata['items']

    except KeyError:
        items = []

    results = []

    for item in items:
        snippet = item['snippet']
        results.append(dict(
            link=item["id"],
            size=item["contentDetails"]["itemCount"],
            title=snippet["title"],
            author=snippet["channelTitle"],
            created=snippet["publishedAt"],
            updated=snippet['publishedAt'], #XXX Not available in API?
            description=snippet["description"]))

    return results


def get_track_id_from_json(item):
    """ Try to extract video Id from various response types """
    fields = ['contentDetails/videoId',
              'snippet/resourceId/videoId',
              'id/videoId',
              'id']
    for field in fields:
        node = item
        for p in field.split('/'):
            if node and isinstance(node, dict):
                node = node.get(p)
        if node:
            return node
    return ''


def get_tracks_from_json(jsons):
    """ Get search results from API response """

    items = jsons.get("items")
    if not items:
        util.dbg("got unexpected data or no search results")
        return ()

    # fetch detailed information about items from videos API
    qs = {'part':'contentDetails,statistics,snippet',
          'id': ','.join([get_track_id_from_json(i) for i in items])}

    wdata = pafy.call_gdata('videos', qs)

    items_vidinfo = wdata.get('items', [])
    # enhance search results by adding information from videos API response
    for searchresult, vidinfoitem in zip(items, items_vidinfo):
        searchresult.update(vidinfoitem)

    # populate list of video objects
    songs = []
    for item in items:

        try:

            ytid = get_track_id_from_json(item)
            duration = item.get('contentDetails', {}).get('duration')

            if duration:
                duration = ISO8601_TIMEDUR_EX.findall(duration)
                if len(duration) > 0:
                    _, hours, _, minutes, _, seconds = duration[0]
                    duration = [seconds, minutes, hours]
                    duration = [int(v) if len(v) > 0 else 0 for v in duration]
                    duration = sum([60**p*v for p, v in enumerate(duration)])
                else:
                    duration = 30
            else:
                duration = 30

            stats = item.get('statistics', {})
            snippet = item.get('snippet', {})
            title = snippet.get('title', '').strip()
            # instantiate video representation in local model
            cursong = Video(ytid=ytid, title=title, length=duration)
            likes = int(stats.get('likeCount', 0))
            dislikes = int(stats.get('dislikeCount', 0))
            #XXX this is a very poor attempt to calculate a rating value
            rating = 5.*likes/(likes+dislikes) if (likes+dislikes) > 0 else 0
            category = snippet.get('categoryId')

            # cache video information in custom global variable store
            g.meta[ytid] = dict(
                # tries to get localized title first, fallback to normal title
                title=snippet.get('localized',
                                  {'title':snippet.get('title',
                                                       '[!!!]')}).get('title',
                                                                      '[!]'),
                length=str(util.fmt_time(cursong.length)),
                rating=str('{}'.format(rating))[:4].ljust(4, "0"),
                uploader=snippet.get('channelId'),
                uploaderName=snippet.get('channelTitle'),
                category=category,
                aspect="custom", #XXX
                uploaded=util.yt_datetime(snippet.get('publishedAt', ''))[1],
                likes=str(num_repr(likes)),
                dislikes=str(num_repr(dislikes)),
                commentCount=str(num_repr(int(stats.get('commentCount', 0)))),
                viewCount=str(num_repr(int(stats.get('viewCount', 0)))))

        except Exception as e:

            util.dbg(json.dumps(item, indent=2))
            util.dbg('Error during metadata extraction/instantiation of ' +
                'search result {}\n{}'.format(ytid, e))

        songs.append(cursong)

    # return video objects
    return songs


def num_repr(num):
    """ Return up to four digit string representation of a number, eg 2.6m. """
    if num <= 9999:
        return str(num)

    def digit_count(x):
        """ Return number of digits. """
        return int(math.floor(math.log10(x)) + 1)

    digits = digit_count(num)
    sig = 3 if digits % 3 == 0 else 2
    rounded = int(round(num, int(sig - digits)))
    digits = digit_count(rounded)
    suffix = "_kmBTqXYX"[(digits - 1) // 3]
    front = 3 if digits % 3 == 0 else digits % 3

    if not front == 1:
        return str(rounded)[0:front] + suffix

    return str(rounded)[0] + "." + str(rounded)[1] + suffix


@command(r'u\s?([\d]{1,4})')
def user_more(num):
    """ Show more videos from user of vid num. """
    if g.browse_mode != "normal":
        g.message = "User uploads must refer to a specific video item"
        g.message = c.y + g.message + c.w
        g.content = content.generate_songlist_display()
        return

    g.current_page = 0
    item = g.model[int(num) - 1]

    #TODO: Cleaner way of doing this?
    if item.ytid in g.meta:
        channel_id = g.meta.get(item.ytid, {}).get('uploader')
        user = g.meta.get(item.ytid, {}).get('uploaderName')
    else:
        paf = util.get_pafy(item)
        user, channel_id = channelfromname(paf.author)

    usersearch_id(user, channel_id, '')


@command(r'r\s?(\d{1,4})')
def related(num):
    """ Show videos related to to vid num. """
    if g.browse_mode != "normal":
        g.message = "Related items must refer to a specific video item"
        g.message = c.y + g.message + c.w
        g.content = content.generate_songlist_display()
        return

    g.current_page = 0
    item = g.model[int(num) - 1]
    related_search(item)


@command(r'mix\s*(\d{1,4})')
def mix(num):
    """ Retrieves the YouTube mix for the selected video. """
    g.content = g.content or content.generate_songlist_display()
    if g.browse_mode != "normal":
        g.message = util.F('mix only videos')
    else:
        item = (g.model[int(num) - 1])
        if item is None:
            g.message = util.F('invalid item')
            return
        item = util.get_pafy(item)
        # Mix playlists are made up of 'RD' + video_id
        try:
            plist("RD" + item.videoid)
        except OSError:
            g.message = util.F('no mix')


@command(r'url\s(.*[-_a-zA-Z0-9]{11}.*)')
def yt_url(url, print_title=0):
    """ Acess videos by urls. """
    url_list = url.split()

    g.model.songs = []

    for u in url_list:
        try:
            p = util.get_pafy(u)

        except (IOError, ValueError) as e:
            g.message = c.r + str(e) + c.w
            g.content = g.content or content.generate_songlist_display(
                    zeromsg=g.message)
            return

        g.browse_mode = "normal"
        v = Video(p.videoid, p.title, p.length)
        g.model.songs.append(v)

    if not g.command_line:
        g.content = content.generate_songlist_display()

    if print_title:
        util.xprint(v.title)


@command(r'url_file\s(\S+)')
def yt_url_file(file_name):
    """ Access a list of urls in a text file """

    #Open and read the file
    try:
        with open(file_name, "r") as fo:
            output = ' '.join([line.strip() for line in fo if line.strip()])

    except (IOError):
        g.message = c.r + 'Error while opening the file, check the validity of the path' + c.w
        g.content = g.content or content.generate_songlist_display(
                zeromsg=g.message)
        return

    #Finally pass the input to yt_url
    yt_url(output)
