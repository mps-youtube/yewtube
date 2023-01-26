import json
import os
import random
import re
from urllib.parse import parse_qs, urlparse

import requests
import yt_dlp
from youtubesearchpython import *


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

def download_video(ytid, folder, audio_only=False):

    '''
    Given a youtube video id and target folder, this function will download video to that folder
    '''

    ytdl_format_options = {
        'outtmpl': os.path.join(folder, '%(title)s-%(id)s.%(ext)s')
    }
    if audio_only:
        ytdl_format_options['format'] = 'bestaudio/best'
        ytdl_format_options['postprocessors'] =[{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    with yt_dlp.YoutubeDL(ytdl_format_options) as ydl:
        ydl.download('https://www.youtube.com/watch?v=%s' % ytid)
        return True

def search_videos(query, pages):

    '''
    Given a keyword / query this function will return youtube video results against those keywords / query
    '''

    videosSearch = VideosSearch(query, limit=50)
    wdata = videosSearch.result()['result']
    for i in range(pages-1):
        videosSearch.next()
        wdata.extend(videosSearch.result()['result'])
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

    playlist = Playlist('https://www.youtube.com/playlist?list=%s' % playlist_id)
    while playlist.hasMoreVideos:
        playlist.getNextVideos()
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

def get_comments(video_id):
    comments = Comments.get(video_id)
    return comments['result']

def get_video_info(video_id):
    videoInfo = Video.getInfo(video_id)
    response = return_dislikes(video_id)
    videoInfo['likes'] = response['likes']
    videoInfo['dislikes'] = response['dislikes']
    videoInfo['averageRating'] = response['rating']
    return videoInfo

def return_dislikes(video_id):
    return json.loads(requests.get('https://returnyoutubedislikeapi.com/votes?videoId=' + video_id).text)


def extract_video_id(url: str) -> str:
    """Extract the video id from a url, return video id as str.

    Args:
        url: url contain video id

    Returns:
        video id

    Raises:
        ValueError: If no video id found

    Examples:

        >>> extract_video_id('http://example.com')
        >>> extract_video_id('https://www.youtube.com/watch?v=LDU_Txk06tM')
        LDU_Txk06tM
        >>> extract_video_id('https://youtu.be/LDU_Txk06tM')
        LDU_Txk06tM
    """
    idregx = re.compile(r'[\w-]{11}$')
    url = str(url).strip()

    if idregx.match(url):
        return url # ID of video

    if '://' not in url:
        url = '//' + url
    parsedurl = urlparse(url)
    if parsedurl.netloc in ('youtube.com', 'www.youtube.com', 'm.youtube.com', 'gaming.youtube.com'):
        query = parse_qs(parsedurl.query)
        if 'v' in query and idregx.match(query['v'][0]):
            return query['v'][0]
    elif parsedurl.netloc in ('youtu.be', 'www.youtu.be'):
        vidid = parsedurl.path.split('/')[-1] if parsedurl.path else ''
        if idregx.match(vidid):
            return vidid

    err = "Need 11 character video id or the URL of the video. Got %s"
    raise ValueError(err % url)

def all_playlists_from_channel(channel_id):
    channel = Channel(channel_id)
    playlists = channel.result['playlists']
    while channel.has_more_playlists():
         channel.next()
         playlists.extend(channel.result["playlists"])
    return playlists