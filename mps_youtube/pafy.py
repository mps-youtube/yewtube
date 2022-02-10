from youtubesearchpython import *
import yt_dlp, random, os

class MyLogger:
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def get_video_streams(ytid):

    '''
    given a youtube video id returns different video / audio stream formats' \
    '''

    with yt_dlp.YoutubeDL({'logger':MyLogger()}) as ydl:
        info_dict = ydl.extract_info(ytid, download=False)
        return [i for i in info_dict['formats'] if i.get('format_note') != 'storyboard']

def download_video(ytid, folder):

    '''
    Given a youtube video id and target folder, this function will download video to that folder
    '''

    ytdl_format_options = {
        'outtmpl': os.path.join(folder, '%(title)s-%(id)s.%(ext)s')
    }

    with yt_dlp.YoutubeDL(ytdl_format_options) as ydl:
        ydl.download('https://www.youtube.com/watch?v=%s' % ytid)
        return True

def video_search(query):

    '''
    Given a keyword / query this function will return youtube video results against those keywords / query
    '''

    videosSearch = VideosSearch(query, limit=50)
    wdata = videosSearch.result()['result']
    return wdata

def channel_search(query):

    '''
    Search channel based on keyword / query provided by user
    '''

    channelsSearch = ChannelsSearch(query, limit=50, region='US')
    return channelsSearch.result()['result']

def playlist_search(query):

    '''
    Returns all playlists having similar names as keyword / query provided
    '''

    playlistsSearch = PlaylistsSearch(query, limit=50)
    return playlistsSearch.result()['result']

def get_playlist(playlist_id):

    '''
    Get all videos of a playlist identified by playlist_id
    '''

    playlist = Playlist.get('https://www.youtube.com/playlist?list=%s' % playlist_id)
    return playlist

def get_video_title_suggestions(query):
    suggestions = Suggestions(language = 'en', region = 'US')
    related_searches = suggestions.get(query)['result']
    return related_searches[random.randint(0,len(related_searches))]

def channel_id_from_name(query):
    channel_info = channel_search(query)[0]
    channel_id = channel_info['id']
    channel_name = channel_info['title']
    return (channel_id, channel_name)

def all_videos_from_channel(channel_id):
    playlist = Playlist(playlist_from_channel_id(channel_id))
    return playlist.videos

def search_videos_from_channel(channel_id, query):
    search = ChannelSearch(query , channel_id)
    return search.result()