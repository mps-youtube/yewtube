from youtubesearchpython import VideosSearch, StreamURLFetcher, Video
import yt_dlp

def get_video_streams(ytid):
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(ytid, download=False)
        return [i for i in info_dict['formats'] if i['format_note'] != 'storyboard']
def video_search(query):
    videosSearch = VideosSearch(query, limit=10)
    wdata = videosSearch.result()['result']
    return wdata