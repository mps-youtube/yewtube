import os
import sys
import pickle

from . import g, c, screen, util, pafy
from .playlist import Playlist, Video


def save():
    """ Save playlists.  Called each time a playlist is saved or deleted. """
    for pl in g.userpl:
        with open(os.path.join(g.PLFOLDER, pl+'.m3u'), 'w') as plf:
            plf.write('#EXTM3U\n\n')
            for song in g.userpl[pl].songs:
                plf.write('#EXTINF:%d,%s\n' % (song.length, song.title))
                plf.write('https://www.youtube.com/watch?v=%s\n' % song.ytid)

    util.dbg(c.r + "Playlist saved\n---" + c.w)


def load():
    """ Open playlists. Called once on script invocation. """
    _convert_playlist_to_v2()
    _convert_playlist_to_m3u()
    try:
        # Loop through all files ending in '.m3u'
        for m3u in [m3u for m3u in os.listdir(g.PLFOLDER) if m3u[-4:] == '.m3u']:
            g.userpl[m3u[:-4]] = read_m3u(os.path.join(g.PLFOLDER, m3u))

    except FileNotFoundError:
        # No playlist folder, create an empty one
        if not os.path.isdir(g.PLFOLDER):
            g.userpl = {}
            os.mkdir(g.PLFOLDER)
            save()

    # remove any cached urls from playlist file, these are now
    # stored in a separate cache file

    do_save = False

    for k, v in g.userpl.items():
        for song in v.songs:
            if hasattr(song, "urls"):
                util.dbg("remove %s: %s", k, song.urls)
                del song.urls
                do_save = True

    if do_save:
        save()


def delete(name):
    """ Delete playlist, including m3u file. """
    del g.userpl[name]
    os.remove(os.path.join(g.PLFOLDER, name + '.m3u'))
    

def read_m3u(m3u):
    """ Processes an m3u file into a Playlist object. """
    name = os.path.basename(m3u)[:-4]
    songs = []
    expect_ytid = False

    with open(m3u, 'r') as plf:
        if plf.readline().startswith('#EXTM3U'):
            for line in plf:
                if line.startswith('#EXTINF:') and not expect_ytid:
                    duration, title = line.replace('#EXTINF:', '').strip().split(',', 1)
                    expect_ytid = True
                elif not line.startswith('\n') and not line.startswith('#') and expect_ytid:
                    try:
                        expect_ytid = False
                        ytid = pafy.extract_video_id(line).strip()
                        songs.append(Video(ytid, title, int(duration)))
                    except ValueError as ex:
                        util.dbg(c.r + str(ex) + c.w)
        # Handles a simple m3u file which should just be a list of urls
        else:
            plf.seek(0)
            for line in plf:
                if not line.startswith('#'):
                    try:
                        p = util.get_pafy(line)
                        songs.append(Video(p.videoid, p.title, p.length))
                    except (IOError, ValueError) as e:
                        util.dbg(c.r + "Error loading video: " + str(e) + c.w)

    return Playlist(name, songs)


def _convert_playlist_to_v2():
    """ Convert previous playlist file to v2 playlist. """
    # skip if previously done
    if os.path.isfile(g.PLFILE):
        return

    # skip if no playlist files exist
    elif not os.path.isfile(g.OLD_PLFILE):
        return

    try:
        with open(g.OLD_PLFILE, "rb") as plf:
            old_playlists = pickle.load(plf)

    except IOError:
        sys.exit("Couldn't open old playlist file")

    # rename old playlist file
    backup = g.OLD_PLFILE + "_v1_backup"

    if os.path.isfile(backup):
        sys.exit("Error, backup exists but new playlist exists not!")

    os.rename(g.OLD_PLFILE, backup)

    # do the conversion
    for plname, plitem in old_playlists.items():

        songs = []

        for video in plitem.songs:
            v = Video(video['link'], video['title'], video['duration'])
            songs.append(v)

        g.userpl[plname] = Playlist(plname, songs)

    # save as v2
    os.mkdir(g.PLFOLDER)
    save()


def _convert_playlist_to_m3u():
    """ Convert playlist_v2 file to the m3u format. 
        This should create a .m3u playlist for each playlist in playlist_v2. """
    # Skip if playlists folder exists
    if os.path.isdir(g.PLFOLDER):
        return

    # Skip if no playlist files exist
    elif not os.path.isfile(g.PLFILE):
        return

    try: 
        with open(g.PLFILE, 'rb') as plf:
            old_playlists = pickle.load(plf)

    except AttributeError:
        # playlist is from a time when this module was __main__
        # https://github.com/np1/mps-youtube/issues/214
        import __main__
        __main__.Playlist = Playlist
        __main__.Video = Video

        from . import main
        main.Playlist = Playlist
        main.Video = Video

        with open(g.PLFILE, "rb") as plf:
            g.userpl = pickle.load(plf)

        os.mkdir(g.PLFOLDER)
        save()
        screen.msgexit("Updated playlist file. Please restart yewtube", 1)

    except EOFError:
        screen.msgexit("Error opening playlists from %s" % g.PLFILE, 1)

    except IOError:
        sys.exit("Couldn't open old playlist file")

    for pl in old_playlists:
        songs = []
        for song in old_playlists[pl]:
            songs.append(song)

        g.userpl[pl] = Playlist(pl, songs)

    os.mkdir(g.PLFOLDER)
    save()
