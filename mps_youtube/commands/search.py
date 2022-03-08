import base64
import json
import logging
import math
import re
import typing as T
from argparse import ArgumentParser
from datetime import datetime, timedelta
from urllib import parse

from .. import pafy

parser = ArgumentParser()
parser.add_argument('-d', '--duration', choices=('any', 'short', 'medium', 'long'))
parser.add_argument('-a', '--after')
parser.add_argument('-l', '--live', nargs="?", const=True)
parser.add_argument('-c', '--category', nargs=1)
parser.add_argument('search', nargs='+')


from .. import c, config, content, contentquery, g, listview, screen, util
from ..playlist import Playlist, Video
from . import command
from .songlist import paginatesongs, plist

ISO8601_TIMEDUR_EX = re.compile(r'PT((\d{1,3})H)?((\d{1,3})M)?((\d{1,2})S)?')

DAYS = dict(day = 1,
            week = 7,
            month = 30,
            year = 365)


def _display_search_results(progtext, wdata, msg=None, failmsg=None):
    """ Perform memoized url fetch, display progtext. """

    loadmsg = "Searching for '%s%s%s'" % (c.y, progtext, c.w)

    def iter_songs():
        wdata2 = wdata
        while True:
            for song in get_tracks_from_json(wdata2):
                yield song

            if type(wdata2) is list or not wdata2.get('nextPageToken'):
                break
            query = None#wdata2['nextPageToken']
            wdata2 = None#pafy.call_gdata('search', qs)

    # The youtube search api returns a maximum of 500 results
    length = len(wdata)
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


# def generate_search_qs(term, match='term', videoDuration='any', after=None, category=None, is_live=False):
#     """ Return query string. """
#
#     aliases = dict(views='viewCount')
#     qs = {
#         'q': term,
#         'maxResults': 50,
#         'safeSearch': "none",
#         'order': aliases.get(config.ORDER.get, config.ORDER.get),
#         'part': 'id,snippet',
#         'type': 'video',
#         'videoDuration': videoDuration
#         #,'key': config.API_KEY.get
#     }
#
#     if after:
#         after = after.lower()
#         qs['publishedAfter'] = '%sZ' % (datetime.utcnow() - timedelta(days=DAYS[after])).isoformat() \
#                                 if after in DAYS.keys() else '%s%s' % (after, 'T00:00:00Z' * (len(after) == 10))
#
#     if match == 'related':
#         qs['relatedToVideoId'] = term
#         del qs['q']
#
#     if config.SEARCH_MUSIC.get:
#         qs['videoCategoryId'] = 10
#
#     if category:
#         qs['videoCategoryId'] = category
#
#     if is_live:
#         qs['eventType'] = "live"
#
#     return qs


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
        return cached

    try:
        channel_id, channel_name = pafy.channel_id_from_name(user)
        return cache_userdata(user, channel_name, channel_id)

    except Exception as e:
        import traceback
        traceback.print_exception(type(e), e, e.__traceback__)
        g.message = "Could not retrieve information for user {}\n{}".format(
            c.y + user + c.w, e)
        util.dbg('Error during channel request for user {}:\n{}'.format(
            user, e))

    # at this point, we know the channel id associated to a user name
    return None


@command(r'channels\s+(.+)')
def channelsearch(q_user):

    # qs = {'part': 'id,snippet',
    #       'q': q_user,
    #       'maxResults': 50,
    #       'type': 'channel',
    #       'order': "relevance"
    #       }

    QueryObj = contentquery.ContentQuery(listview.ListUser, 'search', q_user)
    columns = [
        {"name": "idx", "size": 3, "heading": "Num"},
        {"name": "name", "size": 30, "heading": "Username"},
        {"name": "description", "size": "remaining", "heading": "Description"},
        ]

    def run_m(user_id):
        """ Search ! """
        usersearch_id(*(user_id[0]))
    del g.content

    g.content = listview.ListView(columns, QueryObj, run_m)
    g.message = "Results for channel search: '%s'" % q_user


@command(r'user\s+(.+)', 'user')
def usersearch(q_user, identify='forUsername'):
    """ Fetch uploads by a YouTube user. """

    user, _, term = (x.strip() for x in q_user.partition("/"))
    if identify == 'forUsername':
        ret = channelfromname(user)
        if not ret:  # Error
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

    #query = generate_search_qs(term)
    aliases = dict(views='viewCount')  # The value of the config item is 'views' not 'viewCount'
    if config.USER_ORDER.get:
        pass
        #query['order'] = aliases.get(config.USER_ORDER.get,
        #        config.USER_ORDER.get)
    #query['channelId'] = channel_id

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
    results = pafy.all_videos_from_channel(channel_id)
    _display_search_results(progtext, results, msg, failmsg)


def related_search(vitem):
    """ Fetch videos related to vitem
    vitem = {'description': str, 'length': int, 'title': str, 'ytid': str}
    """

    t = vitem.title
    ttitle = t[:48].strip() + ".." if len(t) > 49 else t

    msg = "Videos related to %s%s%s" % (c.y, ttitle, c.w)
    failmsg = "Related to %s%s%s not found" % (c.y, vitem.ytid, c.w)

    # todo: implement realted search in pafy
    #_search(ttitle, vitem.title, msg, failmsg)


# Livestream category search
@command(r'live\s+(.+)', 'live')
def livestream_category_search(term):
    sel_category = g.categories.get(term, None)

    if not sel_category:
        g.message = ("That is not a valid category. Valid categories are: ")
        g.message += (", ".join(g.categories.keys()))
        return

    query = {
        "part": "id,snippet",
        "eventType": "live",
        "maxResults": 50,
        "type": "video",
        "videoCategoryId": sel_category
    }

    query_obj = contentquery.ContentQuery(listview.ListLiveStream, 'search', query)
    columns = [
              {"name": "idx", "size": 3, "heading": "Num"},
              {"name": "title", "size": 40, "heading": "Title"},
              {"name": "description", "size": "remaining", "heading": "Description"},
              ]

    def start_stream(returned):
        songs = Playlist("Search Results", [Video(*x) for x in returned])
        if not config.PLAYER.get or not util.has_exefile(config.PLAYER.get):
            g.message = "Player not configured! Enter %sset player <player_app> "\
                        "%s to set a player" % (c.g, c.w)
            return
        g.PLAYER_OBJ.play(songs, False, False, False)

    g.content = listview.ListView(columns, query_obj, start_stream)
    g.message = "Livestreams in category: '%s'" % term


# Note: [^./] is to prevent overlap with playlist search command
@command(r'(?:search|\.|/)\s*([^./].{1,500})', 'search')
def search(term):
    """ Perform search. """
    try:  # TODO make use of unknowns
        args, unknown = parser.parse_known_args(term.split())
        video_duration = args.duration if args.duration else 'any'
        if args.category:
            if not args.category[0].isdigit():
                args.category = g.categories.get(args.category[0])
            else:
                args.category = "".join(args.category)
        after = args.after
        term = ' '.join(args.search)
    except SystemExit:  # <------ argsparse calls exit()
        g.message = c.b + "Bad syntax. Enter h for help" + c.w
        return

    if not term or len(term) < 2:
        g.message = c.r + "Not enough input" + c.w
        g.content = content.generate_songlist_display()
        return

    logging.info("search for %s", term)
    #query = generate_search_qs(term, videoDuration=video_duration, after=after, category=args.category, is_live=args.live)

    msg = "Search results for %s%s%s" % (c.y, term, c.w)
    failmsg = "Found nothing for %s%s%s" % (c.y, term, c.w)
    wdata = pafy.search_videos(term, int(config.PAGES.get))
    _display_search_results(term, wdata, msg, failmsg)


@command(r'u(?:ser)?pl\s(.*)', 'userpl', 'upl')
def user_pls(user):
    """ Retrieve user playlists. """
    return usersearch_id(user, pafy.channel_id_from_name(user)[0], '')#pl_search(user, is_user=True)


@command(r'(?:\.\.|\/\/|pls(?:earch)?\s)\s*(.*)', 'plsearch')
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
        # qs = generate_search_qs(term)
        # qs['pageToken'] = token(page)
        # qs['type'] = 'playlist'
        # if 'videoCategoryId' in qs:
        #     del qs['videoCategoryId'] # Incompatable with type=playlist

        pldata = pafy.playlist_search(term)

        #id_list = [i.get('id', {}) for i in pldata]

        result_count = len(pldata)

    #todo: what is the purpose of this code? #qs = {'part': 'contentDetails,snippet','maxResults': 50}
    if is_user:
        if page:
            pass #qs['pageToken'] = token(page)
        pass #qs['channelId'] = channel_id
    else:
        pass #qs['id'] = ','.join(id_list)

    pldata = pafy.playlist_search(term)
    playlists = get_pl_from_json(pldata)[:util.getxy().max_results]

    # if is_user:
    #     result_count = pldata['pageInfo']['totalResults']

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
        items = pldata

    except KeyError:
        items = []

    results = []

    for item in items:
        results.append(dict(
            link=item["id"],
            size=item["videoCount"],
            title=item["title"],
            author=item['channel']["name"],
            created=item.get("publishedAt"),
            updated=item.get('publishedAt'), #XXX Not available in API?
            description=item.get("description")))

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

    if len(jsons) == 0:
        util.dbg("got unexpected data or no search results")
        return ()

    # populate list of video objects
    songs = []
    for item in jsons:
        try:
            ytid = get_track_id_from_json(item)
            duration = util.parse_video_length(item.get('duration'))
            #stats = item.get('statistics', {})
            #snippet = item.get('snippet', {})
            title = item.get('title', '').strip()
            # instantiate video representation in local model
            cursong = Video(ytid=ytid, title=title, length=duration)
            dislike_data = {'likes': 0, 'dislikes':0, 'rating':0}#pafy.return_dislikes(ytid)
            likes = int(dislike_data['likes'])
            dislikes = int(dislike_data['dislikes'])
            # this is a very poor attempt to calculate a rating value
            rating = int(dislike_data['rating'])#5.*likes/(likes+dislikes) if (likes+dislikes) > 0 else 0
            category = '?'#snippet.get('categoryId')
            publishedlocaldatetime = item.get('publishedTime','?')#util.yt_datetime_local(snippet.get('publishedAt', ''))

            # cache video information in custom global variable store
            g.meta[ytid] = dict(
                # tries to get localized title first, fallback to normal title
                title=title,
                length=str(util.fmt_time(cursong.length)),
                rating=rating,#str('{}'.format(rating))[:4].ljust(4, "0"),
                uploader=item['channel']['id'],
                uploaderName=item['channel']['name'],
                category=category,
                aspect="custom", #XXX
                uploaded=publishedlocaldatetime,#publishedlocaldatetime[1] if publishedlocaldatetime is not None else None,
                uploadedTime=publishedlocaldatetime,#,publishedlocaldatetime[2] if publishedlocaldatetime is not None else None,
                likes=str(num_repr(likes)),
                dislikes=str(num_repr(dislikes)),
                commentCount='?',#str(num_repr(int(stats.get('commentCount', 0)))),
                viewCount= item['viewCount']['text'] if 'viewCount' in item.keys() else '?')#str(num_repr(int(stats.get('viewCount', 0)))))
            songs.append(cursong)

        except Exception as e:
            import traceback
            traceback.print_exception(type(e), e, e.__traceback__)
            input('Press any key to continue...')
            util.dbg(json.dumps(item, indent=2))
            util.dbg('Error during metadata extraction/instantiation of ' +
                'search result {}\n{}'.format(ytid, e))



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


@command(r'u\s?([\d]{1,4})', 'u')
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


@command(r'r\s?(\d{1,4})', 'r')
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


@command(r'mix\s*(\d{1,4})', 'mix')
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


@command(r"url\s(.*[-_a-zA-Z0-9]{11}.*)", "url")
def yt_url(url: str, print_title: bool = False):
    """
    Acess videos by urls.

    If `print_title` is true only last title from unique parsed id will be printed.

    If for example `vid1` and `vid2` have title `title1` and `title2`, respectively,
    `yt_url('vid1 vid2 vid1', True)`
    will print `title2` from `vid2` instead `title1` from last entry `vid1`.

    Args:
        url: youtube url
        print_title: print title or not
    """
    url_list = url.split()

    g.model.songs = []

    v_ids = set()
    v_title = None
    for url in url_list:
        try:
            v_id = pafy.extract_video_id(url)
            if v_id in v_ids:
                continue
            p = pafy.get_video_info(v_id)
        except (IOError, ValueError) as e:
            g.message = c.r + str(e) + c.w
            g.content = g.content or content.generate_songlist_display(
                    zeromsg=g.message)
            return

        g.browse_mode = "normal"
        v = Video(p['id'], p['title'], int(p['duration']['secondsText']))
        if p and isinstance(p, dict):
            v_title = p.get("title")
        g.model.songs.append(v)
        v_ids.add(v_id)

    if not g.command_line:
        g.content = content.generate_songlist_display()

    if print_title and v_title:
        util.xprint(v_title)


@command(r'url_file\s(\S+)', 'url_file')
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
